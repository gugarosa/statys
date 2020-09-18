"""Statistical-related measures.
"""

import numpy as np

import statys.utils.logging as l

logger = l.get_logger(__name__)


def max(dist):
    """Measures the maximum value of a distribution.

    Args:
        dist (Distribution): Distribution to be analyzed.

    Returns:
        Dictionary holding the measure's outputs.

    """

    logger.debug('Finding maximum value ...')

    # Initializes a empty dictionary for the outputs
    output = {}

    # Iterates through every attribute in the distribution
    for (attr, value) in dist.attrs:
        # Calculates maximum value
        output[attr] = np.max(value)

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

    # Initializes a empty dictionary for the outputs
    output = {}

    # Iterates through every attribute in the distribution
    for (attr, value) in dist.attrs:
        # Calculates mean
        output[attr] = np.mean(value)

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

    # Initializes a empty dictionary for the outputs
    output = {}

    # Iterates through every attribute in the distribution
    for (attr, value) in dist.attrs:
        # Calculates minimum value
        output[attr] = np.min(value)

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

    # Initializes a empty dictionary for the outputs
    output = {}

    # Iterates through every attribute in the distribution
    for (attr, value) in dist.attrs:
        # Calculates standard deviation
        output[attr] = np.std(value)

    logger.debug('Standard deviation calculated.')

    return output
