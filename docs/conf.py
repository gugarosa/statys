from importlib.metadata import version as package_version

project = "statys"
copyright = "2020, Gustavo de Rosa"
author = "Gustavo de Rosa"
release = package_version("statys")
version = release

extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.autosummary",
    "sphinx.ext.napoleon",
]
autosummary_generate = True
exclude_patterns = ["_build"]
html_theme = "alabaster"
autodoc_default_options = {"members": True}
autodoc_member_order = "bysource"
