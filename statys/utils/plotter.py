import numpy as np
import matplotlib.colors as clr
import matplotlib.pyplot as plt


def plot_similarity(dic):
    """
    """

    #
    size = len(dic)

    #
    m = np.zeros((size, size))

    #
    m[0][1] = 0.14
    m[1][0] = 0.14

    # Creates figure and axis
    _, ax = plt.subplots(figsize=(7, 5))

    # Defines `x` axis properties
    ax.set_xticks(np.arange(0, 2, 1))
    ax.set_xticklabels(['arg0', 'arg1'])

    # Defines `y` axis properties
    ax.set_yticks(np.arange(0, 2, 1))
    ax.set_yticklabels(['arg0', 'arg1'])

    # Sets title and subtitle
    ax.set_title('title')

    # Creates the grid
    ax.grid(which='minor', color='k')

    color_map = clr.LinearSegmentedColormap.from_list('ColorMap', [(1.000, 1.000, 1.000), (0.984, 0.501, 0.447)])
    ax.imshow(m, cmap=color_map, interpolation='none')

    # Displays the plot
    plt.show()

