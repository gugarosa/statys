"""Friedman and Nemenyi comparisons."""

from math import inf, sqrt

import numpy as np
from scipy import stats


def _matrix(data) -> np.ndarray:
    values = np.asarray(data, dtype=float)
    if values.ndim != 2 or min(values.shape) < 2:
        raise ValueError("data must contain at least two blocks and two treatments")
    return values


def friedman(data) -> tuple[tuple[float, int], tuple[float, tuple[int, int]]]:
    """Return Friedman and Iman-Davenport statistics for a score matrix.

    Rows are experimental blocks and columns are treatments or algorithms.
    """

    values = _matrix(data)
    n_blocks, n_treatments = values.shape
    if n_treatments < 3:
        raise ValueError("Friedman's test requires at least three treatments")

    statistic = float(stats.friedmanchisquare(*values.T).statistic)
    denominator = n_blocks * (n_treatments - 1) - statistic
    iman = inf if denominator == 0 else (n_blocks - 1) * statistic / denominator
    degrees = n_treatments - 1

    return (statistic, degrees), (
        float(iman),
        (degrees, degrees * (n_blocks - 1)),
    )


def nemenyi(data, alpha: float = 0.05) -> tuple[np.ndarray, float]:
    """Return average ranks and the Nemenyi critical difference."""

    if not 0 < alpha < 1:
        raise ValueError("alpha must be between 0 and 1")

    values = _matrix(data)
    n_blocks, n_treatments = values.shape
    ranks = stats.rankdata(values, axis=1).mean(axis=0)
    q = stats.studentized_range.ppf(1 - alpha, n_treatments, inf) / sqrt(2)
    critical_difference = q * sqrt(
        n_treatments * (n_treatments + 1) / (6 * n_blocks)
    )

    return ranks, float(critical_difference)
