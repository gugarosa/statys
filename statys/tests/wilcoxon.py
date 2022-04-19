"""Wilcoxon-related tests.
"""

import scipy.stats as s

import statys.utils.wrappers as w
from statys.utils import logging

logger = logging.get_logger(__name__)


def signed_rank(dist, alpha=0.05):
    """Performs the Wilcoxon signed-rank test.

    Args:
        dist (Distribution): Distribution to be analyzed.
        alpha (float): Significance value.

    Returns:
        Dictionary holding the test's outputs.

    """

    logger.info("Performing Wilcoxon signed-rank test ...")

    output = w.statistical_pipeline(s.wilcoxon, dist, alpha)

    logger.info("Test performed.")
    logger.debug(output)

    return output


def rank_sum(dist, alpha=0.05):
    """Performs the Wilcoxon rank-sum test.

    Args:
        dist (Distribution): Distribution to be analyzed.
        alpha (float): Significance value.

    Returns:
        Dictionary holding the test's outputs.

    """

    logger.info("Performing Wilcoxon rank-sum test ...")

    output = w.statistical_pipeline(s.ranksums, dist, alpha)

    logger.info("Test performed.")
    logger.debug(output)

    return output
