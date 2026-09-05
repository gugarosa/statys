from importlib.metadata import version

import statys


def test_public_version_matches_package_metadata():
    assert statys.__version__ == version("statys")
