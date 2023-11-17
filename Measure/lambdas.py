from invoker import Invoker


def invoke(func_name, **kwargs):

    for name, func, packages in functions:
        if name == func_name:
            return Invoker(packages, **kwargs).run(func)

    raise ValueError(f"Unknown lambda function name: {func_name}")


# ==================================================================
# DEFINE LAMBDA FUNCTIONS BELOW AND ADD TO DICTIONARY AT THE BOTTOM
# ==================================================================

def do_reduction(event=None):
    return


def do_linear_regression(event=None):
    import pandas as pd
    from sklearn.model_selection import train_test_split
    from sklearn.linear_model import LinearRegression
    from sklearn.metrics import mean_squared_error, r2_score

    path = './Experience-Salary.csv'
    data = pd.read_csv(path)

    X = data['exp(in months)'].values.reshape(-1, 1)
    y = data['salary(in thousands)'].values
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=0)

    model = LinearRegression()
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)

    mse = mean_squared_error(y_test, y_pred)
    r2 = r2_score(y_test, y_pred)

    return mse, r2


functions = [
    ('reduction', do_reduction, []),
    ('linear_regression', do_linear_regression, ['pandas', 'sklearn']),

    # add more experiments down here
]
