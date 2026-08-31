# Statys

[![Latest release](https://img.shields.io/github/v/release/gugarosa/statys)](https://github.com/gugarosa/statys/releases)
[![CI](https://github.com/gugarosa/statys/actions/workflows/ci.yml/badge.svg)](https://github.com/gugarosa/statys/actions/workflows/ci.yml)
[![PyPI](https://img.shields.io/pypi/v/statys)](https://pypi.org/project/statys/)
[![License](https://img.shields.io/github/license/gugarosa/statys)](LICENSE)

Statys provides Friedman and Iman-Davenport statistics, Nemenyi critical
differences, and critical-difference diagrams for comparing treatments or
algorithms across repeated experimental blocks.

Statys requires Python 3.11 or newer.

## Installation

```bash
pip install statys
```

## Example

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

## Development

```bash
uv sync
uv run pytest
uv run pre-commit run --all-files
uv build
```

Documentation is available at
[statys.readthedocs.io](https://statys.readthedocs.io).
