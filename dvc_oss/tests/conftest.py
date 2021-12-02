# pylint:disable=abstract-method
import os
import uuid

import pytest
from dvc.testing.cloud import Cloud
from dvc.testing.fixtures import *  # noqa, pylint: disable=wildcard-import,unused-import
from dvc.testing.path_info import CloudURLInfo
from dvc.utils import env2bool

TEST_OSS_REPO_BUCKET = "dvc-test-github"
EMULATOR_OSS_ENDPOINT = "127.0.0.1:{port}"
EMULATOR_OSS_ACCESS_KEY_ID = "AccessKeyID"
EMULATOR_OSS_ACCESS_KEY_SECRET = "AccessKeySecret"


class OSS(Cloud, CloudURLInfo):

    IS_OBJECT_STORAGE = True

    @staticmethod
    def get_url():
        return f"oss://{TEST_OSS_REPO_BUCKET}/{uuid.uuid4()}"

    @staticmethod
    def should_test():
        do_test = env2bool("DVC_TEST_OSS", undefined=None)
        if do_test is not None:
            return do_test

        if os.getenv("OSS_ACCESS_KEY_ID") and os.getenv(
            "OSS_ACCESS_KEY_SECRET"
        ):
            return True

        return False

    @property
    def config(self):
        return {
            "url": self.url,
            "oss_key_id": os.environ.get("OSS_ACCESS_KEY_ID"),
            "oss_key_secret": os.environ.get("OSS_ACCESS_KEY_SECRET"),
            "oss_endpoint": os.environ.get("OSS_ENDPOINT"),
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


@pytest.fixture(scope="session")
def oss_server(docker_compose, docker_services):
    import oss2

    port = docker_services.port_for("oss", 8880)
    endpoint = EMULATOR_OSS_ENDPOINT.format(port=port)

    def _check():
        try:
            auth = oss2.Auth(
                EMULATOR_OSS_ACCESS_KEY_ID, EMULATOR_OSS_ACCESS_KEY_SECRET
            )
            oss2.Bucket(auth, endpoint, "mybucket").get_bucket_info()
            return True
        except oss2.exceptions.NoSuchBucket:
            return True
        except oss2.exceptions.OssError:
            return False

    docker_services.wait_until_responsive(timeout=30.0, pause=5, check=_check)

    return endpoint


@pytest.fixture
def make_real_oss():
    def _make_oss():
        import oss2

        url = OSS.get_url()
        ret = OSS(url)

        auth = oss2.Auth(
            ret.config["oss_key_id"], ret.config["oss_key_secret"]
        )
        bucket = oss2.Bucket(
            auth, ret.config["oss_endpoint"], TEST_OSS_REPO_BUCKET
        )
        try:
            bucket.get_bucket_info()
        except oss2.exceptions.NoSuchBucket:
            bucket.create_bucket(
                oss2.BUCKET_ACL_PUBLIC_READ,
                oss2.models.BucketCreateConfig(
                    oss2.BUCKET_STORAGE_CLASS_STANDARD
                ),
            )

        return ret

    return _make_oss


@pytest.fixture
def make_oss(make_real_oss):
    return make_real_oss


@pytest.fixture
def oss(real_oss):
    # FIXME: this should use emulator
    return real_oss


@pytest.fixture
def real_oss(make_real_oss):
    return make_real_oss()
