import os
import pickle
import keras
import tensorflow as tf
from clearml import InputModel, Logger

logger = Logger.current_logger()

ds_dir = os.path.join(os.getcwd(), "data/saved_datasets")
# Load saved Dataset
ds_dir = os.path.join(os.getcwd(), "data/saved_datasets")
ds_file_path = os.path.join(ds_dir, "secret_dataset.pickle")
with open(ds_file_path, "rb") as f:
    secret_dataset = pickle.load(f)
x_test = secret_dataset["x_test"]
y_test = secret_dataset["y_test"]

# Load Saved Model
task_input_model = InputModel("70c1cadb66634740954373c9672c0ae3")
model = keras.models.load_model(task_input_model.get_local_copy())

# Evaluate to Check if it works
accuracy = model.evaluate(x_test, y_test)

logger.report_single_value("Accuracy", accuracy)
