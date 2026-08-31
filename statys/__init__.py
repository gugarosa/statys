"""Statistical comparison tools."""

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
__version__ = "2.0.1"
