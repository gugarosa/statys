from importlib.metadata import version
from importlib.resources import files

import statys


def test_public_version_matches_package_metadata():
    assert statys.__version__ == version("statys")


def test_package_includes_inline_type_information():
    assert files("statys").joinpath("py.typed").is_file()
