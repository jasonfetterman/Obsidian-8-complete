import heapq
import math


class PathPlanner:
    def __init__(self):
        # Grid settings
        self.grid_size = 50
        self.resolution = 0.2  # meters per cell

        # Occupancy grid (0 = free, 1 = obstacle)
        self.grid = [[0 for _ in range(self.grid_size)] for _ in range(self.grid_size)]

        # Goal (set externally)
        self.goal = {"x": 5.0, "y": 5.0}

    # =========================
    # PUBLIC INTERFACE
    # =========================
    def set_goal(self, x, y):
        self.goal = {"x": x, "y": y}

    def update_obstacles(self, obstacle_points):
        """
        obstacle_points = [(x, y), ...]
        """
        # Reset grid
        self.grid = [[0 for _ in range(self.grid_size)] for _ in range(self.grid_size)]

        for ox, oy in obstacle_points:
            gx, gy = self._world_to_grid(ox, oy)
            if self._in_bounds(gx, gy):
                self.grid[gx][gy] = 1

    def compute_path(self, state):
        start = self._world_to_grid(state["x"], state["y"])
        goal = self._world_to_grid(self.goal["x"], self.goal["y"])

        path = self._a_star(start, goal)

        if not path:
            return []

        # Convert back to world coords
        return [self._grid_to_world(p[0], p[1]) for p in path]

    # =========================
    # A* IMPLEMENTATION
    # =========================
    def _a_star(self, start, goal):
        open_set = []
        heapq.heappush(open_set, (0, start))

        came_from = {}
        g_score = {start: 0}

        while open_set:
            _, current = heapq.heappop(open_set)

            if current == goal:
                return self._reconstruct_path(came_from, current)

            for neighbor in self._neighbors(current):
                tentative_g = g_score[current] + 1

                if neighbor not in g_score or tentative_g < g_score[neighbor]:
                    g_score[neighbor] = tentative_g
                    f = tentative_g + self._heuristic(neighbor, goal)
                    heapq.heappush(open_set, (f, neighbor))
                    came_from[neighbor] = current

        return []

    def _neighbors(self, node):
        x, y = node
        dirs = [(1,0), (-1,0), (0,1), (0,-1)]

        results = []
        for dx, dy in dirs:
            nx, ny = x + dx, y + dy
            if self._in_bounds(nx, ny) and self.grid[nx][ny] == 0:
                results.append((nx, ny))
        return results

    def _heuristic(self, a, b):
        return abs(a[0] - b[0]) + abs(a[1] - b[1])

    def _reconstruct_path(self, came_from, current):
        path = [current]
        while current in came_from:
            current = came_from[current]
            path.append(current)
        path.reverse()
        return path

    # =========================
    # UTILITIES
    # =========================
    def _world_to_grid(self, x, y):
        gx = int(x / self.resolution)
        gy = int(y / self.resolution)
        return gx, gy

    def _grid_to_world(self, gx, gy):
        return {
            "x": gx * self.resolution,
            "y": gy * self.resolution
        }

    def _in_bounds(self, x, y):
        return 0 <= x < self.grid_size and 0 <= y < self.grid_size
