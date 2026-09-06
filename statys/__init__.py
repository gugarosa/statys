# Copyright (c) 2020-2026 Gustavo de Rosa.
# Licensed under the Apache License, Version 2.0.

"""Statistical comparison tools.

Comparison functions are available at package level alongside the measures,
pairwise, and significance modules.

"""

from statys import measures, pairwise, significance
from statys.critical import plot_critical_difference
from statys.statistics import friedman, nemenyi

__all__ = [
    "friedman",
    "measures",
    "nemenyi",
    "pairwise",
    "plot_critical_difference",
    "significance",
]
__version__ = "2.0.3"
