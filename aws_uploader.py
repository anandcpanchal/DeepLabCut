import boto3
from botocore.config import Config
from botocore.exceptions import ClientError

import os
import sys
import threading

class AWS_Uploader:

    class ProgressPercentage(object):

        def __init__(self, filename):
            self._filename = filename
            self._size = float(os.path.getsize(filename))
            self._seen_so_far = 0
            self._lock = threading.Lock()

        def __call__(self, bytes_amount):
            # To simplify, assume this is hooked up to a single filename
            with self._lock:
                self._seen_so_far += bytes_amount
                percentage = (self._seen_so_far / self._size) * 100
                sys.stdout.write(
                    "\r%s  %s / %s  (%.2f%%)" % (
                        self._filename, self._seen_so_far, self._size,
                        percentage))
                sys.stdout.flush()

    def __init__(self, bucket=None):
        # Let's use Amazon S3
        self.s3 = boto3.resource('s3')
        self.bucket = bucket

    def set_bucket(self, bucket):
        self.bucket = bucket

    def get_all_buckets(self):
        for bucket in self.s3.buckets.all():
            print(bucket.name)

    def upload_file(self, filename, id):
        if self.bucket is None:
            print(" Please Set bucket name ")
            return
        try:
            filepath = str(id) + '/' + filename
            self.s3.Bucket(self.bucket).upload_file(Filename=filename, Key=filepath,
                                               Callback= self.ProgressPercentage(filename))
        except ClientError:
            print("Error Uploading file : ", filename)
            exit()

if __name__ == '__main__':
    print("Executing AWS Uploader test")
    AWS_Uploader().get_all_buckets()
    instance = AWS_Uploader(bucket='phy-exercise-analysis')
    # instance.upload_file('testFile', id=123456)