import os, gc 


def to_int(f):
    def wrapper():
        return int(f())
    return wrapper


class Stats:
    def __init__(self, utime=None, stime=None, cutime=None, cstime=None,
                 min_flt=None, maj_flt=None, cmin_flt=None, cmaj_flt=None,
                 vsz=None, rss=None, gen_count=None, perm_count=None, 
                 is_freezed=False, verbose=False, timept=0, category='default'):
        self._utime      = utime
        self._stime      = stime
        self._cutime     = cutime
        self._cstime     = cstime
        self._min_flt    = min_flt
        self._maj_flt    = maj_flt
        self._cmin_flt   = cmin_flt
        self._cmaj_flt   = cmaj_flt
        self._vsz        = vsz
        self._rss        = rss
        self._gen_count  = gen_count
        self._perm_count = perm_count

        # metadata
        self._is_freezed = is_freezed
        self._verbose    = verbose
        self._timept     = timept
        self._category   = category

    def set_is_freezed(self, is_freezed: bool):
        self._is_freezed = is_freezed
        return self

    def set_verbose(self, verbose: bool):
        self._verbose = verbose
        return self

    def set_timept(self, timept: int):
        self._timept = timept
        return self

    def set_category(self, category: str):
        self._category = category
        return self

    def get_category(self) -> str:
        return self._category

    @to_int
    def get_min_flt(self):
        return self._min_flt

    @to_int
    def get_maj_flt(self):
        return self._maj_flt

    @to_int
    def get_children_min_flt(self):
        return self._cmin_flt
    
    @to_int
    def get_children_max_flt(self):
        return self._cmax_flt

    @to_int
    def get_user_time(self):
        return self._utime

    @to_int
    def get_sys_time(self):
        return self._stime

    @to_int
    def get_children_user_time(self):
        return self._cutime

    @to_int
    def get_children_sys_time(self):
        return self._cstime

    def get_gen_count(self):
        return self._gen_count

    @to_int
    def get_perm_count(self):
        return self._perm_count

    def __str__(self):
        if not self._verbose:
            return f"{self._timept}, {self._category}, {self._is_freezed}, " + \
                   f"{self._utime}, {self._stime}, {self._cutime}, " + \
                   f"{self._cstime}, {self._min_flt}, {self._maj_flt}, " + \
                   f"{self._cmin_flt}, {self._cmaj_flt}, {self._vsz}, " + \
                   f"{self._rss}, {self._gen_count[0]}, {self._gen_count[1]}, " + \
                   f"{self._gen_count[1]}, {self._perm_count}\n"
        else:
            return f"timept={self._timept}, category={self._category}, " + \
                   f"is_freezed={self._is_freezed}, " + \
                   f"utime={self._utime}, stime={self._stime}, " + \
                   f"cutime={self._cutime}, cstime={self._cstime}, " + \
                   f"min_flt={self._min_flt}, maj_flt={self._maj_flt}, " + \
                   f"cmin_flt={self._cmin_flt}, cmaj_flt={self._cmaj_flt}, " + \
                   f"vsz={self._vsz}, rss={self._rss}, gen_count={self._gen_count}, " + \
                   f"perm_count={self._perm_count}\n"

    def __repr__(self):
        if not self._verbose:
            return f"{self._timept}, {self._category}, {self._is_freezed}, " + \
                   f"{self._utime}, {self._stime}, {self._cutime}, " + \
                   f"{self._cstime}, {self._min_flt}, {self._maj_flt}, " + \
                   f"{self._cmin_flt}, {self._cmaj_flt}, {self._vsz}, " + \
                   f"{self._rss}, {self._gen_count[0]}, {self._gen_count[1]}, " + \
                   f"{self._gen_count[1]}, {self._perm_count}\n"
        else:
            return f"timept={self._timept}, category={self._category}, " + \
                   f"is_freezed={self._is_freezed}, " + \
                   f"utime={self._utime}, stime={self._stime}, " + \
                   f"cutime={self._cutime}, cstime={self._cstime}, " + \
                   f"min_flt={self._min_flt}, maj_flt={self._maj_flt}, " + \
                   f"cmin_flt={self._cmin_flt}, cmaj_flt={self._cmaj_flt}, " + \
                   f"vsz={self._vsz}, rss={self._rss}, gen_count={self._gen_count}, " + \
                   f"perm_count={self._perm_count}\n"


def read_stats(pid: int) -> Stats:
    gen_count = gc.get_count()
    perm_count = gc.get_freeze_count()

    with open(f'/proc/{pid}/stat', 'r') as f:
        info = f.readline().split(' ')
        return Stats(
            min_flt  = info[9],     # CoW
            cmin_flt = info[10],    # CoW
            maj_flt  = info[11],    # CoW
            cmaj_flt = info[12],    # CoW
            utime    = info[13],    # Exe time
            stime    = info[14],    # Exe time
            cutime   = info[15],    # Exe time
            cstime   = info[16],    # Exe time
            vsz      = info[22],    # Mem usage
            rss      = info[23],    # Mem usage
            gen_count = gen_count,  # GC
            perm_count = perm_count,# GC
        )


def print_stats(pid: int) -> None:
    with open(f'/proc/{pid}/stat', 'r') as f:
        print(f.readline())


def export_stats(stats: Stats, path: str) -> None:
    if not os.path.exists(path):
        with open(path, 'w') as f:
            f.write('timept, category, freeze, utime, stime, cutime, cstime, ' +
                    'min_flt, maj_flt, cmin_flt, cmaj_flt, vsz, rss, gen0, ' +
                    'gen1, gen2, perm\n')

    with open(path, 'a') as f:
        f.write(str(stats))


def measure(func, path, category, is_freezed):
    def wrapper(*args, **kwargs):
        begin = read_stats(os.getpid())\
                .set_category(category)\
                .set_is_freezed(is_freezed)

        # ========== BEGIN CORE FUNCTION ========== #
        res = func(*args, **kwargs)
        # ========== END CORE FUNCTION ========== #

        end = read_stats(os.getpid())\
                .set_category(category)\
                .set_timept(1)\
                .set_is_freezed(is_freezed)

        export_stats(begin, path)
        export_stats(end, path)
        return res
    return wrapper

