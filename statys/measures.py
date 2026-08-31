"""Descriptive measures for one or more samples."""

import numpy as np
from scipy import stats


def _apply(function, samples, **kwargs):
    if not samples:
        raise ValueError("at least one sample is required")
    return {
        f"arg{index}": function(sample, **kwargs)
        for index, sample in enumerate(samples)
    }


def kurtosis(*samples, **kwargs):
    """Calculate kurtosis for each sample."""

    return _apply(stats.kurtosis, samples, **kwargs)


def max(*samples, **kwargs):
    """Calculate the maximum for each sample."""

    return _apply(np.max, samples, **kwargs)


def mean(*samples, **kwargs):
    """Calculate the mean for each sample."""

    return _apply(np.mean, samples, **kwargs)


def median(*samples, **kwargs):
    """Calculate the median for each sample."""

    return _apply(np.median, samples, **kwargs)


def min(*samples, **kwargs):
    """Calculate the minimum for each sample."""

    return _apply(np.min, samples, **kwargs)


def rank(*samples, **kwargs):
    """Rank the values in each sample."""

    return _apply(stats.rankdata, samples, **kwargs)


def skewness(*samples, **kwargs):
    """Calculate skewness for each sample."""

    return _apply(stats.skew, samples, **kwargs)


def std(*samples, **kwargs):
    """Calculate standard deviation for each sample."""

    return _apply(np.std, samples, **kwargs)


def var(*samples, **kwargs):
    """Calculate variance for each sample."""

    return _apply(np.var, samples, **kwargs)
