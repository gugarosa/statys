"""Statistical-related measures.
"""

import numpy as np
import scipy.stats as s

import statys.utils.logging as l
import statys.utils.wrappers as w

logger = l.get_logger(__name__)


def kurtosis(dist, **kwargs):
    """Measures the kurtosis of a distribution.

    Args:
        dist (Distribution): Distribution to be analyzed.

    Returns:
        Dictionary holding the measure's outputs.

    """

    logger.info('Calculating kurtosis ...')

    # Calculates the kurtosis value of a distribution
    output = w.measure_pipeline(s.kurtosis, dist, **kwargs)

    logger.info('Kurtosis calculated.')
    logger.debug(output)

    return output


def max(dist, **kwargs):
    """Measures the maximum value of a distribution.

    Args:
        dist (Distribution): Distribution to be analyzed.

    Returns:
        Dictionary holding the measure's outputs.

    """

    logger.info('Finding maximum value ...')

    # Calculates the maximum value of a distribution
    output = w.measure_pipeline(np.max, dist, **kwargs)

    logger.info('Maximum value found.')
    logger.debug(output)

    return output


def mean(dist, **kwargs):
    """Measures the mean of a distribution.

    Args:
        dist (Distribution): Distribution to be analyzed.

    Returns:
        Dictionary holding the measure's outputs.

    """

    logger.info('Calculating mean ...')

    # Calculates the mean value of a distribution
    output = w.measure_pipeline(np.mean, dist, **kwargs)

    logger.info('Mean calculated.')
    logger.debug(output)

    return output


def median(dist, **kwargs):
    """Measures the median of a distribution.

    Args:
        dist (Distribution): Distribution to be analyzed.

    Returns:
        Dictionary holding the measure's outputs.

    """

    logger.info('Calculating median ...')

    # Calculates the median value of a distribution
    output = w.measure_pipeline(np.median, dist, **kwargs)

    logger.info('Median calculated.')
    logger.debug(output)

    return output


def min(dist, **kwargs):
    """Measures the minimum value of a distribution.

    Args:
        dist (Distribution): Distribution to be analyzed.

    Returns:
        Dictionary holding the measure's outputs.

    """

    logger.info('Finding minimum value ...')

    # Calculates the minimum value of a distribution
    output = w.measure_pipeline(np.min, dist, **kwargs)

    logger.info('Minimum value found.')
    logger.debug(output)

    return output


def rank(dist, **kwargs):
    """Ranks the values of a distribution.

    Args:
        dist (Distribution): Distribution to be analyzed.

    Returns:
        Dictionary holding the measure's outputs.

    """

    logger.info('Ranking distribution ...')

    # Calculates the minimum value of a distribution
    output = w.measure_pipeline(s.rankdata, dist, **kwargs)

    logger.info('Distribution ranked.')
    logger.debug(output)

    return output


def skewness(dist, **kwargs):
    """Measures the skewness of a distribution.

    Args:
        dist (Distribution): Distribution to be analyzed.

    Returns:
        Dictionary holding the measure's outputs.

    """

    logger.info('Calculating skewness ...')

    # Calculates the skewness value of a distribution
    output = w.measure_pipeline(s.skew, dist, **kwargs)

    logger.info('Skewness calculated.')
    logger.debug(output)

    return output


def std(dist, **kwargs):
    """Measures the standard deviation of a distribution.

    Args:
        dist (Distribution): Distribution to be analyzed.

    Returns:
        Dictionary holding the measure's outputs.

    """

    logger.info('Calculating standard deviation ...')

    # Calculates the standard deviation of a distribution
    output = w.measure_pipeline(np.std, dist, **kwargs)

    logger.info('Standard deviation calculated.')
    logger.debug(output)

    return output


def var(dist, **kwargs):
    """Measures the variance of a distribution.

    Args:
        dist (Distribution): Distribution to be analyzed.

    Returns:
        Dictionary holding the measure's outputs.

    """

    logger.info('Calculating variance ...')

    # Calculates the variance of a distribution
    output = w.measure_pipeline(np.var, dist, **kwargs)

    logger.info('Variance calculated.')
    logger.debug(output)

    return output
