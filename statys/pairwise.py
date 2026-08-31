"""Pairwise non-parametric statistical tests."""

from itertools import combinations

from scipy import stats


def _compare(test, samples, alpha, **kwargs):
    if len(samples) < 2:
        raise ValueError("at least two samples are required")
    if not 0 < alpha < 1:
        raise ValueError("alpha must be between 0 and 1")

    output = {}
    for (left_index, left), (right_index, right) in combinations(
        enumerate(samples), 2
    ):
        p_value = float(test(left, right, **kwargs).pvalue)
        output[f"arg{left_index}-arg{right_index}"] = (
            int(p_value < alpha),
            p_value,
        )
    return output


def u_test(*samples, alpha=0.05, **kwargs):
    """Perform Mann-Whitney U tests for every pair of samples."""

    return _compare(stats.mannwhitneyu, samples, alpha, **kwargs)


def signed_rank(*samples, alpha=0.05, **kwargs):
    """Perform Wilcoxon signed-rank tests for every pair of samples."""

    return _compare(stats.wilcoxon, samples, alpha, **kwargs)


def rank_sum(*samples, alpha=0.05, **kwargs):
    """Perform Wilcoxon rank-sum tests for every pair of samples."""

    return _compare(stats.ranksums, samples, alpha, **kwargs)
