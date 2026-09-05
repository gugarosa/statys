"""Pairwise non-parametric statistical tests.

Results map ``arg{i}-arg{j}``, with ``i < j``, to ``(reject, p_value)`` in input
order. Rejection is ``1`` exactly when ``p_value < alpha``. P-values are not
adjusted for multiple comparisons.

Keyword arguments are forwarded to SciPy. For one-sided alternatives, the
earlier sample is the first argument to the test. A non-finite p-value cannot
define a rejection decision and raises ``ValueError`` identifying the pair.
Use an explicit SciPy ``nan_policy`` when handling missing observations.
"""

from itertools import combinations
from math import isfinite

from scipy import stats


def _compare(test, samples, alpha, **kwargs) -> dict[str, tuple[int, float]]:
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


def u_test(*samples, alpha: float = 0.05, **kwargs) -> dict[str, tuple[int, float]]:
    """Perform Mann-Whitney U tests for each pair of independent samples."""

    return _compare(stats.mannwhitneyu, samples, alpha, **kwargs)


def signed_rank(
    *samples, alpha: float = 0.05, **kwargs
) -> dict[str, tuple[int, float]]:
    """Perform Wilcoxon signed-rank tests on aligned, paired observations."""

    return _compare(stats.wilcoxon, samples, alpha, **kwargs)


def rank_sum(*samples, alpha: float = 0.05, **kwargs) -> dict[str, tuple[int, float]]:
    """Perform Wilcoxon rank-sum tests for each pair of independent samples.

    SciPy's rank-sum test does not correct for ties; use ``u_test`` for tied data.
    """

    return _compare(stats.ranksums, samples, alpha, **kwargs)
