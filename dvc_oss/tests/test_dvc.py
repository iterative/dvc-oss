import pytest

from dvc.testing.api_tests import (  # noqa: F401
    TestAPI,
)
from dvc.testing.remote_tests import (  # noqa: F401
    TestRemote,
)


@pytest.fixture
def remote(make_remote):
    return make_remote(name="upstream", typ="oss")
