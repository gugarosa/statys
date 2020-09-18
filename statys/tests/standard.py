import numpy as np


def max(dist):
    """
    """

    #
    output = {}

    #
    for (attr, value) in dist.attrs:
        output[attr] = np.max(value)

    return output


def mean(dist):
    """
    """

    #
    output = {}

    #
    for (attr, value) in dist.attrs:
        output[attr] = np.mean(value)

    return output


def min(dist):
    """
    """

    #
    output = {}

    #
    for (attr, value) in dist.attrs:
        output[attr] = np.min(value)

    return output


def std(dist):
    """
    """

    #
    output = {}

    #
    for (attr, value) in dist.attrs:
        output[attr] = np.std(value)

    return output
