from __future__ import annotations

import asyncio
import json
import math
import time
from collections import deque
from pathlib import Path
from typing import Any, Dict, List, Optional


from fastapi import FastAPI, HTTPException, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, JSONResponse

from tasks.px4_bridge_stub import PX4Bridge


# =========================================================
# CONFIG
# =========================================================

USE_PX4 = True

DEFAULT_SPEED = 0.00012
MANUAL_SPEED = 0.00012
VERTICAL_SPEED = 2.0

MIN_ALTITUDE = 0.0
MAX_ALTITUDE = 120.0

BATTERY_CAPACITY = 100.0
BATTERY_LOW = 15.0
BATTERY_CRITICAL = 5.0

HOME_LAT = 47.0707
HOME_LON = 15.4395

MAX_TRAIL_POINTS = 500

PX4_SYNC_INTERVAL = 0.20
PX4_RETRY_DELAY = 2.0
WS_BROADCAST_INTERVAL = 0.20

COMMAND_COOLDOWN = 1.5

BASE_DIR = Path(__file__).resolve().parent
WEB_DIR = BASE_DIR / "web"
DASHBOARD_FILE = WEB_DIR / "dashboard.html"
LOGS_DIR = BASE_DIR.parent / "logs"
LOGS_DIR.mkdir(parents=True, exist_ok=True)


# =========================================================
# APP
# =========================================================

app = FastAPI(title="DroneOS API", version="2.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# =========================================================
# GLOBAL STATE
# =========================================================

DRONE_STATE: Dict[str, Any] = {
    "lat": HOME_LAT,
    "lon": HOME_LON,
    "altitude": 0.0,
    "battery": 100.0,
    "flying": False,
    "armed": False,
    "mode": "MANUAL",
    "heading": 0.0,
    "home_lat": HOME_LAT,
    "home_lon": HOME_LON,
    "health_ok": False,
    "target_lat": HOME_LAT,
    "target_lon": HOME_LON,
    "path_preview": [],
    "trail": [],
    "waypoints": [],
    "current_waypoint_index": -1,
    "autopilot_active": False,
    "rtl_active": False,
    "mission_type": "IDLE",
    "flight_state": "LANDED",  # LANDED | FLYING
    "warning_message": "",
    "no_fly_zones": [],
    "px4_connected": False,
    "px4_mode": "SIM" if not USE_PX4 else "PX4 (disconnected)",
    "px4_link_state": "DISCONNECTED",  # DISCONNECTED | CONNECTING | CONNECTED
    "last_updated": time.time(),
}

_ws_clients: set[WebSocket] = set()
_ws_lock = asyncio.Lock()
_px4_lock = asyncio.Lock()

_last_command_ts = 0.0

_manual_active: Dict[str, bool] = {
    "forward": False,
    "backward": False,
    "left": False,
    "right": False,
    "up": False,
    "down": False,
    "yaw_left": False,
    "yaw_right": False,
}

px4_bridge = PX4Bridge()


# =========================================================
# TELEMETRY / HISTORY
# =========================================================


class TelemetryService:
    def __init__(self, maxlen: int = 1000) -> None:
        self._items: deque[Dict[str, Any]] = deque(maxlen=maxlen)
        self._flight_active = False
        self._current_flight_name: Optional[str] = None
        self._current_flight_points: List[Dict[str, Any]] = []

    def record(self, state: Dict[str, Any]) -> None:
        item = {
            "ts": time.time(),
            "lat": float(state.get("lat", HOME_LAT)),
            "lon": float(state.get("lon", HOME_LON)),
            "altitude": float(state.get("altitude", 0.0)),
            "battery": float(state.get("battery", 100.0)),
            "mode": str(state.get("mode", "MANUAL")),
            "flying": bool(state.get("flying", False)),
            "armed": bool(state.get("armed", False)),
        }
        self._items.append(item)

        flying = bool(state.get("flying", False))

        if flying and not self._flight_active:
            self._flight_active = True
            self._current_flight_name = f"flight_{time.strftime('%Y%m%d_%H%M%S')}.json"
            self._current_flight_points = []

        if self._flight_active:
            self._current_flight_points.append(item)

        if not flying and self._flight_active:
            self._flush_current_flight(state)

    def _flush_current_flight(self, state: Dict[str, Any]) -> None:
        if not self._current_flight_name or not self._current_flight_points:
            self._flight_active = False
            self._current_flight_name = None
            self._current_flight_points = []
            return

        flight_name = self._current_flight_name
        flight_points = self._current_flight_points.copy()

        meta = {
            "name": flight_name,
            "points": len(flight_points),
            "battery_end": float(state.get("battery", 0.0)),
            "ended_at": time.time(),
        }

        payload = {
            "meta": meta,
            "telemetry": flight_points,
        }

        path = LOGS_DIR / flight_name

        def save_file():
            path.write_text(json.dumps(payload, indent=2), encoding="utf-8")

        asyncio.create_task(asyncio.to_thread(save_file))

        self._flight_active = False
        self._current_flight_name = None
        self._current_flight_points = []

    def get_recent(self, limit: int = 50) -> List[Dict[str, Any]]:
        items = list(self._items)
        return items[-limit:]

    def list_history(self) -> List[Dict[str, Any]]:
        files = sorted(LOGS_DIR.glob("flight_*.json"), reverse=True)
        return [{"name": f.name} for f in files]

    def read_history(self, filename: str) -> Dict[str, Any]:
        path = LOGS_DIR / filename
        if not path.exists():
            raise FileNotFoundError(filename)
        return json.loads(path.read_text(encoding="utf-8"))


telemetry_service = TelemetryService()


# =========================================================
# HELPERS
# =========================================================


def _now() -> float:
    return time.time()


def _set_warning(message: str) -> None:
    DRONE_STATE["warning_message"] = message


def _clear_warning() -> None:
    DRONE_STATE["warning_message"] = ""


def _update_flight_state() -> None:
    DRONE_STATE["flight_state"] = (
        "FLYING" if DRONE_STATE.get("flying", False) else "LANDED"
    )


def _clear_nav_state() -> None:
    DRONE_STATE["autopilot_active"] = False
    DRONE_STATE["rtl_active"] = False
    DRONE_STATE["mission_type"] = "IDLE"
    DRONE_STATE["current_waypoint_index"] = -1


def _soft_reset_flight_state_on_disconnect() -> None:
    DRONE_STATE["px4_connected"] = False
    DRONE_STATE["px4_mode"] = "PX4 (disconnected)"
    DRONE_STATE["px4_link_state"] = "DISCONNECTED"
    DRONE_STATE["armed"] = False
    DRONE_STATE["flying"] = False
    DRONE_STATE["mode"] = "MANUAL"
    _update_flight_state()
    _clear_nav_state()


def _apply_command_cooldown() -> None:
    global _last_command_ts
    now = _now()
    delta = now - _last_command_ts
    if delta < COMMAND_COOLDOWN:
        raise RuntimeError("Command cooldown active")
    _last_command_ts = now


def _require_px4_command_ready() -> None:
    if not USE_PX4:
        return

    link_state = DRONE_STATE.get("px4_link_state", "DISCONNECTED")
    if link_state == "CONNECTING":
        raise RuntimeError("PX4 is reconnecting, wait a moment")
    if link_state != "CONNECTED":
        raise RuntimeError("Drone not connected")


def _require_state(expected: List[str]) -> None:
    current = DRONE_STATE.get("flight_state", "UNKNOWN")
    if current not in expected:
        raise RuntimeError(f"Invalid state: {current}, expected one of {expected}")


def _distance_m(a_lat: float, a_lon: float, b_lat: float, b_lon: float) -> float:
    # simplu și suficient pentru planner local
    r = 6371000.0
    lat1 = math.radians(a_lat)
    lat2 = math.radians(b_lat)
    dlat = math.radians(b_lat - a_lat)
    dlon = math.radians(b_lon - a_lon)

    x = dlon * math.cos((lat1 + lat2) / 2.0)
    y = dlat
    return math.sqrt(x * x + y * y) * r


def _in_no_fly_zone(lat: float, lon: float) -> bool:
    for z in DRONE_STATE.get("no_fly_zones", []):
        if _distance_m(lat, lon, float(z["lat"]), float(z["lon"])) <= float(
            z["radius_m"]
        ):
            return True
    return False


def _append_trail(lat: float, lon: float) -> None:
    trail = DRONE_STATE["trail"]
    trail.append([lat, lon])
    if len(trail) > MAX_TRAIL_POINTS:
        DRONE_STATE["trail"] = trail[-MAX_TRAIL_POINTS:]


def _snapshot() -> Dict[str, Any]:
    return json.loads(json.dumps(DRONE_STATE))


def _build_status_snapshot() -> Dict[str, Any]:
    snap = _snapshot()
    return {
        "mode": "PX4" if USE_PX4 else "SIM",
        "px4_connected": snap.get("px4_connected", False),
        "px4_link_state": snap.get("px4_link_state", "DISCONNECTED"),
        "ws_clients": len(_ws_clients),
        "flying": snap.get("flying", False),
        "battery": round(float(snap.get("battery", 0.0)), 1),
        "altitude": round(float(snap.get("altitude", 0.0)), 2),
    }


# =========================================================
# SIMPLE PLANNER HELPERS
# =========================================================


def _generate_circle_points(
    center_lat: float,
    center_lon: float,
    radius_m: float,
    count: int,
) -> List[Dict[str, float]]:
    pts: List[Dict[str, float]] = []
    meters_per_deg_lat = 111320.0
    meters_per_deg_lon = 111320.0 * math.cos(math.radians(center_lat))

    for i in range(count):
        a = (2.0 * math.pi * i) / count
        dlat = (radius_m * math.sin(a)) / meters_per_deg_lat
        dlon = (radius_m * math.cos(a)) / meters_per_deg_lon
        pts.append({"lat": center_lat + dlat, "lon": center_lon + dlon})
    return pts


def _build_mission(
    mission_type: str, center_lat: float, center_lon: float
) -> List[Dict[str, float]]:
    mission_type = mission_type.lower()

    if mission_type == "survey":
        return _generate_circle_points(center_lat, center_lon, 60.0, 8)

    if mission_type == "patrol":
        return _generate_circle_points(center_lat, center_lon, 90.0, 6)

    if mission_type == "inspection":
        return _generate_circle_points(center_lat, center_lon, 35.0, 4)

    if mission_type == "agriculture":
        return _generate_circle_points(center_lat, center_lon, 120.0, 10)

    raise RuntimeError(f"Unknown mission type: {mission_type}")


# =========================================================
# PX4 SYNC
# =========================================================


async def _px4_sync_once() -> None:
    px4 = await px4_bridge.get_state()

    async with _px4_lock:
        DRONE_STATE["lat"] = float(px4.get("lat", DRONE_STATE["lat"]))
        DRONE_STATE["lon"] = float(px4.get("lon", DRONE_STATE["lon"]))
        DRONE_STATE["altitude"] = float(px4.get("altitude", DRONE_STATE["altitude"]))
        DRONE_STATE["battery"] = float(px4.get("battery", DRONE_STATE["battery"]))
        DRONE_STATE["flying"] = bool(px4.get("flying", DRONE_STATE["flying"]))
        DRONE_STATE["armed"] = bool(px4.get("armed", DRONE_STATE["armed"]))
        DRONE_STATE["mode"] = str(px4.get("flight_mode", DRONE_STATE["mode"]))
        DRONE_STATE["heading"] = float(px4.get("heading", DRONE_STATE["heading"]))
        DRONE_STATE["home_lat"] = float(px4.get("home_lat", DRONE_STATE["home_lat"]))
        DRONE_STATE["home_lon"] = float(px4.get("home_lon", DRONE_STATE["home_lon"]))
        DRONE_STATE["health_ok"] = bool(px4.get("health_ok", DRONE_STATE["health_ok"]))
        DRONE_STATE["last_updated"] = _now()

        DRONE_STATE["px4_connected"] = True
        DRONE_STATE["px4_mode"] = "PX4"
        DRONE_STATE["px4_link_state"] = "CONNECTED"

        _update_flight_state()
        _append_trail(float(DRONE_STATE["lat"]), float(DRONE_STATE["lon"]))

    telemetry_service.record(DRONE_STATE)


async def _px4_sync_loop() -> None:
    print("[PX4] Sync loop started")

    while True:
        try:
            if not px4_bridge.connected:
                async with _px4_lock:
                    DRONE_STATE["px4_link_state"] = "CONNECTING"

                print("[PX4] Connecting...")
                await px4_bridge.connect()

                async with _px4_lock:
                    DRONE_STATE["px4_connected"] = True
                    DRONE_STATE["px4_mode"] = "PX4"
                    DRONE_STATE["px4_link_state"] = "CONNECTED"

                print("[PX4] Connected")

            await _px4_sync_once()

        except Exception as e:
            print(f"[PX4] Sync error: {e}, retry in {PX4_RETRY_DELAY}s")
            async with _px4_lock:
                _soft_reset_flight_state_on_disconnect()
            await asyncio.sleep(PX4_RETRY_DELAY)

        await asyncio.sleep(PX4_SYNC_INTERVAL)


async def _ws_broadcast_loop() -> None:
    while True:
        try:
            payload = json.dumps(_snapshot())

            async with _ws_lock:
                clients = list(_ws_clients)

            if clients:
                coros = []
                for ws in clients:
                    coros.append(ws.send_text(payload))
                results = await asyncio.gather(*coros, return_exceptions=True)

                dead: List[WebSocket] = []
                for ws, res in zip(clients, results):
                    if isinstance(res, Exception):
                        dead.append(ws)

                if dead:
                    async with _ws_lock:
                        for ws in dead:
                            _ws_clients.discard(ws)

        except Exception as e:
            print("[WS] broadcast error:", e)

        await asyncio.sleep(WS_BROADCAST_INTERVAL)


# =========================================================
# STARTUP / SHUTDOWN
# =========================================================

_px4_task: Optional[asyncio.Task] = None
_ws_task: Optional[asyncio.Task] = None


@app.on_event("startup")
async def on_startup() -> None:
    global _px4_task, _ws_task

    print("[DroneOS] startup")

    if USE_PX4:
        _px4_task = asyncio.create_task(_px4_sync_loop())

    _ws_task = asyncio.create_task(_ws_broadcast_loop())


@app.on_event("shutdown")
async def on_shutdown() -> None:
    global _px4_task, _ws_task

    print("[DroneOS] shutdown")

    if _px4_task:
        _px4_task.cancel()
        try:
            await _px4_task
        except Exception:
            pass
        _px4_task = None

    if _ws_task:
        _ws_task.cancel()
        try:
            await _ws_task
        except Exception:
            pass
        _ws_task = None

    if USE_PX4:
        await px4_bridge.disconnect()


# =========================================================
# ROUTES - UI / BASIC
# =========================================================


@app.get("/")
async def root() -> FileResponse:
    return FileResponse(DASHBOARD_FILE)


@app.get("/dashboard")
async def dashboard() -> FileResponse:
    return FileResponse(DASHBOARD_FILE)


@app.get("/state")
async def get_state() -> Dict[str, Any]:
    return _snapshot()


@app.get("/api/status")
async def api_status() -> Dict[str, Any]:
    return _build_status_snapshot()


@app.get("/telemetry")
async def telemetry() -> Dict[str, Any]:
    return {"items": telemetry_service.get_recent(100)}


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket) -> None:
    await websocket.accept()
    async with _ws_lock:
        _ws_clients.add(websocket)

    try:
        await websocket.send_text(json.dumps(_snapshot()))
        while True:
            await websocket.receive_text()
    except WebSocketDisconnect:
        pass
    finally:
        async with _ws_lock:
            _ws_clients.discard(websocket)


# =========================================================
# COMMAND ROUTES
# =========================================================


@app.post("/arm")
async def arm() -> Dict[str, Any]:
    try:
        _apply_command_cooldown()
        _require_px4_command_ready()
        _require_state(["LANDED"])

        if USE_PX4:
            await px4_bridge.arm()

        return {"ok": True}

    except Exception as e:
        return JSONResponse(status_code=400, content={"ok": False, "message": str(e)})


@app.post("/takeoff")
async def takeoff() -> Dict[str, Any]:
    try:
        _apply_command_cooldown()
        _require_px4_command_ready()
        _require_state(["LANDED"])

        if USE_PX4:
            if not await px4_bridge.is_armable():
                raise RuntimeError("Drone not ready (GPS / home missing)")
            await px4_bridge.takeoff()

        DRONE_STATE["target_lat"] = DRONE_STATE["lat"]
        DRONE_STATE["target_lon"] = DRONE_STATE["lon"]
        return {"ok": True}

    except Exception as e:
        return JSONResponse(status_code=400, content={"ok": False, "message": str(e)})


@app.post("/land")
async def land() -> Dict[str, Any]:
    try:
        _apply_command_cooldown()
        _require_px4_command_ready()
        _require_state(["FLYING"])

        if USE_PX4:
            await px4_bridge.land()

        _clear_nav_state()
        return {"ok": True}

    except Exception as e:
        return JSONResponse(status_code=400, content={"ok": False, "message": str(e)})


@app.post("/rtl")
async def rtl() -> Dict[str, Any]:
    try:
        _apply_command_cooldown()
        _require_px4_command_ready()
        _require_state(["FLYING"])

        if USE_PX4:
            await px4_bridge.rtl()

        DRONE_STATE["rtl_active"] = True
        DRONE_STATE["autopilot_active"] = False
        DRONE_STATE["mission_type"] = "RTL"
        DRONE_STATE["target_lat"] = DRONE_STATE["home_lat"]
        DRONE_STATE["target_lon"] = DRONE_STATE["home_lon"]
        return {"ok": True}

    except Exception as e:
        return JSONResponse(status_code=400, content={"ok": False, "message": str(e)})


# =========================================================
# AUTOPILOT / MISSION / PLANNER
# =========================================================


@app.post("/autopilot/start")
async def autopilot_start() -> Dict[str, Any]:
    try:
        _apply_command_cooldown()

        if not DRONE_STATE["waypoints"]:
            raise RuntimeError("No mission loaded")

        await px4_bridge.start_mission(DRONE_STATE["waypoints"])

        DRONE_STATE["autopilot_active"] = True
        DRONE_STATE["rtl_active"] = False
        DRONE_STATE["current_waypoint_index"] = 0
        DRONE_STATE["mission_type"] = "AUTO"

        wp = DRONE_STATE["waypoints"][0]
        DRONE_STATE["target_lat"] = wp["lat"]
        DRONE_STATE["target_lon"] = wp["lon"]

        return {"ok": True}

    except Exception as e:
        return JSONResponse(
            status_code=400,
            content={"ok": False, "message": str(e)},
        )


@app.post("/autopilot/stop")
async def autopilot_stop() -> Dict[str, Any]:
    DRONE_STATE["autopilot_active"] = False
    DRONE_STATE["current_waypoint_index"] = -1
    DRONE_STATE["mission_type"] = "IDLE"
    return {"ok": True}


@app.post("/mission/cancel")
async def mission_cancel() -> Dict[str, Any]:
    _clear_nav_state()
    DRONE_STATE["waypoints"] = []
    DRONE_STATE["path_preview"] = []
    return {"ok": True}


@app.post("/plan")
async def upload_plan(payload: Dict[str, Any]) -> Dict[str, Any]:
    try:
        waypoints = payload.get("waypoints", [])
        if not isinstance(waypoints, list) or not waypoints:
            raise RuntimeError("No waypoints provided")

        clean_wps: List[Dict[str, float]] = []
        for wp in waypoints:
            lat = float(wp["lat"])
            lon = float(wp["lon"])
            if _in_no_fly_zone(lat, lon):
                raise RuntimeError("Waypoint inside No-Fly Zone")
            clean_wps.append({"lat": lat, "lon": lon})

        DRONE_STATE["waypoints"] = clean_wps
        DRONE_STATE["path_preview"] = clean_wps
        DRONE_STATE["current_waypoint_index"] = -1

        return {"ok": True, "waypoints": clean_wps}

    except Exception as e:
        return JSONResponse(status_code=400, content={"ok": False, "message": str(e)})


@app.post("/mission/start")
async def mission_start(payload: Dict[str, Any]) -> Dict[str, Any]:
    try:
        mission_type = str(payload.get("mission_type", "survey"))
        center_lat = float(payload["center_lat"])
        center_lon = float(payload["center_lon"])

        wps = _build_mission(mission_type, center_lat, center_lon)
        for wp in wps:
            if _in_no_fly_zone(wp["lat"], wp["lon"]):
                raise RuntimeError("Generated mission intersects No-Fly Zone")

        DRONE_STATE["waypoints"] = wps
        DRONE_STATE["path_preview"] = wps
        DRONE_STATE["mission_type"] = mission_type.upper()
        DRONE_STATE["autopilot_active"] = False
        DRONE_STATE["current_waypoint_index"] = -1

        return {"ok": True, "drone": _snapshot()}

    except Exception as e:
        return JSONResponse(status_code=400, content={"ok": False, "message": str(e)})


@app.post("/path/preview")
async def path_preview(payload: Dict[str, Any]) -> Dict[str, Any]:
    try:
        lat = float(payload["lat"])
        lon = float(payload["lon"])

        if _in_no_fly_zone(lat, lon):
            raise RuntimeError("Target is inside No-Fly Zone")

        preview = [
            {"lat": float(DRONE_STATE["lat"]), "lon": float(DRONE_STATE["lon"])},
            {"lat": lat, "lon": lon},
        ]
        DRONE_STATE["path_preview"] = preview
        DRONE_STATE["target_lat"] = lat
        DRONE_STATE["target_lon"] = lon
        return {"ok": True, "path_preview": preview}

    except Exception as e:
        return JSONResponse(status_code=400, content={"ok": False, "message": str(e)})


@app.post("/mission/preview")
async def mission_preview(payload: Dict[str, Any]) -> Dict[str, Any]:
    try:
        waypoints = payload.get("waypoints", [])
        if not isinstance(waypoints, list) or not waypoints:
            return {"ok": True, "mission_preview": []}

        preview = [
            {"lat": float(wp["lat"]), "lon": float(wp["lon"])} for wp in waypoints
        ]
        DRONE_STATE["path_preview"] = preview
        return {"ok": True, "mission_preview": preview}

    except Exception as e:
        return JSONResponse(status_code=400, content={"ok": False, "message": str(e)})


# =========================================================
# NO-FLY ZONES
# =========================================================


@app.post("/no_fly_zone")
async def add_no_fly_zone(payload: Dict[str, Any]) -> Dict[str, Any]:
    try:
        lat = float(payload["lat"])
        lon = float(payload["lon"])
        radius_m = float(payload["radius_m"])

        DRONE_STATE["no_fly_zones"].append(
            {
                "lat": lat,
                "lon": lon,
                "radius_m": radius_m,
            }
        )
        return {"ok": True}

    except Exception as e:
        return JSONResponse(status_code=400, content={"ok": False, "message": str(e)})


@app.post("/no_fly_zones/clear")
async def clear_no_fly_zones() -> Dict[str, Any]:
    DRONE_STATE["no_fly_zones"] = []
    return {"ok": True}


# =========================================================
# MANUAL CONTROL (placeholder safe endpoint)
# =========================================================


@app.post("/manual/control")
async def manual_control(payload: Dict[str, Any]) -> Dict[str, Any]:
    try:
        direction = str(payload.get("direction", ""))
        active = bool(payload.get("active", False))

        if direction not in _manual_active:
            raise RuntimeError("Unknown manual direction")

        _manual_active[direction] = active
        return {"ok": True}

    except Exception as e:
        return JSONResponse(status_code=400, content={"ok": False, "message": str(e)})


@app.post("/manual_move")
async def manual_move(payload: Dict[str, Any]) -> Dict[str, Any]:
    try:
        lat = float(payload["lat"])
        lon = float(payload["lon"])

        if _in_no_fly_zone(lat, lon):
            raise RuntimeError("Target is inside No-Fly Zone")

        DRONE_STATE["target_lat"] = lat
        DRONE_STATE["target_lon"] = lon
        return {"ok": True}

    except Exception as e:
        return JSONResponse(status_code=400, content={"ok": False, "message": str(e)})


# =========================================================
# HISTORY
# =========================================================


@app.get("/api/history")
async def history_list() -> List[Dict[str, Any]]:
    return telemetry_service.list_history()


@app.get("/api/history/{filename}")
async def history_read(filename: str) -> Dict[str, Any]:
    try:
        return telemetry_service.read_history(filename)
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="History file not found")
