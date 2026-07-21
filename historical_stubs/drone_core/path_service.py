from __future__ import annotations

import math
from typing import Any, Dict, List, Tuple


class PathService:
    def point_inside_no_fly(
        self,
        lat: float,
        lon: float,
        no_fly_zones: List[Dict[str, Any]],
    ) -> bool:
        meters_to_degrees = 1.0 / 111_111.0

        for zone in no_fly_zones:
            radius_deg = float(zone["radius_m"]) * meters_to_degrees
            dlat = float(lat) - float(zone["lat"])
            dlon = float(lon) - float(zone["lon"])
            dist = math.hypot(dlat, dlon)

            if dist <= radius_deg:
                return True

        return False

    def line_intersects_circle(
        self,
        start_lat: float,
        start_lon: float,
        end_lat: float,
        end_lon: float,
        center_lat: float,
        center_lon: float,
        radius_deg: float,
    ) -> bool:
        ax = start_lat
        ay = start_lon
        bx = end_lat
        by = end_lon
        cx = center_lat
        cy = center_lon

        abx = bx - ax
        aby = by - ay
        acx = cx - ax
        acy = cy - ay

        ab_len_sq = abx * abx + aby * aby
        if ab_len_sq == 0:
            dist = math.hypot(cx - ax, cy - ay)
            return dist <= radius_deg

        t = (acx * abx + acy * aby) / ab_len_sq
        t = max(0.0, min(1.0, t))

        closest_x = ax + t * abx
        closest_y = ay + t * aby

        dist = math.hypot(cx - closest_x, cy - closest_y)
        return dist <= radius_deg

    def build_detour_point(
        self,
        start_lat: float,
        start_lon: float,
        end_lat: float,
        end_lon: float,
        zone_lat: float,
        zone_lon: float,
        radius_deg: float,
    ) -> Dict[str, float]:
        # marjă extra ca să ocolească vizibil cercul
        safe_radius = radius_deg * 1.5

        path_dx = end_lat - start_lat
        path_dy = end_lon - start_lon
        path_len = math.hypot(path_dx, path_dy)

        if path_len == 0:
            return {
                "lat": zone_lat + safe_radius,
                "lon": zone_lon,
            }

        # perpendiculară pe traseu
        perp_x = -path_dy / path_len
        perp_y = path_dx / path_len

        option1 = {
            "lat": zone_lat + perp_x * safe_radius,
            "lon": zone_lon + perp_y * safe_radius,
        }
        option2 = {
            "lat": zone_lat - perp_x * safe_radius,
            "lon": zone_lon - perp_y * safe_radius,
        }

        def route_cost(p: Dict[str, float]) -> float:
            d1 = math.hypot(p["lat"] - start_lat, p["lon"] - start_lon)
            d2 = math.hypot(end_lat - p["lat"], end_lon - p["lon"])
            return d1 + d2

        return option1 if route_cost(option1) <= route_cost(option2) else option2

    def apply_smart_target(
        self,
        drone_state: Dict[str, Any],
        dest_lat: float,
        dest_lon: float,
    ) -> Tuple[bool, str]:
        no_fly_zones = drone_state.get("no_fly_zones", [])
        start_lat = float(drone_state["lat"])
        start_lon = float(drone_state["lon"])

        drone_state["path_preview"] = []
        drone_state["avoidance_queue"] = []

        # dacă punctul final e chiar în zona interzisă, refuzăm
        if self.point_inside_no_fly(dest_lat, dest_lon, no_fly_zones):
            return False, "Destination inside no-fly zone"

        meters_to_degrees = 1.0 / 111_111.0

        blocking_zone = None
        for zone in no_fly_zones:
            radius_deg = float(zone["radius_m"]) * meters_to_degrees

            if self.line_intersects_circle(
                start_lat,
                start_lon,
                float(dest_lat),
                float(dest_lon),
                float(zone["lat"]),
                float(zone["lon"]),
                radius_deg,
            ):
                blocking_zone = zone
                break

        # dacă nu intersectează nimic, traseu direct
        if blocking_zone is None:
            drone_state["path_preview"] = [
                {"lat": start_lat, "lon": start_lon},
                {"lat": float(dest_lat), "lon": float(dest_lon)},
            ]
            return True, "Direct path"

        # altfel construim un punct de ocolire
        radius_deg = float(blocking_zone["radius_m"]) * meters_to_degrees
        detour = self.build_detour_point(
            start_lat,
            start_lon,
            float(dest_lat),
            float(dest_lon),
            float(blocking_zone["lat"]),
            float(blocking_zone["lon"]),
            radius_deg,
        )

        # verificare simplă: punctul de ocolire să nu fie și el în no-fly
        if self.point_inside_no_fly(detour["lat"], detour["lon"], no_fly_zones):
            return False, "Could not compute safe detour"

        drone_state["avoidance_queue"] = [
            {"lat": detour["lat"], "lon": detour["lon"]},
        ]

        drone_state["path_preview"] = [
            {"lat": start_lat, "lon": start_lon},
            {"lat": detour["lat"], "lon": detour["lon"]},
            {"lat": float(dest_lat), "lon": float(dest_lon)},
        ]

        return True, "Detour path generated"