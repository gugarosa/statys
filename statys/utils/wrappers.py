"""Wraps common-based functions for easier development.
"""


def calculate_hypothesis(p, alpha):
    """Calculates whether hypothesis' rejection fails or not according to a significance value.

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


def measure_pipeline(measure, dist, **kwargs):
    """Wraps the pipeline of conducting a measure.

    Args:
        measure (pointer): Pointer to a measure function.
        dist (Distribution): Distribution to be analyzed.

    Returns:
        Dictionary holding the test's outputs.

    """

    # Initializes a empty dictionary for the outputs
    output = {}

    # Iterates through every attribute in the distribution
    for (attr, value) in dist.attrs:
        # Calculates the measure
        output[attr] = measure(value, **kwargs)

    return output


def statistical_pipeline(test, dist, alpha):
    """Wraps the pipeline of conducting a statistical test and calculating its hypothesis.

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
                h = calculate_hypothesis(p, alpha)

                # Adds the tuple to the output dictionary
                output[key] = (h, p)

    return output
