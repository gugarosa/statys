"""Critical difference-based plotting utilities.
"""

import matplotlib.pyplot as plt


def _rank_position(index, low, high, spacing, scale):
    """
    """

    #
    x = high - index

    return spacing + scale / (high - low) * x


def plot_critical_difference(cd_dict, width=6, spacing=2):
    """
    """

    #
    scale = width - 2 * spacing

    # Iterates through every dictionary item
    for k, v in cd_dict.items():
        #
        low, high = 1, v[0].shape[0]

        #
        cd = v[1]

        #
        start_pos = _rank_position(high, low, high, spacing, scale)

        #
        end_pos = _rank_position(high - cd, low, high, spacing, scale)

        print(start_pos, end_pos, low, high, cd)
