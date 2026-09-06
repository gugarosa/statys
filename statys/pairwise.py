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
        raise ValueError("at least two samples are required")
    if not 0 < alpha < 1:
        raise ValueError("alpha must be between 0 and 1")

    output = {}
    for (left_index, left), (right_index, right) in combinations(enumerate(samples), 2):
        key = f"arg{left_index}-arg{right_index}"
        p_value = float(test(left, right, **kwargs).pvalue)
        if not isfinite(p_value):
            raise ValueError(f"{key}: test returned a non-finite p-value")

        output[key] = (int(p_value < alpha), p_value)

    return output


def u_test(
    *samples: ArrayLike, alpha: float = 0.05, **kwargs: Any
) -> dict[str, tuple[int, float]]:
    """Compare independent samples with the Mann-Whitney U test.

    Args:
        *samples: At least two array-like samples, which may have different
            lengths. Each pair must produce one scalar p-value.
        alpha (float): Rejection threshold, strictly between zero and one.
            Defaults to 0.05.
        **kwargs: Passed to ``scipy.stats.mannwhitneyu``, including
            ``alternative``, ``method``, and ``nan_policy``. Defaults are
            SciPy's, including a two-sided alternative.

    Returns:
        dict[str, tuple[int, float]]: Keys ``arg{i}-arg{j}`` for ``i < j``
        in input order. Values are ``(reject, p_value)``, where rejection
        is ``int(p_value < alpha)``. P-values are not adjusted for multiple
        comparisons.

    Raises:
        ValueError: If fewer than two samples are supplied, `alpha` is
            outside its bounds, or a test returns a non-finite p-value.
            SciPy errors propagate unchanged.

    Notes:
        The null hypothesis concerns the distributions, not merely their
        medians. A one-sided alternative compares the earlier input sample
        against the later one.

    Examples:
        >>> from statys import pairwise
        >>> result = pairwise.u_test([1, 2], [3, 4], method="exact")
        >>> reject, p_value = result["arg0-arg1"]
        >>> reject, round(p_value, 3)
        (0, 0.333)
    """

    return _compare(stats.mannwhitneyu, samples, alpha, **kwargs)


def signed_rank(
    *samples: ArrayLike, alpha: float = 0.05, **kwargs: Any
) -> dict[str, tuple[int, float]]:
    """Compare paired samples with the Wilcoxon signed-rank test.

    Args:
        *samples: At least two array-like samples of aligned, paired
            observations. Each pair must produce one scalar p-value.
        alpha (float): Rejection threshold, strictly between zero and one.
            Defaults to 0.05.
        **kwargs: Passed to ``scipy.stats.wilcoxon``, including
            ``zero_method``, ``alternative``, ``method``, and ``nan_policy``.

    Returns:
        dict[str, tuple[int, float]]: Keys ``arg{i}-arg{j}`` for ``i < j``
        in input order, mapped to ``(int(p_value < alpha), p_value)``.
        P-values are unadjusted.

    Raises:
        ValueError: If fewer than two samples are supplied, `alpha` is
            outside its bounds, or a test returns a non-finite p-value.
            SciPy errors propagate unchanged.

    Notes:
        SciPy tests whether paired differences are symmetric about zero.
        Differences are computed as the earlier sample minus the later
        one; this order matters for one-sided alternatives.

    Examples:
        >>> from statys import pairwise
        >>> pairwise.signed_rank([1, 2, 3, 4], [5, 7, 9, 11], method="exact")
        {'arg0-arg1': (0, 0.125)}
    """

    return _compare(stats.wilcoxon, samples, alpha, **kwargs)


def rank_sum(
    *samples: ArrayLike, alpha: float = 0.05, **kwargs: Any
) -> dict[str, tuple[int, float]]:
    """Compare independent samples with the Wilcoxon rank-sum test.

    Args:
        *samples: At least two array-like samples, which may have different
            lengths. Each pair must produce one scalar p-value.
        alpha (float): Rejection threshold, strictly between zero and one.
            Defaults to 0.05.
        **kwargs: Passed to ``scipy.stats.ranksums``, including
            ``alternative`` and ``nan_policy``. The default alternative
            is two-sided.

    Returns:
        dict[str, tuple[int, float]]: Keys ``arg{i}-arg{j}`` for ``i < j``
        in input order, mapped to ``(int(p_value < alpha), p_value)``.
        P-values are unadjusted.

    Raises:
        ValueError: If fewer than two samples are supplied, `alpha` is
            outside its bounds, or a test returns a non-finite p-value.
            SciPy errors propagate unchanged.

    See Also:
        :func:`statys.pairwise.u_test`: Independent-sample comparison
        with tie correction available.

    Notes:
        SciPy's rank-sum test assumes continuous distributions and does
        not correct for ties. One-sided alternatives follow the input order.

    Examples:
        >>> from statys import pairwise
        >>> result = pairwise.rank_sum([1, 4], [2, 3])
        >>> result["arg0-arg1"]
        (0, 1.0)
    """

    return _compare(stats.ranksums, samples, alpha, **kwargs)
