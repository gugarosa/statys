"""Significance-based plotting utilities, such as h-index and p-value.
"""

from typing import Any, Dict, List, Optional

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.axis import Axis


def _create_labels(size: Optional[int] = 1) -> List[str]:
    """Creates a list of labels strings.

    Args:
        size: Amount of strings to be created.

    Returns:
        (List[str]): Stringed labels, e.g., arg0, arg1, ..., argn.

    """

    labels = []

    for i in range(size):
        labels.append(f"$arg_{{{i}}}$")

    return labels


def _prepare_plot(n_args: int, labels: List[str], title: str) -> Axis:
    """Prepares the plot with common definitions.

    Args:
        n_args: Number of arguments.
        labels: List of stringed labels.
        title: Title to be displayed.

    Returns:
        (Axis): Axis property from the plot.

    """

    # Creates the figure and its axis
    _, ax = plt.subplots()

    # Checks if labels exists and number of supplied labels equals the number of arguments
    if labels and len(labels) == n_args:
        pass

    else:
        # Re-creates the labels list
        labels = _create_labels(n_args)

    # Defines axis properties
    ax.set_xticks(np.arange(0, n_args, 1))
    ax.set_xticklabels(labels)
    ax.set_yticks(np.arange(0, n_args, 1))
    ax.set_yticklabels(labels)
    ax.tick_params(top=True, bottom=False, labeltop=True, labelbottom=False)

    # Defines grid properties
    ax.set_title(title)
    ax.set_xticks(np.arange(n_args + 1) - 0.5, minor=True)
    ax.set_yticks(np.arange(n_args + 1) - 0.5, minor=True)
    ax.grid(which="minor", color="w", linestyle="-", linewidth=3)
    ax.tick_params(which="minor", bottom=False, left=False)

    # Iterates through every spine
    for _, spine in ax.spines.items():
        # Removes the outline border
        spine.set_visible(False)

    return ax


def plot_p_value(
    p_dict: Dict[str, Any],
    color_map: Optional[str] = "YlOrRd",
    labels: Optional[List[str]] = None,
    title: Optional[str] = None,
) -> None:
    """Plots a p-value grid according to statistical results.

    Args:
        p_dict: Significances and p-values.
        color_map: Color map from matplotlib.
        labels: Stringed labels.
        title: Title to be displayed.

    """

    # Calculates the number of arguments by solving: y = x^2 - x
    n_args = round(np.roots([1, -1, -len(p_dict)])[0])

    # Prepares the plot using common-based definitions
    ax = _prepare_plot(n_args, labels, title)

    # Instantiates the p-valued matrix
    p = np.zeros((n_args, n_args))

    for k, v in p_dict.items():
        # Gathers the positions from the arguments
        args = k.replace("arg", "").split("-")

        # Transforms the positions into integers
        i, j = int(args[0]), int(args[1])

        # Replaces its value
        p[i][j] = 1 - v[1]

    # Iterates through the p-valued matrix
    for (i, j), z in np.ndenumerate(p):
        # Applies the corresponding value to the position
        ax.text(j, i, "{:0.3f}".format(1 - z), ha="center", va="center")

    # Adds the significances to the plot
    ax.imshow(p, cmap=color_map)

    # Displays the plot
    plt.show()


def plot_h_index(
    h_dict: Dict[str, Any],
    color_map: Optional[str] = "YlOrRd",
    labels: Optional[List[str]] = None,
    title: Optional[str] = None,
) -> None:
    """Plots an h-index grid according to statistical results.

    Args:
        h_dict: H-indexes and p-values.
        color_map: Color map from matplotlib.
        labels: Stringed labels.
        title: Title to be displayed.

    """

    # Calculates the number of arguments by solving: y = x^2 - x
    n_args = round(np.roots([1, -1, -len(h_dict)])[0])

    # Prepares the plot using common-based definitions
    ax = _prepare_plot(n_args, labels, title)

    # Instantiates the significance matrix
    sigs = np.zeros((n_args, n_args), dtype="int")

    for k, v in h_dict.items():
        # Gathers the positions from the arguments
        args = k.replace("arg", "").split("-")

        # Transforms the positions into integers
        i, j = int(args[0]), int(args[1])

        # Replaces its value
        sigs[i][j] = v[0]

    # Iterates through the significance matrix
    for (i, j), z in np.ndenumerate(sigs):
        # Applies the corresponding value to the position
        ax.text(j, i, z, ha="center", va="center")

    # Adds the significances to the plot
    ax.imshow(sigs, cmap=color_map)

    # Displays the plot
    plt.show()
