import os, gc

from tools import measure


class Parent:
    def __init__(self, output: str, do_freeze: bool):
        self._output = output
        self._do_freeze = do_freeze

    def set_freeze(self, do_freeze: bool):
        self._do_freeze = do_freeze
        return self

    def do_linear_regression(self, min=0, max=100):
        import numpy as np
        from sklearn.linear_model import LinearRegression


        pid = os.fork()
        
        if pid:
            os.waitpid(pid, 0)
        else:
            print("TODO: linear regression in child proc")
            os._exit(0)

    def do_reduce(self, min=0, max=50, n=10000):
        import numpy as np

        array = np.random.uniform(low=min, high=max, size=(n,))

        def f(arr):
            return np.sum(arr)

        if self._do_freeze:
            gc.freeze()

        pid = os.fork()

        if pid:
            os.waitpid(pid, 0)
            gc.unfreeze()
        else:
            res = measure(f, self._output, 'reduction', self._do_freeze)(array)
            print(res)
            os._exit(0)


