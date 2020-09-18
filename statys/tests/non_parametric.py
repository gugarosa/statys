"""Non-parametric-related tests.
"""

import scipy.stats as s

import statys.utils.logging as l

logger = l.get_logger(__name__)


def mann_whitney(dist, alpha=0.05):
    """Performs the Mann-Whitney test.

    Args:
        dist (Distribution): Distribution to be analyzed.
        alpha (float): Significance value.

    Returns:
        Dictionary holding the test's outputs.

    """

    logger.debug('Performing Mann-Whitney test ...')

    # Initializes a empty dictionary for the outputs
    output = {}

    logger.debug('Test performed.')

    return output


def wilcoxon_signed_rank(dist, alpha=0.05):
    """Performs the Wilcoxon signed-rank test.

    Args:
        dist (Distribution): Distribution to be analyzed.
        alpha (float): Significance value.

    Returns:
        Dictionary holding the test's outputs.

    """

    logger.debug('Performing Wilcoxon signed-rank test ...')

    # Initializes a empty dictionary for the outputs
    output = {}

    #
    for (attr, value) in dist.attrs:
        for (attr2, value2) in dist.attrs:
            if attr == attr2:
                pass
            else:
                # print(value, value2)
                _, p = s.wilcoxon(value, value2)

                if p >= alpha:
                    h = 0
                else:
                    h = 1

                output[attr] = (h, p)

    logger.debug('Test performed.')

    return output


def wilcoxon_rank_sum(dist, alpha=0.05):
    """Performs the Wilcoxon rank-sum test.

    Args:
        dist (Distribution): Distribution to be analyzed.
        alpha (float): Significance value.

    Returns:
        Dictionary holding the test's outputs.

    """

    logger.debug('Performing Wilcoxon rank-sum test ...')

    # Initializes a empty dictionary for the outputs
    output = {}

    #
    for (attr, value) in dist.attrs:
        for (attr2, value2) in dist.attrs:
            if attr == attr2:
                pass
            else:
                # print(value, value2)
                _, p = s.ranksums(value, value2)

                if p >= alpha:
                    h = 0
                else:
                    h = 1

                output[attr] = (h, p)

    logger.debug('Test performed.')

    return output
