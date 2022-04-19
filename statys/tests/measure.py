"""Statistical-related measures.
"""

import numpy as np
import scipy.stats as s

import statys.utils.wrappers as w
from statys.utils import logging

logger = logging.get_logger(__name__)


def kurtosis(dist, **kwargs):
    """Measures the kurtosis of a distribution.

    Args:
        dist (Distribution): Distribution to be analyzed.

    Returns:
        Dictionary holding the measure's outputs.

    """

    logger.info("Calculating kurtosis ...")

    output = w.measure_pipeline(s.kurtosis, dist, **kwargs)

    logger.info("Kurtosis calculated.")
    logger.debug(output)

    return output


def max(dist, **kwargs):
    """Measures the maximum value of a distribution.

    Args:
        dist (Distribution): Distribution to be analyzed.

    Returns:
        Dictionary holding the measure's outputs.

    """

    logger.info("Finding maximum value ...")

    output = w.measure_pipeline(np.max, dist, **kwargs)

    logger.info("Maximum value found.")
    logger.debug(output)

    return output


def mean(dist, **kwargs):
    """Measures the mean of a distribution.

    Args:
        dist (Distribution): Distribution to be analyzed.

    Returns:
        Dictionary holding the measure's outputs.

    """

    logger.info("Calculating mean ...")

    output = w.measure_pipeline(np.mean, dist, **kwargs)

    logger.info("Mean calculated.")
    logger.debug(output)

    return output


def median(dist, **kwargs):
    """Measures the median of a distribution.

    Args:
        dist (Distribution): Distribution to be analyzed.

    Returns:
        Dictionary holding the measure's outputs.

    """

    logger.info("Calculating median ...")

    output = w.measure_pipeline(np.median, dist, **kwargs)

    logger.info("Median calculated.")
    logger.debug(output)

    return output


def min(dist, **kwargs):
    """Measures the minimum value of a distribution.

    Args:
        dist (Distribution): Distribution to be analyzed.

    Returns:
        Dictionary holding the measure's outputs.

    """

    logger.info("Finding minimum value ...")

    output = w.measure_pipeline(np.min, dist, **kwargs)

    logger.info("Minimum value found.")
    logger.debug(output)

    return output


def rank(dist, **kwargs):
    """Ranks the values of a distribution.

    Args:
        dist (Distribution): Distribution to be analyzed.

    Returns:
        Dictionary holding the measure's outputs.

    """

    logger.info("Ranking distribution ...")

    output = w.measure_pipeline(s.rankdata, dist, **kwargs)

    logger.info("Distribution ranked.")
    logger.debug(output)

    return output


def skewness(dist, **kwargs):
    """Measures the skewness of a distribution.

    Args:
        dist (Distribution): Distribution to be analyzed.

    Returns:
        Dictionary holding the measure's outputs.

    """

    logger.info("Calculating skewness ...")

    output = w.measure_pipeline(s.skew, dist, **kwargs)

    logger.info("Skewness calculated.")
    logger.debug(output)

    return output


def std(dist, **kwargs):
    """Measures the standard deviation of a distribution.

    Args:
        dist (Distribution): Distribution to be analyzed.

    Returns:
        Dictionary holding the measure's outputs.

    """

    logger.info("Calculating standard deviation ...")

    output = w.measure_pipeline(np.std, dist, **kwargs)

    logger.info("Standard deviation calculated.")
    logger.debug(output)

    return output


def var(dist, **kwargs):
    """Measures the variance of a distribution.

    Args:
        dist (Distribution): Distribution to be analyzed.

    Returns:
        Dictionary holding the measure's outputs.

    """

    logger.info("Calculating variance ...")

    output = w.measure_pipeline(np.var, dist, **kwargs)

    logger.info("Variance calculated.")
    logger.debug(output)

    return output
