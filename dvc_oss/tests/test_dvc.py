import pytest
from dvc.testing.api_tests import (  # noqa, pylint: disable=unused-import
    TestAPI,
)
from dvc.testing.remote_tests import (  # noqa, pylint: disable=unused-import
    TestRemote,
)


@pytest.fixture
def remote(make_remote):
    yield make_remote(name="upstream", typ="oss")
