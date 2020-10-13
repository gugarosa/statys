"""Statistical-related measures.
"""

import numpy as np
import scipy.stats as st

import statys.utils.logging as l
import statys.utils.wrappers as w

logger = l.get_logger(__name__)


def kurtosis(dist, axis=None):
    """Measures the kurtosis of a distribution.

    Args:
        dist (Distribution): Distribution to be analyzed.
        axis (int): Axis to conduct the measure.

    Returns:
        Dictionary holding the measure's outputs.

    """

    logger.info('Calculating kurtosis ...')

    # Calculates the kurtosis value of a distribution
    output = w.measure_pipeline(st.kurtosis, dist, axis)

    logger.info('Kurtosis calculated.')
    logger.debug(output)

    return output


def max(dist, axis=None):
    """Measures the maximum value of a distribution.

    Args:
        dist (Distribution): Distribution to be analyzed.
        axis (int): Axis to conduct the measure.

    Returns:
        Dictionary holding the measure's outputs.

    """

    logger.info('Finding maximum value ...')

    # Calculates the maximum value of a distribution
    output = w.measure_pipeline(np.max, dist, axis)

    logger.info('Maximum value found.')
    logger.debug(output)

    return output


def mean(dist, axis=None):
    """Measures the mean of a distribution.

    Args:
        dist (Distribution): Distribution to be analyzed.
        axis (int): Axis to conduct the measure.

    Returns:
        Dictionary holding the measure's outputs.

    """

    logger.info('Calculating mean ...')

    # Calculates the mean value of a distribution
    output = w.measure_pipeline(np.mean, dist, axis)

    logger.info('Mean calculated.')
    logger.debug(output)

    return output


def median(dist, axis=None):
    """Measures the median of a distribution.

    Args:
        dist (Distribution): Distribution to be analyzed.
        axis (int): Axis to conduct the measure.

    Returns:
        Dictionary holding the measure's outputs.

    """

    logger.info('Calculating median ...')

    # Calculates the median value of a distribution
    output = w.measure_pipeline(np.median, dist, axis)

    logger.info('Median calculated.')
    logger.debug(output)

    return output


def min(dist, axis=None):
    """Measures the minimum value of a distribution.

    Args:
        dist (Distribution): Distribution to be analyzed.
        axis (int): Axis to conduct the measure.

    Returns:
        Dictionary holding the measure's outputs.

    """

    logger.info('Finding minimum value ...')

    # Calculates the minimum value of a distribution
    output = w.measure_pipeline(np.max, dist, axis)

    logger.info('Minimum value found.')
    logger.debug(output)

    return output


def skewness(dist, axis=None):
    """Measures the skewness of a distribution.

    Args:
        dist (Distribution): Distribution to be analyzed.
        axis (int): Axis to conduct the measure.

    Returns:
        Dictionary holding the measure's outputs.

    """

    logger.info('Calculating skewness ...')

    # Calculates the skewness value of a distribution
    output = w.measure_pipeline(st.skew, dist, axis)

    logger.info('Skewness calculated.')
    logger.debug(output)

    return output


def std(dist, axis=None):
    """Measures the standard deviation of a distribution.

    Args:
        dist (Distribution): Distribution to be analyzed.
        axis (int): Axis to conduct the measure.

    Returns:
        Dictionary holding the measure's outputs.

    """

    logger.info('Calculating standard deviation ...')

    # Calculates the standard deviation of a distribution
    output = w.measure_pipeline(np.std, dist, axis)

    logger.info('Standard deviation calculated.')
    logger.debug(output)

    return output


def var(dist, axis=None):
    """Measures the variance of a distribution.

    Args:
        dist (Distribution): Distribution to be analyzed.
        axis (int): Axis to conduct the measure.

    Returns:
        Dictionary holding the measure's outputs.

    """

    logger.info('Calculating variance ...')

    # Calculates the variance of a distribution
    output = w.measure_pipeline(np.var, dist, axis)

    logger.info('Variance calculated.')
    logger.debug(output)

    return output
