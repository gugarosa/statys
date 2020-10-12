"""
"""

import numpy as np
import matplotlib.colors as clr
import matplotlib.pyplot as plt

def _create_labels(size=1):
    """
    """

    #
    labels = []

    #
    for i in range(size):
        #
        labels.append(f'arg{i}')

    return labels


def plot_similarity(sim_dict, labels=None):
    """
    """

    # Calculates the number of arguments by solving: y = x^2 - x
    n_args = int(np.roots([1, -1, -len(sim_dict)])[0])

    # Instantiates the similarity matrix
    sims = np.zeros((n_args, n_args))

    # Creates the figure and its axis
    _, ax = plt.subplots(figsize=(7, 5))

    # Checks if labels exists and number of supplied labels equals the number of arguments
    if labels and len(labels) == n_args:
        # If yes, it is good to go
        pass

    # If not
    else:
        # Re-creates the labels list
        labels = _create_labels(n_args)

    # Defines axis properties
    ax.set_xticks(np.arange(0, n_args, 1))
    ax.set_xticklabels(labels)
    ax.set_yticks(np.arange(0, n_args, 1))
    ax.set_yticklabels(labels)

    # Sets title and defines the grid
    ax.set_title('title')
    ax.grid(which='minor', color='k')

    # Creates the color map
    color_map = clr.LinearSegmentedColormap.from_list('ColorMap', [(1.000, 1.000, 1.000), (0.984, 0.501, 0.447)])

    # Adds the similarities to the plot
    ax.imshow(sims, cmap=color_map, interpolation='none')

    # Displays the plot
    plt.show()
