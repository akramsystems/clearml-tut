import tensorflow as tf
import clearml
from clearml import Logger
import os
import pickle
from dotenv import load_dotenv


load_dotenv(".env")
bucket_name = os.environ["s3_bucket_name"]

# # LOAD DATASET
ds_dir = os.path.join(os.getcwd(), "data/saved_datasets")
ds_file_path = os.path.join(ds_dir, "secret_dataset.pickle")

with open(ds_file_path, "rb") as f:
    secret_dataset = pickle.load(f)

x_train = secret_dataset["x_train"]
y_train = secret_dataset["y_train"]
x_test = secret_dataset["x_test"]
y_test = secret_dataset["y_test"]


task = clearml.Task.init(
    project_name="Super Secret Project",
    task_name="Train Black Box Model",
    output_uri=f"s3://{bucket_name}/clearml-datasets/"
)
params = {"epochs": 20, "hidden_layer_dim": 128}

# track the parameters for this experiment
task.connect(params)

logger = Logger.current_logger()

# # Create Model
model = tf.keras.models.Sequential(
    [
        tf.keras.layers.Flatten(input_shape=(28, 28)),
        tf.keras.layers.Dense(params["hidden_layer_dim"], activation="relu"),
        tf.keras.layers.Dropout(0.2),
        tf.keras.layers.Dense(10),
    ]
)
loss_fn = tf.keras.losses.SparseCategoricalCrossentropy(from_logits=True)
model.compile(optimizer="adam", loss=loss_fn, metrics=["accuracy"])

history = model.fit(
    x_train, y_train, validation_data=(x_test, y_test),
    epochs=params["epochs"]
)

scores = model.evaluate(x_test, y_test)

acc = history.history["accuracy"]
loss = history.history["loss"]
val_acc = history.history["val_accuracy"]
val_loss = history.history["val_loss"]

for i, v in enumerate(acc):
    Logger.current_logger().report_scalar(
        "Accuracy", "Training", iteration=i, value=v)
    Logger.current_logger().report_scalar(
        "Accuracy", "Validation", iteration=i, value=val_acc[i]
    )
    Logger.current_logger().report_scalar(
        "Loss", "Training", iteration=i, value=loss[i]
    )
    Logger.current_logger().report_scalar(
        "Loss", "Validation", iteration=i, value=val_loss[i]
    )


logger.report_single_value("final_accuracy", scores[1])

# Save Model
model.save("model/my_model.h5", save_format="h5")
# tf.saved_model.save(model, export_dir="model/mnist")
