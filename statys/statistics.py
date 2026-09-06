# Copyright (c) 2020-2026 Gustavo de Rosa.
# Licensed under the Apache License, Version 2.0.

"""Friedman and Nemenyi comparisons.

Score matrices use experimental blocks as rows and treatments as columns.

"""

from __future__ import annotations

from math import inf, nan, sqrt

import numpy as np
from numpy.typing import ArrayLike, NDArray
from scipy import stats


def _matrix(data: ArrayLike) -> NDArray[np.float64]:
    values = np.asarray(data, dtype=float)
    if values.ndim != 2 or min(values.shape) < 2:
        raise ValueError("`data` must contain at least two blocks and two treatments.")

    return values


def friedman(
    data: ArrayLike,
) -> tuple[tuple[float, int], tuple[float, tuple[int, int]]]:
    """Return Friedman and Iman-Davenport statistics for a score matrix.

    Args:
        data: Score matrix shaped ``(n_blocks, n_treatments)`` with at least two blocks and three treatments.

    Returns:
        Tuple ``(friedman_result, iman_result)`` containing the statistics and their degrees of freedom.

    Raises:
        ValueError: ``data`` is not a numeric matrix with at least two blocks and three treatments.

    See Also:
        :func:`statys.nemenyi`: Compute average ranks and a post-hoc critical difference.

    Notes:
        Columns must identify the same treatments in every block. Scores are converted to floating point
        without modifying input arrays.

        ``friedman_result`` is a tuple of (float, int): SciPy's tie-corrected chi-square statistic followed by
        ``n_treatments - 1`` degrees of freedom. ``iman_result`` is a tuple of (float, tuple of (int, int)):
        the Iman-Davenport F statistic and its numerator/denominator degrees of freedom,
        ``(k - 1, (k - 1) * (n - 1))``, for ``n`` blocks and ``k`` treatments.
        No p-values or rejection decisions are returned.

        Identical, non-constant block rankings give an infinite F statistic. NaN inputs or ties across every
        treatment in every block give undefined (NaN) statistics, following SciPy. The chi-square approximation
        can be unreliable for small samples, so returning a statistic does not establish significance.

    Examples:
        >>> from statys import friedman
        >>> data = [[1, 2, 3], [2, 1, 3], [1, 3, 2], [2, 3, 1]]
        >>> chi_square, iman = friedman(data)
        >>> chi_square
        (1.5, 2)
        >>> round(iman[0], 6), iman[1]
        (0.692308, (2, 6))

    """

    values = _matrix(data)
    n_blocks, n_treatments = values.shape
    if n_treatments < 3:
        raise ValueError("`data` must contain at least three treatments for Friedman's test.")

    statistic = float(stats.friedmanchisquare(*values.T).statistic)

    ranks = stats.rankdata(values, axis=1)
    mean_ranks = ranks.mean(axis=0)
    between = n_blocks * np.sum((mean_ranks - (n_treatments + 1) / 2) ** 2)
    within = np.sum((ranks - mean_ranks) ** 2)

    # Q = n * (k - 1) * between / (between + within)
    # This equivalent F avoids subtracting Q from its bound near perfect agreement
    if within == 0:
        iman = inf if between > 0 else nan
    else:
        iman = (n_blocks - 1) * between / within

    degrees = n_treatments - 1

    return (statistic, degrees), (
        float(iman),
        (degrees, degrees * (n_blocks - 1)),
    )


def nemenyi(data: ArrayLike, alpha: float = 0.05) -> tuple[NDArray[np.float64], float]:
    """Return average ranks and the Nemenyi critical difference.

    Args:
        data: Score matrix shaped ``(n_blocks, n_treatments)`` with at least two blocks and two treatments.
        alpha: Significance level strictly between zero and one.

    Returns:
        Tuple ``(ranks, critical_difference)`` containing an average-rank array and the Nemenyi threshold.

    Raises:
        ValueError: ``data`` is not a matrix with at least two blocks and treatments, or ``alpha`` is out of bounds.

    See Also:
        :func:`statys.friedman`: Compute the omnibus test statistics.
        :func:`statys.plot_critical_difference`: Display ranks and their threshold.

    Notes:
        Columns must identify the same treatments in every block. Smaller scores get lower ranks.
        Negate scores when larger values should rank first. Input arrays are not modified.

        ``ranks`` is a float64 ndarray shaped ``(n_treatments,)`` containing average within-block ranks in
        the original column order. Ties receive their average rank. ``critical_difference`` is a float
        threshold based on the studentized-range distribution. Larger rank differences are significant.

        This function does not run an omnibus test or decide whether post-hoc analysis is warranted.
        NaN scores propagate into the average ranks.

    Examples:
        >>> from statys import nemenyi
        >>> data = [[1, 2, 3], [2, 1, 3], [1, 3, 2], [2, 3, 1]]
        >>> ranks, critical_difference = nemenyi(data)
        >>> ranks.tolist()
        [1.5, 2.25, 2.25]
        >>> round(critical_difference, 6)
        1.657247

    """

    if not 0 < alpha < 1:
        raise ValueError(f"`alpha` must be between 0 and 1, but got {alpha}.")

    values = _matrix(data)
    n_blocks, n_treatments = values.shape

    ranks = stats.rankdata(values, axis=1).mean(axis=0)

    q = stats.studentized_range.ppf(1 - alpha, n_treatments, inf) / sqrt(2)
    critical_difference = q * sqrt(n_treatments * (n_treatments + 1) / (6 * n_blocks))

    return ranks, float(critical_difference)
