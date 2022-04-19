"""Friedman-related tests and their post-hocs.
"""

import numpy as np

import statys.tests.measure as m
import statys.utils.constants as c
from statys.utils import logging

logger = logging.get_logger(__name__)


def friedman(dist, **kwargs):
    """Performs the Friedman test.

    Args:
        dist (Distribution): Distribution to be analyzed.

    Returns:
        Dictionary holding the test's outputs.

    """

    logger.info("Performing Friedman test ...")

    # Initializes a empty dictionary for the outputs
    output = {}

    # Computes the average ranks (axis keyword should be used accordingly)
    average_ranks = m.rank(dist, **kwargs)

    for key, val in average_ranks.items():
        # Initializes the number of measurements as one
        n = 1

        # If argument has more than one measurement
        if val.ndim > 1:
            # Gathers the number of measurements
            n = val.shape[0]

            # Averages its rankings
            val = np.mean(val, axis=0)

        # Gathers the amount of ranks
        k = len(val)

        # Calculates the Friedman's statistic
        f = (
            12
            * n
            * (sum([v**2.0 for v in val]) - (k * (k + 1) * (k + 1) / 4))
            / (k * (k + 1))
        )

        # Calculates the F-distribution
        f_dist = (k - 1, (k - 1) * (n - 1))

        # Calculates the Iman's statistic
        iman = (n - 1) * f / (n * (k - 1) - f)

        # Adds the tuple to the output dictionary
        output[key] = (f, k - 1), (iman, f_dist)

    logger.info("Test performed.")
    logger.debug(output)

    return output


def friedman_with_posthoc(dist, alpha=0.05, post_hoc="nemenyi", **kwargs):
    """Performs the Friedman test with a post-hoc analysis.

    Args:
        dist (Distribution): Distribution to be analyzed.
        alpha (float): Significance value.
        post_hoc (str): Type of post-hoc analysis.

    Returns:
        Dictionary holding the test's outputs.

    """

    logger.info("Performing Friedman-%s test ...", post_hoc)

    # Initializes a empty dictionary for the outputs
    output = {}

    # Computes the average ranks (axis keyword should be used accordingly)
    average_ranks = m.rank(dist, **kwargs)

    if alpha == 0.01:
        critical_index = 0

    elif alpha == 0.05:
        critical_index = 1

    elif alpha == 0.1:
        critical_index = 2

    # Gathers the corresponding critical values
    q = np.asarray(c.CRITICAL_VALUES[post_hoc])[:, critical_index]

    for key, val in average_ranks.items():
        # Initializes the number of measurements as one
        n = 1

        # If argument has more than one measurement
        if val.ndim > 1:
            # Gathers the number of measurements
            n = val.shape[0]

            # Averages its rankings
            val = np.mean(val, axis=0)

        # Gathers the amount of ranks
        k = len(val)

        # Calculates the critical difference
        cd = q[k - 1] * (k * (k + 1) / (6 * n)) ** 0.5

        # Adds the tuple to the output dictionary
        output[key] = (val, cd)

    logger.info("Test performed.")
    logger.debug(output)

    return output
