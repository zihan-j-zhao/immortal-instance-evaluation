def to_int(f):
    def wrapper():
        return int(f())
    return wrapper


class Stats:
    def __init__(self, utime=None, stime=None, cutime=None, cstime=None,
                 min_flt=None, maj_flt=None, cmin_flt=None, cmaj_flt=None,
                 vsz=None, rss=None):
        self._utime    = utime
        self._stime    = stime
        self._cutime   = cutime
        self._cstime   = cstime
        self._min_flt  = min_flt
        self._maj_flt  = maj_flt
        self._cmin_flt = cmin_flt
        self._cmaj_flt = cmaj_flt
        self._vsz      = vsz
        self._rss      = rss

        self._verbose = False

    def __str__(self):
        if not self._verbose:
            return f"{self._utime}, {self._stime}, {self._cutime}, " + \
                   f"{self._cstime}, {self._min_flt}, {self._maj_flt}, " + \
                   f"{self._cmin_flt}, {self._cmaj_flt}, {self._vsz}, {self._rss}"
        else:
            return f"utime={self._utime}, stime={self._stime}, cutime={self._cutime}, " + \
                   f"cstime={self._cstime}, min_flt={self._min_flt}, maj_flt={self._maj_flt}, " + \
                   f"cmin_flt={self._cmin_flt}, cmaj_flt={self._cmaj_flt}, vsz={self._vsz}, rss={self._rss}"

    def __repr__(self):
        if not self._verbose:
            return f"{self._utime}, {self._stime}, {self._cutime}, " + \
                   f"{self._cstime}, {self._min_flt}, {self._maj_flt}, " + \
                   f"{self._cmin_flt}, {self._cmaj_flt}, {self._vsz}, {self._rss}"
        else:
            return f"utime={self._utime}, stime={self._stime}, cutime={self.cutime}, " + \
                   f"cstime={self._cstime}, min_flt={self._min_flt}, maj_flt={self._maj_flt}, " + \
                   f"cmin_flt={self._cmin_flt}, cmaj_flt={self._cmaj_flt}, vsz={self._vsz}, rss={self._rss}"

    def set_verbose(self, verbose: bool):
        self._verbose = verbose
        return self

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


def export_stats(pid: int) -> Stats:
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
        )


def print_stats(pid: int) -> None:
    with open(f'/proc/{pid}/stat', 'r') as f:
        print(f.readline())


