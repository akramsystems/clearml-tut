## clearml-tutorial

This Repository has scripts to help learn how to integrate use ClearML in your machine learning experiments, please make sure to setup clearml by running `clearml-init`, and providing your credentials. This should generate a file in your home directory i.e. `~/clearml.conf`.

#### Requirements

- tensorflow 2.x
- clearml 1.7.2
- boto3 # for uploading to s3

---

### How to Set default output directory as s3

To set the default storage location update your `~/clearml.conf` file by adding the following

```
.
.
sdk {
    aws {
        s3 {
            region: "${AWS_REGION}"
            key: "${AWS_ACCESS_KEY_ID}"
            secret: "${AWS_SECRET_ACCESS_KEY}"
        }
    }
    ...
    development {
        default_output_uri: "s3://{BUCKET_NAME}/clearml"
    }
}
.
.
```
