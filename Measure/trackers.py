import gc
import os
import json
import time
import random


class ObjectTracker:
    def __init__(self, path='objects.json'):
        self._path = path

        self._store = []

    def __map_typenames__(self, objects):
        d = {}
        for o in objects:
            name = type(o).__name__
            if name in d:
                d[name] += 1
            else:
                d[name] = 1
        return d

    def __map_typemods__(self, objects):
        d = {}
        for o in objects:
            name = type(o).__module__
            if name in d:
                d[name] += 1
            else:
                d[name] = 1
        return d
    
    def snapshot(self):
        t = time.time()
        raw = gc.get_objects()
        raw_cnt = len(raw)
        #raw_ids = [id(o) for o in raw]
        raw_typemods = self.__map_typemods__(raw)
        raw_typenames = self.__map_typenames__(raw)

        self._store.append({
            'timestamp': t,
            'raw_count': raw_cnt,
            #'raw_ids': raw_ids,
            'raw_types': raw_typenames,
            'raw_mods': raw_typemods,
        })

    def save(self):
        with open(self._path, 'w') as file:
            json.dump(self._store, file, indent=4)


class GCTracker:
    def __init__(self, path='gc.csv'):
        self._path = path
        self._id = random.randint(10000, 99999)

        self._start = None
        self._count = 0  # number of times gc is triggered
        self._total = 0  # total time taken by collection

    def start(self):
        self._start = time.time()

    def stop(self):
        assert self._start is not None, 'Must start GCTracker before stopping it'

        self._count += 1
        self._total += time.time() - self._start
        self._start = None

    def save(self):
        import csv

        d = {
            'id'        : [self._id],
            'count'     : [self._count],
            'total_time': [self._total],
            'avg_time'  : [self._total / self._count],
        }

        with open(self._path, 'a', newline='') as csv_file:
            writer = csv.DictWriter(csv_file, fieldnames=d.keys())
            if not os.path.exists(self._path):
                writer.writeheader()
            for row in zip(*d.values()):
                writer.writerow(dict(zip(d.keys(), row)))


gc_tracker = GCTracker(path='../Results/gc.csv')
obj_tracker = ObjectTracker(path='../Results/objects.json')

def track_callback(phase, info):
    if phase == 'start':
        gc_tracker.start()
    else:
        gc_tracker.stop()

