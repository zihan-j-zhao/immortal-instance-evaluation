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
        import pandas as pd
        from sklearn.model_selection import train_test_split
        from sklearn.linear_model import LinearRegression
        from sklearn.metrics import mean_squared_error, r2_score

        path = './Experience-Salary.csv'
        data = pd.read_csv(path)

        # ========== BEGIN LAMBDA FUNCTION ========== #
        def f(df):
            X = df['exp(in months)'].values.reshape(-1, 1)
            y = data['salary(in thousands)'].values
            X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=0)

            model = LinearRegression()
            model.fit(X_train, y_train)
            y_pred = model.predict(X_test)

            mse = mean_squared_error(y_test, y_pred)
            r2 = r2_score(y_test, y_pred)

            return mse, r2
        # ========== END LAMBDA FUNCTION ========== #

        pid = os.fork()
        
        if pid:
            os.waitpid(pid, 0)
        else:
            mse, r2 = f(data)
            print(f"mse={mse}, r2={r2}")
            os._exit(0)

    def do_reduce(self, min=0, max=50, n=10000):
        import numpy as np

        array = np.random.uniform(low=min, high=max, size=(n,))

        # ========== BEGIN LAMBDA FUNCTION ========== #
        def f(arr):
            return np.sum(arr)
        # ========== END LAMBDA FUNCTION ========== #

        if self._do_freeze:
            gc.freeze()

        pid = os.fork()

        if pid:
            os.waitpid(pid, 0)

            if self._do_freeze:
                gc.unfreeze()
        else:
            res = measure(f, self._output, 'reduction', self._do_freeze)(array)
            print(res)
            os._exit(0)


