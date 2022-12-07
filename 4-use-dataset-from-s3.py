import os
from clearml import Dataset

ds_dir = os.path.join(os.getcwd(), "data/saved_datasets")


# Specify which dataset you want to use
ds = Dataset.get(
    dataset_name="secret_dataset",
    dataset_version="2.0",
    output_uri=f"s3://{bucket_name}/clearml_datasets",
)


print("Dataset Information")
for k, v in ds.file_entries_dict.items():
    print(f"{k}:")
    for a, b in v.__dict__.items():
        print(f"\t {a} -> {b}")


# Download a local copy of the Dataset
if ds.list_files()[0] not in os.listdir(ds_dir):
    ds.get_mutable_local_copy(ds_dir)

print("\nFiles Downloaded:")
for file in os.listdir(ds_dir):
    print(f"\t{file}")
print("\n")
