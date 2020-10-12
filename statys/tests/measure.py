"""Statistical-related measures.
"""

import numpy as np
import scipy.stats as st

import statys.utils.logging as l
import statys.utils.wrappers as w

logger = l.get_logger(__name__)


def kurtosis(dist):
    """Measures the kurtosis of a distribution.

    Args:
        dist (Distribution): Distribution to be analyzed.

    Returns:
        Dictionary holding the measure's outputs.

    """

    logger.info('Calculating kurtosis ...')

    # Calculates the kurtosis value of a distribution
    output = w.measure_pipeline(st.kurtosis, dist)

    logger.info('Kurtosis calculated.')
    logger.debug(output)

    return output


def max(dist):
    """Measures the maximum value of a distribution.

    Args:
        dist (Distribution): Distribution to be analyzed.

    Returns:
        Dictionary holding the measure's outputs.

    """

    logger.info('Finding maximum value ...')

    # Calculates the maximum value of a distribution
    output = w.measure_pipeline(np.max, dist)

    logger.info('Maximum value found.')
    logger.debug(output)

    return output


def mean(dist):
    """Measures the mean of a distribution.

    Args:
        dist (Distribution): Distribution to be analyzed.

    Returns:
        Dictionary holding the measure's outputs.

    """

    logger.info('Calculating mean ...')

    # Calculates the mean value of a distribution
    output = w.measure_pipeline(np.mean, dist)

    logger.info('Mean calculated.')
    logger.debug(output)

    return output


def median(dist):
    """Measures the median of a distribution.

    Args:
        dist (Distribution): Distribution to be analyzed.

    Returns:
        Dictionary holding the measure's outputs.

    """

    logger.info('Calculating median ...')

    # Calculates the median value of a distribution
    output = w.measure_pipeline(np.median, dist)

    logger.info('Median calculated.')
    logger.debug(output)

    return output


def min(dist):
    """Measures the minimum value of a distribution.

    Args:
        dist (Distribution): Distribution to be analyzed.

    Returns:
        Dictionary holding the measure's outputs.

    """

    logger.info('Finding minimum value ...')

    # Calculates the minimum value of a distribution
    output = w.measure_pipeline(np.max, dist)

    logger.info('Minimum value found.')
    logger.debug(output)

    return output


def skewness(dist):
    """Measures the skewness of a distribution.

    Args:
        dist (Distribution): Distribution to be analyzed.

    Returns:
        Dictionary holding the measure's outputs.

    """

    logger.info('Calculating skewness ...')

    # Calculates the skewness value of a distribution
    output = w.measure_pipeline(st.skew, dist)

    logger.info('Skewness calculated.')
    logger.debug(output)

    return output


def std(dist):
    """Measures the standard deviation of a distribution.

    Args:
        dist (Distribution): Distribution to be analyzed.

    Returns:
        Dictionary holding the measure's outputs.

    """

    logger.info('Calculating standard deviation ...')

    # Calculates the standard deviation of a distribution
    output = w.measure_pipeline(np.std, dist)

    logger.info('Standard deviation calculated.')
    logger.debug(output)

    return output


def var(dist):
    """Measures the variance of a distribution.

    Args:
        dist (Distribution): Distribution to be analyzed.

    Returns:
        Dictionary holding the measure's outputs.

    """

    logger.info('Calculating variance ...')

    # Calculates the variance of a distribution
    output = w.measure_pipeline(np.var, dist)

    logger.info('Variance calculated.')
    logger.debug(output)

    return output
