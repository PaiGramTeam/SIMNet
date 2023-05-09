import os

import pytest


def test_build(if_test_build: bool):
    if not if_test_build:
        pytest.skip("TEST_BUILD not enabled")
    assert os.system("python setup.py") == 0  # pragma: no cover
