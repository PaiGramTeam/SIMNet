import os


def test_build():
    assert os.system("python setup.py") == 0  # pragma: no cover