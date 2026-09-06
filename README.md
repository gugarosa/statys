# Statys

[![Latest release](https://img.shields.io/github/v/release/gugarosa/statys)](https://github.com/gugarosa/statys/releases)
[![CI](https://github.com/gugarosa/statys/actions/workflows/ci.yml/badge.svg)](https://github.com/gugarosa/statys/actions/workflows/ci.yml)
[![PyPI](https://img.shields.io/pypi/v/statys)](https://pypi.org/project/statys/)
[![License](https://img.shields.io/github/license/gugarosa/statys)](LICENSE)

Statys provides descriptive measures, pairwise non-parametric tests, Friedman
and Iman-Davenport statistics, Nemenyi critical differences, and comparison
plots.

## Installation

Statys requires Python 3.11 or newer. Add it to a project managed by uv with:

```bash
uv add statys
```

For a consumer installation in an existing Python environment, pip is also supported:

```bash
pip install statys
```

## Repeated comparisons

```python
import numpy as np

from statys import friedman, nemenyi, plot_critical_difference

scores = np.array(
    [
        [0.82, 0.79, 0.75],
        [0.80, 0.77, 0.78],
        [0.84, 0.81, 0.76],
        [0.79, 0.75, 0.74],
    ]
)

print(friedman(scores))
ranks, critical_difference = nemenyi(scores)
plot_critical_difference(
    ranks,
    critical_difference,
    labels=["Model A", "Model B", "Model C"],
    output="critical-difference.pdf",
)
```

Rows are experimental blocks and columns are the treatments being compared.
Smaller values receive lower ranks, with average ranks for ties. For metrics
where larger is better (such as accuracy), use `nemenyi(-scores)` to give
better treatments lower ranks.

`friedman` returns `((chi_square, df), (F, (df1, df2)))`, with tie correction
from SciPy and an Iman-Davenport F statistic. Perfect agreement between
non-constant block rankings gives `F = inf`. NaN inputs or blocks that all
tie every treatment give undefined (`nan`) statistics, not evidence for
the null hypothesis.

## Measures and pairwise tests

```python
from statys import measures, pairwise, significance

control = [0.82, 0.80, 0.84, 0.79]
model_a = [0.79, 0.77, 0.81, 0.75]
model_b = [0.75, 0.78, 0.76, 0.74]

print(measures.mean(control, model_a, model_b))

results = pairwise.signed_rank(control, model_a, model_b)
significance.plot_p_value(
    results,
    labels=["Control", "Model A", "Model B"],
    output="p-values.pdf",
)
```

The `measures` module also provides `kurtosis`, `max`, `median`, `min`, `rank`,
`skewness`, `std`, and `var`. The `pairwise` module provides `u_test`,
`signed_rank`, and `rank_sum`.

Pairwise results map `arg{i}-arg{j}` (`i < j`) to `(reject, p_value)`, in input
order. `reject` is `1` when `p_value < alpha` and `0` otherwise; p-values are
not adjusted for multiple comparisons. Additional keyword arguments are
forwarded to SciPy. The signed-rank test requires aligned, paired observations;
the other two tests compare independent samples. Use `u_test` rather than
`rank_sum` when tie correction is needed.

A test producing a non-finite p-value raises `ValueError` identifying the
affected pair rather than reporting a false no-rejection decision. Missing
data handling can be selected explicitly, for example with `nan_policy="omit"`.

Significance plots mirror each stored comparison into both matrix halves.
For one-sided tests, that result retains the original input order; the
mirrored cell is not a test in the opposite direction. Missing comparisons
remain blank. P-value colors use `1 - p` on a fixed zero-to-one scale, so
colors have the same meaning across plots; annotations show the original
p-values.

## Development

```bash
uv sync
uv run pytest
uv run pre-commit run --all-files
uv run --extra docs sphinx-build -W --keep-going -b html docs docs/_build/html
uv build
```

`pytest` also executes the examples in public docstrings. CI runs the
interpreter matrix, existing style hooks, and a warning-as-error documentation
build before permitting a release.

### Code style

Adapted from [cpmux's conventions](https://github.com/gugarosa/cpmux/blob/main/CONVENTIONS.md),
using the corresponding phitrain rule IDs:

- Use modern unions (`X | None`) and builtin generics (`dict[str, Any]`, `list[str]`).
  Import ABCs such as `Callable` and `Iterable` from `collections.abc`, not `typing`.
  Keep syntax compatible with Statys's declared Python 3.11+ support. (R2)
- Keep imports top-level and absolute (`from statys.x import y`), grouped as stdlib,
  third-party, then local imports, with blank lines between groups.
- Public APIs use [Google-style docstrings][google-docstrings] with a single-sentence
  summary and one-line `Args:`, `Returns:`, and `Raises:` entries. Do not put semicolons
  or `defaults to <X>` tails in entries. Keep detailed contracts and examples in
  `Notes:` and `Examples:` rather than discarding them. (R3, R13)
- Keep one blank line before a docstring's closing `"""` and one blank line after it
  before the first statement or field. Private helpers and framework-dispatched
  overrides have no docstrings. Test functions stay plain, without docstrings or type hints.
- A regular class has a single-sentence class summary and documents constructor
  arguments on `__init__`. Data classes without an explicit constructor document every
  field in `Attributes:`, one `name: what it holds.` entry per line.
- Raised messages name the backticked argument or offender and end with a period:
  `` "`<name>` <verb-phrase>[, but got <value>]." ``. Use `is None`/`is True` prose. (R1)
- Runtime validation uses `if`/`raise` with a specific exception, not `assert`.
  Never use a bare `except:` or translate dependency failures into successful-looking defaults.
- Comments explain why, not what. Prefer no comment or one line, with a three-line
  maximum, no banner separators, and no trailing period. Copyright/license notices
  retain their prescribed punctuation. Preserve attribution for adapted code. (R8)
- Separate logical phases with a single blank line in function bodies of at least
  12 lines. Do not insert a blank line after every statement. (R11)
- Inline first. Extract helpers, constants, or parameters when a second call site
  establishes reuse, rather than adding speculative abstractions. Preserve supported public APIs. (R16)
- Use double-quoted string literals. Code and readable prose stay within 120 columns,
  using the existing Black, isort, and Flake8 tools without broad suppressions. (R9)
- Never use `print()` in library code. If logging is introduced, follow the shared
  `get_logger(__name__)` pattern. Warning/error diagnostics use a backticked offender
  and a trailing period (`` "`name=value` <verb-phrase>." ``), while info/debug stay plain. (R14)

Every tracked Python file starts with this two-line header:

```python
# Copyright (c) 2020-2026 Gustavo de Rosa.
# Licensed under the Apache License, Version 2.0.
```

Statys has no logging or application-framework layer to adapt, so these conventions
do not introduce cpmux, Rich, Typer, Textual, or Pydantic dependencies. Example scripts
are consumers rather than library code and may print their results. The Apache-2.0
license and supported package-level exports remain unchanged.

[google-docstrings]: https://google.github.io/styleguide/pyguide.html#383-functions-and-methods

The library ships inline type information. Array inputs use
`numpy.typing.ArrayLike`; rank arrays and fixed result tuples have concrete
annotations. Measure return values and forwarded keyword arguments remain
dynamic because NumPy/SciPy determine their type from the input dtype and
options. Do not narrow these contracts by coercing or copying inputs merely
to satisfy a type annotation.

Keep stateless operations as functions and share actual responsibilities such as
the pairwise comparison loop. Use NumPy/SciPy for statistical primitives and explicit
Matplotlib figures for plotting, without new factories or global plotting state.

Documentation is available at
[statys.readthedocs.io](https://statys.readthedocs.io).

## Releasing

Use `uv version --bump patch` (or the appropriate version increment), update
`statys.__version__` to match, and open a pull request for review.

After the pull request is merged into `main` and the full CI matrix succeeds,
the release job publishes the untagged version to PyPI and creates a GitHub
release and tag at that commit. Already-tagged versions are not republished.
Publication uses the repository's `PYPI_API_TOKEN` secret and does not depend
on a local CLI session.

Publishing a GitHub release manually remains supported; its tag must match
the package version, prefixed with `v`. First attempts fail on duplicate PyPI
files. An explicit rerun of the same workflow can resume a partial upload,
skipping existing files rather than replacing them.
