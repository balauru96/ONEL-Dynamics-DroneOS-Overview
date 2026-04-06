import asyncio
from typing import Dict, Any


class PX4Bridge:
    def __init__(self):
        self.connected: bool = False
        self._state: Dict[str, Any] = {
            "armed": False,
            "position": (0.0, 0.0, 0.0),
            "mode": "UNKNOWN",
        }

    async def connect(self) -> None:
        if self.connected:
            return
        print("Connecting to PX4...")
        await asyncio.sleep(1)
        self.connected = True
        print("Connected.")

    async def disconnect(self) -> None:
        if not self.connected:
            return
        print("Disconnecting...")
        await asyncio.sleep(1)
        self.connected = False
        print("Disconnected.")

    async def reconnect(self) -> None:
        print("Reconnecting...")
        await self.disconnect()
        await self.connect()

    def is_connected(self) -> bool:
        return self.connected

    async def get_state(self) -> Dict[str, Any]:
        await asyncio.sleep(0.1)
        return self._state

    async def arm(self) -> None:
        if not self.connected:
            raise RuntimeError("Not connected")
        print("Arming drone...")
        await asyncio.sleep(0.5)
        self._state["armed"] = True

    async def disarm(self) -> None:
        print("Disarming drone...")
        await asyncio.sleep(0.5)
        self._state["armed"] = False

    async def takeoff(self, altitude: float = 5.0) -> None:
        if not self._state["armed"]:
            raise RuntimeError("Drone not armed")
        print(f"Taking off to {altitude} meters...")
        await asyncio.sleep(1)
        self._state["position"] = (0.0, 0.0, altitude)

    async def land(self) -> None:
        print("Landing...")
        await asyncio.sleep(1)
        self._state["position"] = (0.0, 0.0, 0.0)

    async def rtl(self) -> None:
        print("Returning to launch...")
        await asyncio.sleep(1)
        self._state["position"] = (0.0, 0.0, 0.0)

    async def send_waypoints(self, waypoints: list) -> None:
        print(f"Uploading {len(waypoints)} waypoints...")
        await asyncio.sleep(1)
