class Invoker:
    def __init__(self, packages, out_dir='../Results/', freeze=False, collect=False):
        assert type(packages) == list, 'Expect packages to be a list of names (strings)'
        assert all(isinstance(e, str) for e in packages), 'Expect packages to be a list of names (strings)'
        assert type(freeze) == bool, 'Expect freeze to be a bool'
        assert type(collect) == bool, 'Expect collect to be a bool'

        self._packages          = packages
        self._freeze            = freeze
        self._collect           = collect
        self._out_dir           = out_dir
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
        self._pkg_load_time     = []
        self._execution_time    = []

    def run(self, func, event=None):
        self._name = func.__name__[3:]

        import os
        import gc
        import time
        import importlib

        for pkg in self._packages:
            importlib.import_module(pkg)

        if self._collect:
            gc.collect()

        if self._freeze:
            gc.freeze()

        pid = os.fork()

        if not pid:
            self.mem_snapshot(desc='child start')

            t0 = time.time()
            for pkg in self._packages:
                importlib.import_module(pkg)
            self._pkg_load_time.append(time.time() - t0)

            self.mem_snapshot(desc='before lambda')

            t0 = time.time()
            res = func(event)
            self._execution_time.append(time.time() - t0)

            self.mem_snapshot(desc='after lambda')
            self.persist()
            print(res)
        else:
            os.waitpid(pid, 0)
            if self._freeze:
                gc.unfreeze()

    def mem_snapshot(self, desc=None):
        import gc
        import os

        self._mem_ord.append(0 if len(self._mem_ord) == 0 else self._mem_ord[-1] + 1)
        self._mem_desc.append(desc)
        self._gen_count.append(gc.get_count())
        self._perm_count.append(gc.get_freeze_count())

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
            'packages': [self._packages] * n,
            'freeze': [self._freeze] * n,
            'collect': [self._collect] * n,

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
            'packages'          : [self._packages] * n,
            'freeze'            : [self._freeze] * n,
            'collect'           : [self._collect] * n,
            'pkg_load_time'     : self._pkg_load_time,
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
