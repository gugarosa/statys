# Copyright (c) 2020-2026 Gustavo de Rosa.
# Licensed under the Apache License, Version 2.0.

from importlib.metadata import version as package_version

project = "statys"
copyright = "2020-2026, Gustavo de Rosa"
author = "Gustavo de Rosa"
release = package_version("statys")
version = release

extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.autosummary",
    "sphinx.ext.napoleon",
]
autosummary_generate = True
napoleon_numpy_docstring = False
exclude_patterns = ["_build"]
html_theme = "alabaster"
autodoc_default_options = {"members": True}
autodoc_member_order = "bysource"
# Docstrings describe shapes without expanding ArrayLike unions
autodoc_typehints = "none"
