import os
import pickle
import keras
import tensorflow as tf
from clearml import Task, InputModel, Logger
from dotenv import load_dotenv

load_dotenv(".env")

# set checking clearml web server
MODEL_ID = os.environ["model_id"]

task = Task.init(
    project_name="Super Secret Project", task_name="Train Black Box Model"
)
logger = Logger.current_logger()

# Load saved Dataset
ds_dir = os.path.join(os.getcwd(), "data/saved_datasets")
ds_file_path = os.path.join(ds_dir, "secret_dataset.pickle")
with open(ds_file_path, "rb") as f:
    secret_dataset = pickle.load(f)

x_test = secret_dataset["x_test"]
y_test = secret_dataset["y_test"]

# Load Saved Model
task_input_model = InputModel(MODEL_ID)
model = keras.models.load_model(task_input_model.get_local_copy())

# Evaluate to Check if it works
accuracy = model.evaluate(x_test, y_test)

logger.report_single_value("Loss", accuracy[0])
logger.report_single_value("Accuracy", accuracy[1])
