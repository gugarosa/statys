# Copyright (c) 2020-2026 Gustavo de Rosa.
# Licensed under the Apache License, Version 2.0.

from importlib.metadata import version
from importlib.resources import files

import statys


def test_public_version_matches_package_metadata():
    assert statys.__version__ == version("statys")


def test_package_includes_inline_type_information():
    assert files("statys").joinpath("py.typed").is_file()
