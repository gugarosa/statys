import numpy as np


def max(analyzer):
    """
    """

    #
    output = {}

    #
    for (attr, value) in analyzer.attrs:
        output[attr] = np.max(value)

    return output


def mean(analyzer):
    """
    """

    #
    output = {}

    #
    for (attr, value) in analyzer.attrs:
        output[attr] = np.mean(value)

    return output


def min(analyzer):
    """
    """

    #
    output = {}

    #
    for (attr, value) in analyzer.attrs:
        output[attr] = np.min(value)

    return output


def std(analyzer):
    """
    """

    #
    output = {}

    #
    for (attr, value) in analyzer.attrs:
        output[attr] = np.std(value)

    return output
