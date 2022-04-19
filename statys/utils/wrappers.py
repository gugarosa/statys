"""Wraps common-based functions for easier development.
"""


from typing import Any, Dict

from statys.core.distribution import Distribution


def calculate_hypothesis(p: float, alpha: float) -> bool:
    """Calculates whether hypothesis' rejection fails or not according to a significance value.

    Args:
        p: P-value from a statistical test.
        alpha: Significance value.

    Returns:
        (bool): 1 if hypothesis is rejected and 0 if it failed to be rejected.

    """

    if p >= alpha:
        # If yes, indicates a failure to reject the null hypothesis
        h = 0

    else:
        # Hypothesis should be rejected
        h = 1

    return h


def measure_pipeline(measure: callable, dist: Distribution, **kwargs) -> Dict[str, Any]:
    """Wraps the pipeline of conducting a measure.

    Args:
        measure: Pointer to a measure function.
        dist: Distribution to be analyzed.

    Returns:
        (Dict[str, Any]): Test's outputs.

    """

    # Initializes a empty dictionary for the outputs
    output = {}

    for (attr, value) in dist.attrs:
        # Calculates the measure
        output[attr] = measure(value, **kwargs)

    return output


def statistical_pipeline(
    test: callable, dist: Distribution, alpha: float
) -> Dict[str, Any]:
    """Wraps the pipeline of conducting a statistical test and calculating its hypothesis.

    Args:
        test: Pointer to a statistical test.
        dist: Distribution to be analyzed.
        alpha: Significance value.

    Returns:
        (Dict[str, Any]): Test's outputs.

    """

    # Initializes a empty dictionary for the outputs
    output = {}

    for (attr, value) in dist.attrs:
        for (attr2, value2) in dist.attrs:
            if attr == attr2:
                pass

            else:
                # Creates a key to the dictionary
                key = attr + "-" + attr2

                # Performs the statistical test
                _, p = test(value, value2)

                # Calculates whether hypothesis fails to be rejected or not
                h = calculate_hypothesis(p, alpha)

                # Adds the tuple to the output dictionary
                output[key] = (h, p)

    return output
