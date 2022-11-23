import tensorflow as tf

params = {
    "epochs": 5,
    "hidden_layer_dim": 128
}


mnist = tf.keras.datasets.mnist
(x_train, y_train), (x_test, y_test) = mnist.load_data()

# Data Processing
x_train, x_test = x_train / 255.0, x_test / 255.0

# Create Model
model = tf.keras.models.Sequential(
    [
        tf.keras.layers.Flatten(input_shape=(28, 28)),
        tf.keras.layers.Dense(
            params["hidden_layer_dim"], activation="relu"),
        tf.keras.layers.Dropout(0.2),
        tf.keras.layers.Dense(10),
    ]
)
loss_fn = tf.keras.losses.SparseCategoricalCrossentropy(from_logits=True)
model.compile(optimizer="adam", loss=loss_fn, metrics=["accuracy"])
model.fit(x_train, y_train, epochs=params["epochs"])
model.evaluate(x_test, y_test)

# Save Model
tf.saved_model.save(model, export_dir="model/mnist")
