"""Friedman and Nemenyi comparisons."""

from math import inf, nan, sqrt

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
    The result is ``((chi_square, k - 1), (F, (k - 1, (k - 1) * (n - 1))))``
    for ``n`` blocks and ``k`` treatments. The Friedman statistic is corrected
    for ties by SciPy. Identical, non-constant rankings give ``F = inf``.
    NaN inputs or ties across every treatment in every block give undefined
    (NaN) statistics, following SciPy.
    """

    values = _matrix(data)
    n_blocks, n_treatments = values.shape
    if n_treatments < 3:
        raise ValueError("Friedman's test requires at least three treatments")

    statistic = float(stats.friedmanchisquare(*values.T).statistic)
    ranks = stats.rankdata(values, axis=1)
    mean_ranks = ranks.mean(axis=0)
    between = n_blocks * np.sum((mean_ranks - (n_treatments + 1) / 2) ** 2)
    within = np.sum((ranks - mean_ranks) ** 2)
    # Q = n * (k - 1) * between / (between + within).
    # This equivalent F avoids subtracting Q from its bound near perfect agreement.
    if within == 0:
        iman = inf if between > 0 else nan
    else:
        iman = (n_blocks - 1) * between / within
    degrees = n_treatments - 1

    return (statistic, degrees), (
        float(iman),
        (degrees, degrees * (n_blocks - 1)),
    )


def nemenyi(data, alpha: float = 0.05) -> tuple[np.ndarray, float]:
    """Return average ranks and the Nemenyi critical difference.

    Rows are blocks and columns are treatments. Smaller values receive lower
    ranks, with average ranks for ties. Negate scores if larger values should
    receive lower ranks. ``alpha`` must lie strictly between zero and one.
    """

    if not 0 < alpha < 1:
        raise ValueError("alpha must be between 0 and 1")

    values = _matrix(data)
    n_blocks, n_treatments = values.shape
    ranks = stats.rankdata(values, axis=1).mean(axis=0)
    q = stats.studentized_range.ppf(1 - alpha, n_treatments, inf) / sqrt(2)
    critical_difference = q * sqrt(n_treatments * (n_treatments + 1) / (6 * n_blocks))

    return ranks, float(critical_difference)
