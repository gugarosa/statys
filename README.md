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

## Development

```bash
uv sync
uv run pytest
uv run pre-commit run --all-files
uv build
```

Documentation is available at
[statys.readthedocs.io](https://statys.readthedocs.io).
