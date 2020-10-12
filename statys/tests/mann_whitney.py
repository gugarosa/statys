"""Mann-Whitney-related tests.
"""

import scipy.stats as s

import statys.utils.logging as l
import statys.utils.wrappers as w

logger = l.get_logger(__name__)


def u_test(dist, alpha=0.05):
    """Performs the Mann-Whitney U test.

    Args:
        dist (Distribution): Distribution to be analyzed.
        alpha (float): Significance value.

    Returns:
        Dictionary holding the test's outputs.

    """

    logger.info('Performing Mann-Whitney U test ...')

    # Performs the Mann-Whitney test
    output = w.statistical_pipeline(s.mannwhitneyu, dist, alpha)

    logger.info('Test performed.')
    logger.debug(output)

    return output
