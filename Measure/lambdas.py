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


def do_image_classification(event=None):
    import tensorflow as tf

    (train_images, train_labels), (test_images, test_labels) = tf.keras.datasets.cifar10.load_data()
    train_images, test_images = train_images / 255.0, test_images / 255.0
    model = tf.keras.models.Sequential([
        tf.keras.layers.Conv2D(32, (3, 3), activation='relu', input_shape=(32, 32, 3)),
        tf.keras.layers.MaxPooling2D((2, 2)),
        tf.keras.layers.Conv2D(64, (3, 3), activation='relu'),
        tf.keras.layers.MaxPooling2D((2, 2)),
        tf.keras.layers.Conv2D(64, (3, 3), activation='relu'),
        tf.keras.layers.Flatten(),
        tf.keras.layers.Dense(64, activation='relu'),
        tf.keras.layers.Dense(10)
    ])

    model.compile(optimizer='adam',
                  loss=tf.keras.losses.SparseCategoricalCrossentropy(from_logits=True),
                  metrics=['accuracy'])

    model.fit(train_images, train_labels, epochs=3,
              validation_data=(test_images, test_labels))

    test_loss, test_acc = model.evaluate(test_images, test_labels, verbose=2)

    return test_loss, test_acc


functions = [
    ('reduction', do_reduction, []),
    ('linear_regression', do_linear_regression, ['pandas', 'sklearn']),
    ('image_classification', do_image_classification, ['tensorflow'])

    # add more experiments down here
]
