# pylint:disable=abstract-method
import os
import uuid

from dvc.testing.cloud import Cloud
from dvc.testing.path_info import CloudURLInfo

TEST_OSS_ENDPOINT = "oss-us-east-1.aliyuncs.com"
TEST_OSS_REPO_BUCKET = "dvc-test-github"


class OSS(Cloud, CloudURLInfo):

    IS_OBJECT_STORAGE = True

    @staticmethod
    def get_url():
        return f"oss://{TEST_OSS_REPO_BUCKET}/{uuid.uuid4()}"

    @property
    def config(self):
        return {
            "url": self.url,
            "oss_key_id": os.environ.get("OSS_ACCESS_KEY_ID"),
            "oss_key_secret": os.environ.get("OSS_ACCESS_KEY_SECRET"),
            "oss_endpoint": TEST_OSS_ENDPOINT,
        }

    def is_file(self):
        raise NotImplementedError

    def is_dir(self):
        raise NotImplementedError

    def exists(self):
        raise NotImplementedError

    def mkdir(self, mode=0o777, parents=False, exist_ok=False):
        raise NotImplementedError

    def write_bytes(self, contents):
        raise NotImplementedError

    def read_bytes(self):
        raise NotImplementedError

    def unlink(self, missing_ok: bool = False) -> None:
        raise NotImplementedError

    def rmdir(self, recursive: bool = True) -> None:
        raise NotImplementedError
