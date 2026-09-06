# Copyright (c) 2020-2026 Gustavo de Rosa.
# Licensed under the Apache License, Version 2.0.

"""Pairwise non-parametric statistical tests.

Results map ``arg{i}-arg{j}``, with ``i < j``, to ``(reject, p_value)`` in input
order. Rejection is ``1`` exactly when ``p_value < alpha``. P-values are not
adjusted for multiple comparisons.

Keyword arguments are forwarded to SciPy. For one-sided alternatives, the
earlier sample is the first argument to the test. A non-finite p-value cannot
define a rejection decision and raises ``ValueError`` identifying the pair.
Use an explicit SciPy ``nan_policy`` when handling missing observations.

"""

from __future__ import annotations

from collections.abc import Callable
from itertools import combinations
from math import isfinite
from typing import Any

from numpy.typing import ArrayLike
from scipy import stats


def _compare(
    test: Callable[..., Any],
    samples: tuple[ArrayLike, ...],
    alpha: float,
    **kwargs: Any,
) -> dict[str, tuple[int, float]]:
    if len(samples) < 2:
        raise ValueError("`samples` must contain at least two samples.")
    if not 0 < alpha < 1:
        raise ValueError(f"`alpha` must be between 0 and 1, but got {alpha}.")

    output = {}
    for (left_index, left), (right_index, right) in combinations(enumerate(samples), 2):
        key = f"arg{left_index}-arg{right_index}"
        p_value = float(test(left, right, **kwargs).pvalue)
        if not isfinite(p_value):
            raise ValueError(f"`{key}` must produce a finite p-value, but got {p_value}.")

        output[key] = (int(p_value < alpha), p_value)

    return output


def u_test(*samples: ArrayLike, alpha: float = 0.05, **kwargs: Any) -> dict[str, tuple[int, float]]:
    """Compare independent samples with the Mann-Whitney U test.

    Args:
        *samples: At least two independent array-like samples to compare in input order.
        alpha: Rejection threshold strictly between zero and one.
        **kwargs: Options forwarded to ``scipy.stats.mannwhitneyu``.

    Returns:
        Dictionary of ``arg{i}-arg{j}`` keys mapped to ``(int(p_value < alpha), p_value)`` tuples.

    Raises:
        ValueError: Fewer than two samples, an out-of-range ``alpha``, or a non-finite p-value.

    Notes:
        Sample lengths may differ, but each pair must produce one scalar p-value. SciPy errors propagate unchanged.
        Options include ``alternative``, ``method``, and ``nan_policy``. SciPy uses a two-sided alternative by default.
        Keys satisfy ``i < j`` and follow input order. P-values are not adjusted for multiple comparisons.
        The null hypothesis concerns distributions, not merely medians. A one-sided alternative compares the
        earlier input sample against the later one.

    Examples:
        >>> from statys import pairwise
        >>> result = pairwise.u_test([1, 2], [3, 4], method="exact")
        >>> reject, p_value = result["arg0-arg1"]
        >>> reject, round(p_value, 3)
        (0, 0.333)

    """

    return _compare(stats.mannwhitneyu, samples, alpha, **kwargs)


def signed_rank(*samples: ArrayLike, alpha: float = 0.05, **kwargs: Any) -> dict[str, tuple[int, float]]:
    """Compare paired samples with the Wilcoxon signed-rank test.

    Args:
        *samples: At least two array-like samples of aligned, paired observations.
        alpha: Rejection threshold strictly between zero and one.
        **kwargs: Options forwarded to ``scipy.stats.wilcoxon``.

    Returns:
        Dictionary of ``arg{i}-arg{j}`` keys mapped to ``(int(p_value < alpha), p_value)`` tuples.

    Raises:
        ValueError: Fewer than two samples, an out-of-range ``alpha``, or a non-finite p-value.

    Notes:
        Each pair must produce one scalar p-value. SciPy errors propagate unchanged.
        Options include ``zero_method``, ``alternative``, ``method``, and ``nan_policy``.
        Keys satisfy ``i < j`` and follow input order. P-values are not adjusted for multiple comparisons.
        SciPy tests whether paired differences are symmetric about zero. Differences are the earlier sample
        minus the later one, so input order matters for one-sided alternatives.

    Examples:
        >>> from statys import pairwise
        >>> pairwise.signed_rank([1, 2, 3, 4], [5, 7, 9, 11], method="exact")
        {'arg0-arg1': (0, 0.125)}

    """

    return _compare(stats.wilcoxon, samples, alpha, **kwargs)


def rank_sum(*samples: ArrayLike, alpha: float = 0.05, **kwargs: Any) -> dict[str, tuple[int, float]]:
    """Compare independent samples with the Wilcoxon rank-sum test.

    Args:
        *samples: At least two independent array-like samples to compare in input order.
        alpha: Rejection threshold strictly between zero and one.
        **kwargs: Options forwarded to ``scipy.stats.ranksums``.

    Returns:
        Dictionary of ``arg{i}-arg{j}`` keys mapped to ``(int(p_value < alpha), p_value)`` tuples.

    Raises:
        ValueError: Fewer than two samples, an out-of-range ``alpha``, or a non-finite p-value.

    See Also:
        :func:`statys.pairwise.u_test`: Independent-sample comparison with tie correction available.

    Notes:
        Sample lengths may differ, but each pair must produce one scalar p-value. SciPy errors propagate unchanged.
        Options include ``alternative`` and ``nan_policy``. The default alternative is two-sided.
        Keys satisfy ``i < j`` and follow input order. P-values are not adjusted for multiple comparisons.
        SciPy's rank-sum test assumes continuous distributions and does not correct for ties.
        One-sided alternatives follow the input order.

    Examples:
        >>> from statys import pairwise
        >>> result = pairwise.rank_sum([1, 4], [2, 3])
        >>> result["arg0-arg1"]
        (0, 1.0)

    """

    return _compare(stats.ranksums, samples, alpha, **kwargs)
