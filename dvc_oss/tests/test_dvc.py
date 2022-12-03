import pytest
from dvc.testing.api_tests import (  # noqa, pylint: disable=unused-import
    TestAPI,
)
from dvc.testing.remote_tests import (  # noqa, pylint: disable=unused-import
    TestRemote,
)
from dvc.testing.workspace_tests import TestAdd as _TestAdd
from dvc.testing.workspace_tests import (  # noqa, pylint: disable=unused-import
    TestGetUrl,
)
from dvc.testing.workspace_tests import TestImport as _TestImport
from dvc.testing.workspace_tests import (  # noqa, pylint: disable=unused-import
    TestLsUrl,
)


@pytest.fixture
def remote(make_remote):
    yield make_remote(name="upstream", typ="oss")


class TestImport(_TestImport):
    @pytest.fixture
    def stage_md5(self):
        raise NotImplementedError

    @pytest.fixture
    def is_object_storage(self):
        raise NotImplementedError

    @pytest.fixture
    def dir_md5(self):
        raise NotImplementedError


class TestAdd(_TestAdd):
    @pytest.fixture
    def hash_name(self):
        raise NotImplementedError

    @pytest.fixture
    def hash_value(self):
        raise NotImplementedError

    @pytest.fixture
    def dir_hash_value(self):
        raise NotImplementedError
