import boto3

from config import load_config

# State files kept in S3 between runs.
STATE_FILES = ("prices-recent.json", "price-comparison-recent.json")


class FileUpload:

    def __init__(self):
        s3_config = load_config()["s3"]
        self.aws_access_key_id = s3_config["aws_access_key_id"]
        self.aws_secret_access_key = s3_config["aws_secret_access_key"]
        self.s3_bucket_name = s3_config["bucket"]

    #other_filenames should be a list of filenames. it is assumed they are in the tmp folder.
    def file_upload(self, other_filenames=None):

        s3 = boto3.client('s3', aws_access_key_id=self.aws_access_key_id,
                          aws_secret_access_key=self.aws_secret_access_key)

        for name in STATE_FILES:
            s3.upload_file("/tmp/%s" % name, self.s3_bucket_name, name)

        if other_filenames:
            for each_filename in other_filenames:
                s3.upload_file("/tmp/%s" % each_filename, self.s3_bucket_name, each_filename)
