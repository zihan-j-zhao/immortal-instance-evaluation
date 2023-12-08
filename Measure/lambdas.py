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


# Machine Learning
def do_linear_regression(event=None):
    import pandas as pd
    from sklearn.model_selection import train_test_split
    from sklearn.linear_model import LinearRegression
    from sklearn.metrics import mean_squared_error, r2_score

    path = './amz_us_price_prediction_dataset.csv'
    data = pd.read_csv(path)

    X = data['stars'].values.reshape(-1, 1)
    y = data['price'].values
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=0)

    model = LinearRegression()
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)

    mse = mean_squared_error(y_test, y_pred)
    r2 = r2_score(y_test, y_pred)

    return mse, r2


# Machine Learning (tensorflow not supported yet in 3.12)
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


# Image Processing
def do_grayscale(event=None):
    from PIL import Image
    import numpy as np

    original_image = Image.open('./4k_image.jpg')
    pixels = np.array(original_image)
    grayscale = pixels.mean(axis=2)
    grayscale_image = Image.fromarray(grayscale.astype('uint8'))
    grayscale_image.save('4k_grayscale.jpg')

    return 'done grayscaling 4k image'


# Image Processing
def do_edge_detection(event=None):
    from PIL import Image
    import numpy as np

    def sobel_operator(img):
        sobel_x = np.array([[1, 0, -1],
                            [2, 0, -2],
                            [1, 0, -1]])
        sobel_y = np.array([[1, 2, 1],
                            [0, 0, 0],
                            [-1, -2, -1]])
        pixels = np.arange(img)
        height, width = pixels.shape
        edge_img = np.zeros((height, width))

        for i in range(1, height - 1):
            for j in range(1, width - 1):
                g_x = np.sum(np.multiply(pixels[i - 1:i + 2, j - 1:j + 2], sobel_x))
                g_y = np.sum(np.multiply(pixels[i - 1:i + 2, j - 1:j + 2], sobel_y))
                edge_img[i, j] = np.sqrt(g_x ** 2 + g_y ** 2)

        return edge_img

    original_image = Image.open('./4k_image.jpg')
    gray_image = original_image.convert("L")
    edge_pixels = sobel_operator(gray_image)
    edge_image = Image.fromarray(edge_pixels.astype('uint8'))
    edge_image = edge_image.convert("L")
    edge_image.save('4k_edge.jpg')

    return 'done edge 4k image'


# Storage
def do_database_operations(event=None):
    from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, Table
    from sqlalchemy.ext.declarative import declarative_base
    from sqlalchemy.orm import relationship, sessionmaker

    Base = declarative_base()

    product_supplier_table = Table('product_supplier', Base.metadata,
        Column('product_id', Integer, ForeignKey('product.id')),
        Column('supplier_id', Integer, ForeignKey('supplier.id'))
    )

    class Product(Base):
        __tablename__ = 'product'
        id = Column(Integer, primary_key=True)
        name = Column(String)
        suppliers = relationship("Supplier", secondary=product_supplier_table, back_populates="products")

    class Supplier(Base):
        __tablename__ = 'supplier'
        id = Column(Integer, primary_key=True)
        name = Column(String)
        products = relationship("Product", secondary=product_supplier_table, back_populates="suppliers")

    engine = create_engine('sqlite:///inventory.db')
    Base.metadata.create_all(engine)

    session = sessionmaker(bind=engine)()

    for i in range(100):
        new_product = Product(name=f"Product {i}")
        new_supplier = Supplier(name=f"Supplier {i}")
        new_product.suppliers.append(new_supplier)
        session.add(new_product)
    session.commit()

    return 'done db operations'


functions = [
    ('reduction', do_reduction, []),
    ('linear_regression', do_linear_regression, ['pandas', 'sklearn']),
    # ('image_classification', do_image_classification, ['tensorflow']),
    ('grayscale_4k', do_grayscale, ['PIL', 'numpy']),
    ('edge_4k', do_edge_detection, ['PIL', 'numpy']),
    ('db_operations', do_database_operations, ['sqlalchemy'])

    # add more experiments down here
]
