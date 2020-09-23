"""Statistical-related measures.
"""

import numpy as np

import statys.utils.logging as l
import statys.utils.wrappers as w

logger = l.get_logger(__name__)


def max(dist):
    """Measures the maximum value of a distribution.

    Args:
        dist (Distribution): Distribution to be analyzed.

    Returns:
        Dictionary holding the measure's outputs.

    """

    logger.debug('Finding maximum value ...')

    # Calculates the maximum value of a distribution
    output = w.measure_pipeline(np.max, dist)

    logger.debug('Maximum value found.')

    return output


def mean(dist):
    """Measures the mean of a distribution.

    Args:
        dist (Distribution): Distribution to be analyzed.

    Returns:
        Dictionary holding the measure's outputs.

    """

    logger.debug('Calculating mean ...')

    # Calculates the mean value of a distribution
    output = w.measure_pipeline(np.mean, dist)

    logger.debug('Mean calculated.')

    return output


def min(dist):
    """Measures the minimum value of a distribution.

    Args:
        dist (Distribution): Distribution to be analyzed.

    Returns:
        Dictionary holding the measure's outputs.

    """

    logger.debug('Finding minimum value ...')

    # Calculates the minimum value of a distribution
    output = w.measure_pipeline(np.max, dist)

    logger.debug('Minimum value found.')

    return output


def std(dist):
    """Measures the standard deviation of a distribution.

    Args:
        dist (Distribution): Distribution to be analyzed.

    Returns:
        Dictionary holding the measure's outputs.

    """

    logger.debug('Calculating standard deviation ...')

    # Calculates the standard deviation of a distribution
    output = w.measure_pipeline(np.std, dist)

    logger.debug('Standard deviation calculated.')

    return output
