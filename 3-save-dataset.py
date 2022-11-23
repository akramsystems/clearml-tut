import tensorflow as tf
from clearml import Dataset
import os
import pickle


ds = Dataset.create(
    dataset_name="secret_dataset",
    dataset_project="dataset project",
    dataset_version="1.0",
    description="do not show this dataset anyone <>_<>",
)

# Load and Prepare Dataset
mnist = tf.keras.datasets.mnist
(x_train, y_train), (x_test, y_test) = mnist.load_data()
x_train, x_test = x_train / 255.0, x_test / 255.0

secret_dataset = {
    "x_train": x_train,
    "y_train": y_train,
    "x_test": x_test,
    "y_test": y_test,
}


# Save Data Locally (NOT SECURE)
data_dir = os.path.join(os.getcwd(), "data")
pickle_file_path = os.path.join(data_dir, "secret_dataset.pickle")
with open(pickle_file_path, "wb") as f:
    pickle.dump(secret_dataset, f, pickle.HIGHEST_PROTOCOL)

# Attach files you want to uploaded to our dataset
# ds.add_external_files(source_url="s3://bucket/folder/path")
ds.add_files(pickle_file_path)

# Upload and Publish (finalize)
ds.finalize(auto_upload=True)
