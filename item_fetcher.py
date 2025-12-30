import os

import boto3
from botocore.exceptions import ClientError

from utils.logs import LOGGER


class S3ItemFetcher:
    def __init__(self, bucket_name: str, base_prefix: str):
        """
        :param bucket_name: S3 bucket name
        :param base_prefix: Base folder containing date-folders (e.g., 'logs/')
        """
        self.s3 = boto3.client("s3")
        self.bucket = bucket_name
        self.base_prefix = base_prefix

    def list_files_for_date(self):
        try:
            response = self.s3.list_objects_v2(Bucket=self.bucket, Prefix=self.base_prefix)
        except ClientError as e:
            raise RuntimeError(f"S3 error: {e}")

        if "Contents" not in response:
            return []
        all_objects = [obj["Key"] for obj in response["Contents"]]
        LOGGER.info(f"Found {len(all_objects)} files for date: {self.base_prefix}")
        LOGGER.info(f"List of files: {all_objects}")
        yield from all_objects

    def parse_file(self, key: str):
        """
        Override this method depending on your file type.
        Here we simply return the file content as text.
        """
        obj = self.s3.get_object(Bucket=self.bucket, Key=key)
        LOGGER.info(f"Parsing {key}")
        return obj["Body"].read().decode("utf-8")

    def parse_files_for_date(self):
        """
        Main method: lists and parses all files for a specific date.
        Returns mapping {filename -> parsed content}.
        """
        files = self.list_files_for_date()
        results = {}

        for key in files:
            try:
                results[key] = self.parse_file(key)
            except Exception as e:
                results[key] = f"ERROR reading file: {e}"

        return results

    def download_file(self, key: str, local_path: str):
        """
        Download a file from S3 to a local path.

        :param key: Full S3 object key
        :param local_path: Path on local filesystem
        """
        try:
            os.makedirs(os.path.dirname(local_path), exist_ok=True)
            self.s3.download_file(self.bucket, key, local_path)
        except ClientError as e:
            raise RuntimeError(f"Failed to download {key}: {e}")

        return local_path
