# object_tracking.py
# OBSIDIAN-8 V3 — REV D
# Tracks objects in video frames over time, assigns unique IDs

import numpy as np
from collections import OrderedDict
from scipy.spatial import distance as dist

class ObjectTracker:
    def __init__(self, max_disappeared=10):
        """
        max_disappeared: number of frames an object can disappear before removal
        """
        self.next_object_id = 0
        self.objects = OrderedDict()       # object_id -> centroid
        self.disappeared = OrderedDict()   # object_id -> frames disappeared
        self.max_disappeared = max_disappeared

    def register(self, centroid):
        self.objects[self.next_object_id] = centroid
        self.disappeared[self.next_object_id] = 0
        self.next_object_id += 1

    def deregister(self, object_id):
        del self.objects[object_id]
        del self.disappeared[object_id]

    def update(self, rects):
        """
        rects: list of bounding boxes [(startX, startY, endX, endY)]
        """
        if len(rects) == 0:
            # mark existing objects as disappeared
            for object_id in list(self.disappeared.keys()):
                self.disappeared[object_id] += 1
                if self.disappeared[object_id] > self.max_disappeared:
                    self.deregister(object_id)
            return self.objects

        # compute centroids
        input_centroids = np.zeros((len(rects), 2), dtype="int")
        for (i, (startX, startY, endX, endY)) in enumerate(rects):
            cX = int((startX + endX) / 2.0)
            cY = int((startY + endY) / 2.0)
            input_centroids[i] = (cX, cY)

        # if no objects, register all
        if len(self.objects) == 0:
            for centroid in input_centroids:
                self.register(centroid)
        else:
            object_ids = list(self.objects.keys())
            object_centroids = list(self.objects.values())

            # compute distance between each pair
            D = dist.cdist(np.array(object_centroids), input_centroids)
            rows = D.min(axis=1).argsort()
            cols = D.argmin(axis=1)[rows]

            used_rows, used_cols = set(), set()
            for (row, col) in zip(rows, cols):
                if row in used_rows or col in used_cols:
                    continue
                object_id = object_ids[row]
                self.objects[object_id] = input_centroids[col]
                self.disappeared[object_id] = 0
                used_rows.add(row)
                used_cols.add(col)

            # check unmatched objects
            unused_rows = set(range(D.shape[0])) - used_rows
            for row in unused_rows:
                object_id = object_ids[row]
                self.disappeared[object_id] += 1
                if self.disappeared[object_id] > self.max_disappeared:
                    self.deregister(object_id)

            # check unmatched input centroids
            unused_cols = set(range(D.shape[1])) - used_cols
            for col in unused_cols:
                self.register(input_centroids[col])

        return self.objects

# -------------------- TEST LOOP --------------------
if __name__ == "__main__":
    tracker = ObjectTracker(max_disappeared=5)
    # simulate bounding boxes over frames
    frames = [
        [(30,30,60,60), (200,200,230,230)],
        [(32,32,62,62), (202,202,232,232)],
        [(34,34,64,64)],
        []
    ]

    for i, rects in enumerate(frames):
        objects = tracker.update(rects)
        print(f"Frame {i}: {objects}")
