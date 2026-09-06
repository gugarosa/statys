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

Public functions use [NumPy-style docstrings](https://numpydoc.readthedocs.io/en/latest/format.html):
document input shapes, defaults, result structure, expected errors, and a
small reproducible example. Keep implementation details out of parameter
descriptions.

The library ships inline type information. Array inputs use
`numpy.typing.ArrayLike`; rank arrays and fixed result tuples have concrete
annotations. Measure return values and forwarded keyword arguments remain
dynamic because NumPy/SciPy determine their type from the input dtype and
options. Do not narrow these contracts by coercing or copying inputs merely
to satisfy a type annotation.

Keep stateless operations as functions and share only actual responsibilities
(such as the pairwise comparison loop). Use NumPy/SciPy for statistical
primitives and explicit Matplotlib figures for plotting, rather than adding
estimator classes, factories, or global plotting state without a concrete
requirement.

Use blank lines to separate logical phases such as validation, calculation,
and output or rendering. Keep comments that explain decisions or invariants,
not comments that repeat obvious assignments. Preserve source attribution
and useful references when simplifying adapted code.

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
