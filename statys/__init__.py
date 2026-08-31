"""Statistical comparison tools."""

from statys.critical import plot_critical_difference
from statys.statistics import friedman, nemenyi

__all__ = ["friedman", "nemenyi", "plot_critical_difference"]
__version__ = "2.0.0"
