# map_manager.py
# OBSIDIAN-8 V3 — REV D
# Manages persistent world and city maps for autonomous navigation

import numpy as np
import os
import threading
import time

class MapManager:
    def __init__(self, map_dir="maps/world", grid_size=4000, resolution=0.05):
        """
        map_dir: directory to store maps
        grid_size: number of cells per axis (e.g., 4000x4000)
        resolution: meters per cell
        """
        self.map_dir = map_dir
        os.makedirs(map_dir, exist_ok=True)
        self.grid_size = grid_size
        self.resolution = resolution
        self.lock = threading.Lock()

        # Initialize empty occupancy grid (0: free, 1: occupied, -1: unknown)
        self.occupancy_grid = np.full((grid_size, grid_size), -1, dtype=np.int8)

        # Autosave thread
        self.running = True
        self.autosave_thread = threading.Thread(target=self._autosave_loop)
        self.autosave_thread.start()

    def load_map(self, filename):
        path = os.path.join(self.map_dir, filename)
        if os.path.exists(path):
            self.occupancy_grid = np.load(path)
            print(f"[MapManager] Loaded map: {filename}")
        else:
            print(f"[MapManager] Map file not found, starting new grid.")

    def save_map(self, filename):
        path = os.path.join(self.map_dir, filename)
        with self.lock:
            np.save(path, self.occupancy_grid)
        print(f"[MapManager] Map saved: {filename}")

    def update_cell(self, x_m, y_m, value):
        """
        Update occupancy grid cell based on world coordinates in meters
        value: 0=free, 1=occupied
        """
        x_idx = int(x_m / self.resolution + self.grid_size // 2)
        y_idx = int(y_m / self.resolution + self.grid_size // 2)
        if 0 <= x_idx < self.grid_size and 0 <= y_idx < self.grid_size:
            with self.lock:
                self.occupancy_grid[y_idx, x_idx] = value

    def query_cell(self, x_m, y_m):
        x_idx = int(x_m / self.resolution + self.grid_size // 2)
        y_idx = int(y_m / self.resolution + self.grid_size // 2)
        if 0 <= x_idx < self.grid_size and 0 <= y_idx < self.grid_size:
            with self.lock:
                return self.occupancy_grid[y_idx, x_idx]
        return -1  # unknown

    def _autosave_loop(self):
        while self.running:
            self.save_map("autosave.npy")
            time.sleep(30)  # save every 30 seconds

    def shutdown(self):
        self.running = False
        self.autosave_thread.join()
        self.save_map("final_map.npy")
        print("[MapManager] Shutdown complete, map saved.")


# -------------------- TEST LOOP --------------------
if __name__ == "__main__":
    manager = MapManager()
    try:
        # Simulate robot moving in environment
        for x in np.linspace(-5, 5, 50):
            for y in np.linspace(-5, 5, 50):
                # Random obstacles
                if (x**2 + y**2) < 10:
                    manager.update_cell(x, y, 1)
                else:
                    manager.update_cell(x, y, 0)
        print("Map updated.")
    finally:
        manager.shutdown()
