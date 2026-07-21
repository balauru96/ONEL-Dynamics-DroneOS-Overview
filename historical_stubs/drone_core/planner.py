import heapq
import math
from typing import Dict, Iterable, List, Optional, Set, Tuple


GridCell = Tuple[int, int]
LatLon = Tuple[float, float]


class AStarPlanner:
    def _init_(self, grid_w: int, grid_h: int, blocked_cells: Set[GridCell]) -> None:
        self.grid_w = grid_w
        self.grid_h = grid_h
        self.blocked = blocked_cells

    def in_bounds(self, cell: GridCell) -> bool:
        x, y = cell
        return 0 <= x < self.grid_w and 0 <= y < self.grid_h

    def is_blocked(self, cell: GridCell) -> bool:
        return cell in self.blocked

    def neighbors(self, cell: GridCell) -> Iterable[Tuple[GridCell, float]]:
        x, y = cell

        cardinal_moves = [
            ((1, 0), 1.0),
            ((-1, 0), 1.0),
            ((0, 1), 1.0),
            ((0, -1), 1.0),
        ]

        for (dx, dy), step_cost in cardinal_moves:
            nxt = (x + dx, y + dy)
            if self.in_bounds(nxt) and not self.is_blocked(nxt):
                yield nxt, step_cost

        diagonal_moves = [
            (1, 1),
            (1, -1),
            (-1, 1),
            (-1, -1),
        ]

        for dx, dy in diagonal_moves:
            nxt = (x + dx, y + dy)
            side_a = (x + dx, y)
            side_b = (x, y + dy)

            if not self.in_bounds(nxt):
                continue
            if self.is_blocked(nxt):
                continue

            # Fara taiere de colt printre obstacole
            if self.is_blocked(side_a) or self.is_blocked(side_b):
                continue

            yield nxt, math.sqrt(2)

    @staticmethod
    def heuristic(a: GridCell, b: GridCell) -> float:
        dx = abs(a[0] - b[0])
        dy = abs(a[1] - b[1])
        return max(dx, dy) + (math.sqrt(2) - 1) * min(dx, dy)

    def plan(self, start: GridCell, goal: GridCell) -> List[GridCell]:
        if start in self.blocked or goal in self.blocked:
            return []
        if start == goal:
            return [start]

        frontier: List[Tuple[float, GridCell]] = []
        heapq.heappush(frontier, (0.0, start))

        came_from: Dict[GridCell, Optional[GridCell]] = {start: None}
        cost_so_far: Dict[GridCell, float] = {start: 0.0}

        while frontier:
            _, current = heapq.heappop(frontier)

            if current == goal:
                break

            for nxt, step_cost in self.neighbors(current):
                new_cost = cost_so_far[current] + step_cost

                if nxt not in cost_so_far or new_cost < cost_so_far[nxt]:
                    cost_so_far[nxt] = new_cost
                    priority = new_cost + self.heuristic(nxt, goal)
                    heapq.heappush(frontier, (priority, nxt))
                    came_from[nxt] = current

        if goal not in came_from:
            return []

        path: List[GridCell] = []
        current: Optional[GridCell] = goal

        while current is not None:
            path.append(current)
            current = came_from[current]

        path.reverse()
        return path


class MissionPlanner:
    """
    Planner pentru DroneOS:
    - construieste un grid local in jurul segmentului
    - marcheaza no-fly zones ca blocked cells
    - ruleaza A*
    - aplica smoothing
    - intoarce traseu in lat/lon
    """

    def _init_(self, cell_size_m: float = 8.0, margin_m: float = 120.0) -> None:
        self.cell_size_m = float(cell_size_m)
        self.margin_m = float(margin_m)

    @staticmethod
    def meters_to_lat(meters: float) -> float:
        return meters / 111111.0

    @staticmethod
    def meters_to_lon(meters: float, ref_lat: float) -> float:
        scale = math.cos(math.radians(ref_lat))
        if abs(scale) < 1e-9:
            scale = 1e-9
        return meters / (111111.0 * scale)

    @staticmethod
    def distance_m(a_lat: float, a_lon: float, b_lat: float, b_lon: float) -> float:
        mean_lat = (a_lat + b_lat) / 2.0
        dlat_m = (b_lat - a_lat) * 111111.0
        dlon_m = (b_lon - a_lon) * 111111.0 * math.cos(math.radians(mean_lat))
        return math.hypot(dlat_m, dlon_m)

    def _build_bounds(
        self,
        start: Dict[str, float],
        goal: Dict[str, float],
        no_fly_zones: List[Dict],
    ) -> Tuple[float, float, float, float]:
        lat_values = [float(start["lat"]), float(goal["lat"])]
        lon_values = [float(start["lon"]), float(goal["lon"])]

        for zone in no_fly_zones:
            zlat = float(zone["lat"])
            zlon = float(zone["lon"])
            radius_m = float(zone["radius_m"]) + self.margin_m

            lat_values.extend([
                zlat - self.meters_to_lat(radius_m),
                zlat + self.meters_to_lat(radius_m),
            ])
            lon_values.extend([
                zlon - self.meters_to_lon(radius_m, zlat),
                zlon + self.meters_to_lon(radius_m, zlat),
            ])

        base_lat_min = min(lat_values)
        base_lat_max = max(lat_values)
        ref_lat = (base_lat_min + base_lat_max) / 2.0

        lat_margin = self.meters_to_lat(self.margin_m)
        lon_margin = self.meters_to_lon(self.margin_m, ref_lat)

        base_lon_min = min(lon_values)
        base_lon_max = max(lon_values)

        return (
            base_lat_min - lat_margin,
            base_lon_min - lon_margin,
            base_lat_max + lat_margin,
            base_lon_max + lon_margin,
        )

    def _grid_dimensions(
        self,
        lat_min: float,
        lon_min: float,
        lat_max: float,
        lon_max: float,
    ) -> Tuple[int, int]:
        height_m = self.distance_m(lat_min, lon_min, lat_max, lon_min)
        width_m = self.distance_m(lat_min, lon_min, lat_min, lon_max)

        grid_h = max(3, int(math.ceil(height_m / self.cell_size_m)) + 1)
        grid_w = max(3, int(math.ceil(width_m / self.cell_size_m)) + 1)
        return grid_w, grid_h

    def _world_to_grid(
        self,
        lat: float,
        lon: float,
        lat_min: float,
        lon_min: float,
        lat_max: float,
        lon_max: float,
        grid_w: int,
        grid_h: int,
    ) -> GridCell:
        lat_span = max(1e-12, lat_max - lat_min)
        lon_span = max(1e-12, lon_max - lon_min)

        x = int(round((lon - lon_min) / lon_span * (grid_w - 1)))
        y = int(round((lat - lat_min) / lat_span * (grid_h - 1)))

        x = max(0, min(grid_w - 1, x))
        y = max(0, min(grid_h - 1, y))
        return x, y

    def _grid_to_world(
        self,
        cell: GridCell,
        lat_min: float,
        lon_min: float,
        lat_max: float,
        lon_max: float,
        grid_w: int,
        grid_h: int,
    ) -> LatLon:
        x, y = cell

        lon = lon_min if grid_w <= 1 else lon_min + (x / (grid_w - 1)) * (lon_max - lon_min)
        lat = lat_min if grid_h <= 1 else lat_min + (y / (grid_h - 1)) * (lat_max - lat_min)

        return lat, lon

    def _build_blocked_cells(
        self,
        no_fly_zones: List[Dict],
        lat_min: float,
        lon_min: float,
        lat_max: float,
        lon_max: float,
        grid_w: int,
        grid_h: int,
        start_cell: GridCell,
        goal_cell: GridCell,
    ) -> Set[GridCell]:
        blocked: Set[GridCell] = set()

        safety_padding_m = self.cell_size_m * 0.75

        lat_span = max(1e-12, lat_max - lat_min)
        lon_span = max(1e-12, lon_max - lon_min)

        for zone in no_fly_zones:
            zlat = float(zone["lat"])
            zlon = float(zone["lon"])
            radius_m = float(zone["radius_m"]) + safety_padding_m

            lat_radius = self.meters_to_lat(radius_m)
            lon_radius = self.meters_to_lon(radius_m, zlat)

            zone_lat_min = zlat - lat_radius
            zone_lat_max = zlat + lat_radius
            zone_lon_min = zlon - lon_radius
            zone_lon_max = zlon + lon_radius

            x_min = int(max(0, math.floor((zone_lon_min - lon_min) / lon_span * (grid_w - 1))))
            x_max = int(min(grid_w - 1, math.ceil((zone_lon_max - lon_min) / lon_span * (grid_w - 1))))
            y_min = int(max(0, math.floor((zone_lat_min - lat_min) / lat_span * (grid_h - 1))))
            y_max = int(min(grid_h - 1, math.ceil((zone_lat_max - lat_min) / lat_span * (grid_h - 1))))

            for y in range(y_min, y_max + 1):
                for x in range(x_min, x_max + 1):
                    lat, lon = self._grid_to_world(
                        (x, y),
                        lat_min,
                        lon_min,
                        lat_max,
                        lon_max,
                        grid_w,
                        grid_h,
                    )

                    if self.distance_m(lat, lon, zlat, zlon) <= radius_m:
                        blocked.add((x, y))

        blocked.discard(start_cell)
        blocked.discard(goal_cell)
        return blocked

    def _line_of_sight_clear(
        self,
        a: GridCell,
        b: GridCell,
        blocked: Set[GridCell],
        grid_w: int,
        grid_h: int,
    ) -> bool:
        x0, y0 = a
        x1, y1 = b

        dx = x1 - x0
        dy = y1 - y0
        steps = max(abs(dx), abs(dy))

        if steps == 0:
            return True

        for i in range(steps + 1):
            t = i / steps
            x = int(round(x0 + dx * t))
            y = int(round(y0 + dy * t))

            if not (0 <= x < grid_w and 0 <= y < grid_h):
                return False
            if (x, y) in blocked:
                return False

        return True

    def _smooth_cell_path(
        self,
        cell_path: List[GridCell],
        blocked: Set[GridCell],
        grid_w: int,
        grid_h: int,
    ) -> List[GridCell]:
        if len(cell_path) <= 2:
            return cell_path

        smoothed: List[GridCell] = [cell_path[0]]
        anchor_index = 0

        while anchor_index < len(cell_path) - 1:
            best_index = anchor_index + 1

            for j in range(anchor_index + 1, len(cell_path)):
                if self._line_of_sight_clear(
                    cell_path[anchor_index],
                    cell_path[j],
                    blocked,
                    grid_w,
                    grid_h,
                ):
                    best_index = j
                else:
                    break

            smoothed.append(cell_path[best_index])
            anchor_index = best_index

        return smoothed

    @staticmethod
    def _compress_path(
        path: List[LatLon],
        min_keep_distance_m: float = 6.0,
    ) -> List[Dict[str, float]]:
        if not path:
            return []

        result: List[Dict[str, float]] = [{"lat": path[0][0], "lon": path[0][1]}]
        last_lat, last_lon = path[0]

        for lat, lon in path[1:]:
            mean_lat = (lat + last_lat) / 2.0
            dlat_m = (lat - last_lat) * 111111.0
            dlon_m = (lon - last_lon) * 111111.0 * math.cos(math.radians(mean_lat))
            dist = math.hypot(dlat_m, dlon_m)

            if dist >= min_keep_distance_m:
                result.append({"lat": lat, "lon": lon})
                last_lat, last_lon = lat, lon

        final_point = {"lat": path[-1][0], "lon": path[-1][1]}
        if result[-1] != final_point:
            result.append(final_point)

        return result
    
    def _offset_latlon(self, lat: float, lon: float, north_m: float, east_m: float) -> Dict[str, float]:
        return {
            "lat": lat + self.meters_to_lat(north_m),
            "lon": lon + self.meters_to_lon(east_m, lat),
        }

    def generate_lawnmower_pattern(
        self,
        center_lat: float,
        center_lon: float,
        width_m: float = 120.0,
        height_m: float = 80.0,
        lane_spacing_m: float = 15.0,
    ) -> List[Dict[str, float]]:
        """
        Genereaza waypointuri in model serpentina / lawnmower:
        - bun pentru survey
        - bun pentru agriculture
        """
        width_m = max(20.0, float(width_m))
        height_m = max(20.0, float(height_m))
        lane_spacing_m = max(5.0, float(lane_spacing_m))

        half_w = width_m / 2.0
        half_h = height_m / 2.0

        lane_count = max(2, int(math.floor(height_m / lane_spacing_m)) + 1)

        if lane_count == 1:
            y_offsets = [0.0]
        else:
            y_offsets = [
                -half_h + i * (height_m / (lane_count - 1))
                for i in range(lane_count)
            ]

        waypoints: List[Dict[str, float]] = []

        for i, y in enumerate(y_offsets):
            if i % 2 == 0:
                start_east = -half_w
                end_east = half_w
            else:
                start_east = half_w
                end_east = -half_w

            wp_start = self._offset_latlon(center_lat, center_lon, north_m=y, east_m=start_east)
            wp_end = self._offset_latlon(center_lat, center_lon, north_m=y, east_m=end_east)

            waypoints.append(wp_start)
            waypoints.append(wp_end)

        return waypoints

    def generate_survey_mission(
        self,
        center_lat: float,
        center_lon: float,
    ) -> List[Dict[str, float]]:
        return self.generate_lawnmower_pattern(
            center_lat=center_lat,
            center_lon=center_lon,
            width_m=120.0,
            height_m=80.0,
            lane_spacing_m=15.0,
        )

    def generate_agriculture_mission(
        self,
        center_lat: float,
        center_lon: float,
    ) -> List[Dict[str, float]]:
        return self.generate_lawnmower_pattern(
            center_lat=center_lat,
            center_lon=center_lon,
            width_m=180.0,
            height_m=120.0,
            lane_spacing_m=18.0,
        )

    def generate_patrol_mission(
        self,
        center_lat: float,
        center_lon: float,
        radius_m: float = 45.0,
    ) -> List[Dict[str, float]]:
        radius_m = max(15.0, float(radius_m))
        points: List[Dict[str, float]] = []

        for angle_deg in [0, 60, 120, 180, 240, 300]:
            angle = math.radians(angle_deg)
            north_m = math.cos(angle) * radius_m
            east_m = math.sin(angle) * radius_m
            points.append(self._offset_latlon(center_lat, center_lon, north_m, east_m))

        points.append(points[0])
        return points

    def generate_inspection_mission(
        self,
        center_lat: float,
        center_lon: float,
        radius_m: float = 20.0,
    ) -> List[Dict[str, float]]:
        radius_m = max(8.0, float(radius_m))
        points: List[Dict[str, float]] = []

        for angle_deg in [0, 90, 180, 270]:
            angle = math.radians(angle_deg)
            north_m = math.cos(angle) * radius_m
            east_m = math.sin(angle) * radius_m
            points.append(self._offset_latlon(center_lat, center_lon, north_m, east_m))

        points.append(points[0])
        return points

    def generate_mission_waypoints(
        self,
        mission_type: str,
        center_lat: float,
        center_lon: float,
    ) -> List[Dict[str, float]]:
        mission_type = mission_type.lower().strip()

        if mission_type == "survey":
            return self.generate_survey_mission(center_lat, center_lon)

        if mission_type == "agriculture":
            return self.generate_agriculture_mission(center_lat, center_lon)

        if mission_type == "patrol":
            return self.generate_patrol_mission(center_lat, center_lon)

        if mission_type == "inspection":
            return self.generate_inspection_mission(center_lat, center_lon)

        return []

    def plan_segment(
        self,
        start: Dict[str, float],
        goal: Dict[str, float],
        no_fly_zones: List[Dict],
    ) -> List[Dict[str, float]]:
        lat_min, lon_min, lat_max, lon_max = self._build_bounds(start, goal, no_fly_zones)
        grid_w, grid_h = self._grid_dimensions(lat_min, lon_min, lat_max, lon_max)

        start_cell = self._world_to_grid(
            float(start["lat"]),
            float(start["lon"]),
            lat_min,
            lon_min,
            lat_max,
            lon_max,
            grid_w,
            grid_h,
        )
        goal_cell = self._world_to_grid(
            float(goal["lat"]),
            float(goal["lon"]),
            lat_min,
            lon_min,
            lat_max,
            lon_max,
            grid_w,
            grid_h,
        )

        blocked = self._build_blocked_cells(
            no_fly_zones,
            lat_min,
            lon_min,
            lat_max,
            lon_max,
            grid_w,
            grid_h,
            start_cell,
            goal_cell,
        )

        planner = AStarPlanner(grid_w, grid_h, blocked)
        cell_path = planner.plan(start_cell, goal_cell)

        if not cell_path:
            return []

        cell_path = self._smooth_cell_path(cell_path, blocked, grid_w, grid_h)

        world_path = [
            self._grid_to_world(cell, lat_min, lon_min, lat_max, lon_max, grid_w, grid_h)
            for cell in cell_path
        ]

        return self._compress_path(world_path)

    def plan_path(
        self,
        start: Dict[str, float],
        waypoints: List[Dict[str, float]],
        no_fly_zones: List[Dict],
    ) -> List[Dict[str, float]]:
        if not waypoints:
            return []

        full_path: List[Dict[str, float]] = []
        current = {"lat": float(start["lat"]), "lon": float(start["lon"])}

        for wp in waypoints:
            segment = self.plan_segment(current, wp, no_fly_zones)

            if not segment:
                return []

            if full_path:
                full_path.extend(segment[1:])
            else:
                full_path.extend(segment)

            current = {"lat": float(wp["lat"]), "lon": float(wp["lon"])}

        return full_path