class Invoker:
    def __init__(self, modules, out_dir='../Results/', verbose=False, 
                 enable_object_tracker=False):
        assert type(modules) == list, 'Expect modules to be a list of names (strings)'
        assert all(isinstance(e, str) for e in modules), 'Expect modules to be a list of names (strings)'
        assert type(verbose) == bool, 'Expect verbose to be a bool'

        self._modules           = modules
        self._verbose           = verbose
        self._out_dir           = out_dir
        self._ob_tracker_on     = enable_object_tracker
        self._name              = None

        # memory
        self._mem_ord           = []
        self._mem_desc          = []
        self._vsz               = []
        self._rss               = []
        self._min_flt           = []
        self._maj_flt           = []
        self._gen_count         = []
        self._perm_count        = []

        # time
        self._time_ord          = [0]
        self._immortal_time     = []
        self._mod_load_time     = []
        self._execution_time    = []

    def run(self, func, event=None):
        self._name = func.__name__[3:]

        import gc
        import os
        import sys
        import time
        import importlib

        import trackers

        if self._ob_tracker_on:
            trackers.obj_tracker.snapshot() # beginning
        # =========================
        gc.callbacks.append(trackers.track_callback)

        for mod in self._modules:
            importlib.import_module(mod)

        gc.collect() # trigger a full collection of garbage

        maj = sys.version_info.major
        min = sys.version_info.minor

        t0 = time.time()
        if maj == 3 and min == 12:
            do_immortalize(gc.get_objects(), verbose=self._verbose)
        self._immortal_time.append(time.time() - t0)
        # =========================

        gc.collect() # move immortal instances to permanent generation

        if self._ob_tracker_on:
            trackers.obj_tracker.snapshot() # after imports and immortalization

        pid = os.fork()

        if not pid:
            self.mem_snapshot(desc='child start')

            t0 = time.time()
            for mod in self._modules:
                importlib.import_module(mod)
            self._mod_load_time.append(time.time() - t0)

            self.mem_snapshot(desc='before lambda')

            t0 = time.time()
            res = func(event)
            self._execution_time.append(time.time() - t0)

            self.mem_snapshot(desc='after lambda')
            self.persist()
            print(res)
            sys.exit(0)
        else:
            os.waitpid(pid, 0)

            trackers.gc_tracker.save()
            if self._ob_tracker_on:
                trackers.obj_tracker.save()

    def mem_snapshot(self, desc=None):
        import gc
        import os

        self._mem_ord.append(0 if len(self._mem_ord) == 0 else self._mem_ord[-1] + 1)
        self._mem_desc.append(desc)
        self._gen_count.append(gc.get_count())
        self._perm_count.append(0)

        with open(f'/proc/{os.getpid()}/stat', 'r') as f:
            stats = f.readline().split(' ')
            self._vsz.append(stats[22])
            self._rss.append(stats[23])
            self._min_flt.append(stats[9])
            self._maj_flt.append(stats[11])

    def persist(self):
        import os

        # persist memory data
        n = len(self._mem_ord)

        mem_dict = {
            'ord'       : self._mem_ord,
            'desc'      : self._mem_desc,
            'lambda': [self._name] * n,
            'modules': [self._modules] * n,

            'vsz'       : self._vsz,
            'rss'       : self._rss,
            'min_flt'   : self._min_flt,
            'maj_flt'   : self._maj_flt,
            'gen0'      : [tup[0] for tup in self._gen_count],
            'gen1'      : [tup[1] for tup in self._gen_count],
            'gen2'      : [tup[2] for tup in self._gen_count],
            'perm'      : self._perm_count,
        }

        filename = self._name + '-mem.csv'
        filepath = os.path.join(self._out_dir, filename)
        new_file = not os.path.exists(filepath)
        write_csv(mem_dict, filepath, new_file)

        # persist timing data
        n = len(self._time_ord)

        time_dict = {
            'ord'               : self._time_ord,
            'lambda'            : [self._name] * n,
            'modules'           : [self._modules] * n,
            'immortal_time'     : self._immortal_time,
            'mod_load_time'     : self._mod_load_time,
            'execution_time'    : self._execution_time,
        }

        filename = self._name + '-time.csv'
        filepath = os.path.join(self._out_dir, filename)
        new_file = not os.path.exists(filepath)
        write_csv(time_dict, filepath, new_file)


def write_csv(d, filepath, new_file):
    import csv

    with open(filepath, 'a', newline='') as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=d.keys())
        if new_file:
            writer.writeheader()
        for row in zip(*d.values()):
            writer.writerow(dict(zip(d.keys(), row)))


def do_immortalize(obj, verbose=False):
    import immortal

    count, error, stats, status = immortal.immortalize_object(obj, stats=verbose)
    print(f"count={count}, error={error}, status={status}")
    if verbose:
        print(f"stats={stats}")

