"""Non-parametric-related tests.
"""

import scipy.stats as s

import statys.utils.logging as l

logger = l.get_logger(__name__)


def _calculate_hypothesis(p, alpha):
    """Calculates whether hypothesis' rejection fails or not.

    Args:
        p (float): P-value from a statistical test.
        alpha (float): Significance value.

    Returns:
        1 if hypothesis is rejected and 0 if it failed to be rejected.

    """

    # Checks if alpha is bigger than significance
    if p >= alpha:
        # If yes, indicates a failure to reject the null hypothesis
        h = 0

    # If alpha is smaller than significance
    else:
        # Hypothesis should be rejected
        h = 1

    return h


def _perform_non_parametric_test(test, dist, alpha):
    """Wraps the pipeline of conducting a non-parametric test and calculating its hypothesis.

    Args:
        test (pointer): Pointer to a statistical test.
        dist (Distribution): Distribution to be analyzed.
        alpha (float): Significance value.

    Returns:
        Dictionary holding the test's outputs.

    """

    # Initializes a empty dictionary for the outputs
    output = {}

    # Iterates through every attribute in the distribution
    for (attr, value) in dist.attrs:
        # Re-iterates through every attribute in the distribution
        for (attr2, value2) in dist.attrs:
            # Checks if `attr` is the same as `attr2`
            if attr == attr2:
                # Ignores if they are the same
                pass

            # If they are not the same
            else:
                # Creates a key to the dictionary
                key = attr + '-' + attr2

                # Performs the statistical test
                _, p = test(value, value2)

                # Calculates whether hypothesis fails to be rejected or not
                h = _calculate_hypothesis(p, alpha)

                # Adds the tuple to the output dictionary
                output[key] = (h, p)

    return output


def mann_whitney(dist, alpha=0.05):
    """Performs the Mann-Whitney test.

    Args:
        dist (Distribution): Distribution to be analyzed.
        alpha (float): Significance value.

    Returns:
        Dictionary holding the test's outputs.

    """

    logger.debug('Performing Mann-Whitney test ...')

    # Performs the Mann-Whitney test
    output = _perform_non_parametric_test(s.mannwhitneyu, dist, alpha)

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

    # Performs the Wilcoxon signed-rank test
    output = _perform_non_parametric_test(s.wilcoxon, dist, alpha)

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

    # Performs the Wilcoxon rank-sum test
    output = _perform_non_parametric_test(s.ranksums, dist, alpha)

    logger.debug('Test performed.')

    return output
