"""Critical difference-based plotting utilities. Note that is an improved version of the script provided
by https://github.com/biolab/orange3.
"""


import numpy as np
from matplotlib.backends.backend_agg import FigureCanvasAgg
from matplotlib.figure import Figure


def _create_labels(size=1):
    """Creates a list of labels strings.

    Args:
        size (int): Amount of strings to be created.

    Returns:
        A list of stringed labels, e.g., x0, x1, ..., xn.

    """

    # Creates a list of empty labels
    labels = []

    # Iterates through every possible size
    for i in range(size):
        # Appends the label string
        labels.append(f'$x_{i}$')

    return labels


def _multiple_range(l):
    """Performs a multiple range, used to traverse matrices.

    Args:
        l (List): List to be traversed.

    Yields:
        An iterator of tuples.

    """

    # Calculates the list's length
    length = len(l)

    # Checks if list does not exists
    if length == 0:
        # If not, yields an empty tuple
        yield ()

    # If list exists
    else:
        # Gathers the first index
        index = l[0]

        # Checks if it is an integer
        if isinstance(index, int):
            # Transforms it into an indexator
            index = [index]

        # Iterates over the indexes
        for a in range(*index):
            # Recursively call the function
            for b in _multiple_range(l[1:]):
                # Yields the corresponding tuple
                yield tuple([a] + list(b))


def _line_factoring(line, factor):
    """Factors a line's positioning.

    Args:
        line (list): List of lines to be factored.
        factor (float): Factor to use in the factoring.

    Returns:
        A list of factored lines.

    """

    return [a * factor for a in line]


def _plot_line(ax, l, width_factor, height_factor, color='k', **kwargs):
    """Plots pairs of points as lines.

    Args:
        ax (Axis): Axis to be plotted.
        l (list): List of pairs of points.
        width_factor (float): Width factor.
        height_factor (float): Height factor.
        color (str): Color to be plotted.

    """

    # Calculates the `x` element
    x = _line_factoring(_get_element(l, 0), width_factor)

    # Calculates the `y` element
    y = _line_factoring(_get_element(l, 1), height_factor)

    # Plots the pair of points
    ax.plot(x, y, color=color, **kwargs)


def _plot_text(ax, x, y, s, width_factor, height_factor, **kwargs):
    """Plots a text on the desired position.

    Args:
        ax (Axis): Axis to be plotted.
        x (int): `x` position to be plotted.
        y (int): `y` position to be plotted.
        s (str): String to be plotted.
        width_factor (float): Width factor.
        height_factor (float): Height factor.

    """

    # Plots the text itself
    ax.text(width_factor * x, height_factor * y, s, **kwargs)


def _get_amount_lines(ranks, cd):
    """Gets the amount of possible lines to create the plot.

    Args:
        ranks (list): List of ranks.
        cd (float): Critical difference.

    Returns:
        List of tuples containing the longest possible amount of lines.

    """

    # Calculates the number of possible ranks
    n_ranks = len(ranks)

    # Transforms them into pairs
    pairs = [(i, j) for i, j in _multiple_range([[n_ranks], [n_ranks]]) if j > i]

    # Remove non-significant pairs
    non_pairs = [(i, j) for i, j in pairs if abs(ranks[i] - ranks[j]) <= cd]

    # Internal function to return the longest pairs
    def get_longest(i, j, pairs):
        # Iterates over every pair
        for k, l in pairs:
            # Checks if iterated pair is bigger than current one
            if (k <= i and l > j) or (k < i and l >= j):
                # Return false
                return False

        # If no false has been returned, return true
        return True

    # Keeps the longest pair
    longest = [(i, j) for i, j in non_pairs if get_longest(i, j, non_pairs)]

    return longest


def _get_element(l, n):
    """Gets a specific element from a list of tuples.

    Args:
        l (list): List to be iterated.
        n (int): Element to be retrieved.

    Returns:
        A new list with only the retrieved elements.

    """

    # Checks if element's index is negative
    if n < 0:
        # Adds the length of the list to gather the desired index
        i = len(l[0]) + n

    # If element's index is positive
    else:
        # Use the index as usual
        i = n

    return [a[i] for a in l]


def _calculate_plot_properties(sort_ranks, cd):
    """Calculates a set of properties used to accurately plot the statistical test.

    Args:
        sort_ranks (list): List holding the sorted ranks.
        cd (float): Critical difference.

    Returns:
        A set of properties used in the plot's construction.

    """

    # Gathers the number of possible ranks
    n_ranks = len(sort_ranks)

    # Instantiates the height distance as 0.25
    height_distance = 0.25

    # Calculates the value of the top line
    top_distance = height_distance + 0.4

    # Gathers the amount of possible (longest) lines
    n_lines = _get_amount_lines(sort_ranks, cd)

    # Calculates the value of the blanked lines
    blank_lines = 0.2 + 0.2 + (len(n_lines) - 1) * 0.1

    # Gathers the position of non-significant samples
    not_sig_distance = max(2 * 0.2, blank_lines)

    # Finally, calculates the plot's height
    height = top_distance + ((n_ranks + 1) / 2) * 0.2 + not_sig_distance

    return n_ranks, height_distance, top_distance, n_lines, not_sig_distance, height


def _prepare_plot(width, height):
    """Prepares the plot prior to its use.

    Args:
        width (float): Width of the plot.
        height (float): Height of the plot.

    Returns:
        The figure and axis properties from the plot.

    """

    # Creates a new figure based on inputted width and height
    fig = Figure(figsize=(width, height))

    # Adds the corresponding axes to create a box
    ax = fig.add_axes([0, 0, 1, 1])

    # Sets the outer box display as off
    ax.set_axis_off()

    # Plots its boundaries
    ax.plot([0, 1], [0, 1], c='w')

    # Sets the `x` and `y` limits
    ax.set_xlim(0, 1)
    ax.set_ylim(1, 0)

    return fig, ax


def _position_rank(index, low, high, text_spacing, scale, reverse):
    """Positions a rank according to its value.

    Args:
        index (int): Index to be positioned.
        low (int): Minimum rank possible.
        high (int): Maximum rank possible.
        text_spacing (int): Text spacing inside the plot.
        scale (float): Plot's scale.
        reverse (bool): Whether plot should use ascending or descending order.

    Returns:
        A value that indicates where the rank should be positioned in the plot.

    """

    # Checks if the plot is reversed
    if reverse:
        # Calculates `x` with high values
        x = high - index

    # If plot is not reversed
    else:
        # Calculates `x` with low values
        x = index - low

    return text_spacing + scale / (high - low) * x


def plot_critical_difference(cd_dict, labels=None, width=6, text_spacing=2, reverse=False):
    """Plots the critical difference between the averaged ranks.

    Args:
        cd_dict (dict): Dictionary of average ranks and critical differences.
        labels (list): List of stringed labels.
        width (int): Plot's width.
        text_spacing (int): Text spacing inside the plot.
        reverse (bool): Whether plot should use ascending or descending order.

    """

    # Defines the plot's scale
    scale = width - 2 * text_spacing

    # Iterates through every dictionary item
    for key, v in cd_dict.items():
        # Gathers the minimum and maximum possible ranks
        low, high = 1, v[0].shape[0]

        # Gathers current item ranks and its critical difference
        ranks, cd = v[0], v[1]

        # Defines a sorting-based operator
        sort_operator = sorted([(r, i) for i, r in enumerate(ranks)], reverse=reverse)

        # Gathers the sorted ranks and their indexes
        sort_ranks, sort_idx = _get_element(sort_operator, 0), _get_element(sort_operator, 1)

        # Checks if labels exists and number of supplied labels equals the number of arguments
        if labels and len(labels) == len(ranks):
            # If yes, it is good to go
            pass

        # If not
        else:
            # Re-creates the labels list
            labels = _create_labels(len(ranks))

        # Gathers the sorted labels as well
        sort_labels = [labels[i] for i in sort_idx]

        # Calculates a set of properties used to perform an accurate plot
        n_ranks, height_distance, top_distance, n_lines, not_sig_distance, height = _calculate_plot_properties(
            sort_ranks, cd)

        # Prepares the plot based on inputted width and calculated height
        fig, ax = _prepare_plot(width, height)

        # Calculates the width and height factors
        width_factor = 1 / width
        height_factor = 1 / height

        # Defines `x` and `y` points
        x = (text_spacing, top_distance)
        y = (width - text_spacing, top_distance)

        # Plots the first line
        _plot_line(ax, [x, y], width_factor, height_factor, linewidth=0.7)

        # Defines regular, big and small ticks sizes
        big_tick = 0.1
        small_tick = 0.05

        # Iterates over every possible value between low and high
        # for plotting the ticks
        for a in list(np.arange(low, high, 0.5)) + [high]:
            # Gathers the current tick as smallest one
            tick = small_tick

            # Checks if `a` is an integer
            if isinstance(a, int):
                # Gathers the current tick as biggest one
                tick = big_tick

            # Defines `x` and `y` points
            x = (_position_rank(a, low, high, text_spacing, scale, reverse), top_distance - tick / 2)
            y = (_position_rank(a, low, high, text_spacing, scale, reverse), top_distance)

            # Plots a new line
            _plot_line(ax, [x, y], width_factor, height_factor, linewidth=0.7)

        # Iterates over every possible value between low and high
        # for plotting the text
        for a in range(low, high + 1):
            # Plots the text label
            _plot_text(ax, _position_rank(a, low, high, text_spacing, scale, reverse), top_distance -
                       tick / 2 - 0.05, str(a), width_factor, height_factor, ha='center', va='bottom')

        # Iterates over every possible left-sided rank
        for i in range(int((n_ranks + 1) / 2)):
            # Calculates the "line-arrow"
            arrow = top_distance + not_sig_distance + i * 0.2

            # Defines `x`, `y` and `z` points
            x = (_position_rank(sort_ranks[i], low, high, text_spacing, scale, reverse), top_distance)
            y = (_position_rank(sort_ranks[i], low, high, text_spacing, scale, reverse), arrow)
            z = (text_spacing - 0.1, arrow)

            # Plots a new line
            _plot_line(ax, [x, y, z], width_factor, height_factor, linewidth=0.7)

            # Plots the text label
            _plot_text(ax, text_spacing - 0.2, arrow,
                       sort_labels[i], width_factor, height_factor, ha='right', va='center')

        # Iterates over every possible right-sided rank
        for i in range(int((n_ranks + 1) / 2), n_ranks):
            # Calculates the "line-arrow"
            arrow = top_distance + not_sig_distance + (n_ranks - i - 1) * 0.2

            # Defines `x`, `y` and `z` points
            x = (_position_rank(sort_ranks[i], low, high, text_spacing, scale, reverse), top_distance)
            y = (_position_rank(sort_ranks[i], low, high, text_spacing, scale, reverse), arrow)
            z = (text_spacing + scale + 0.1, arrow)

            # Plots a new line
            _plot_line(ax, [x, y, z], width_factor, height_factor, linewidth=0.7)

            # Plots the text label
            _plot_text(ax, text_spacing + scale + 0.2, arrow,
                       sort_labels[i], width_factor, height_factor, ha='left', va='center')

        # Checks if it is supposed to use the reverse order
        if reverse:
            # Calculates the starting and ending position from `high` values
            start = _position_rank(high, low, high, text_spacing, scale, reverse)
            end = _position_rank(high - cd, low, high, text_spacing, scale, reverse)

        # If not
        else:
            # Calculates the starting and ending position from `low` values
            start = _position_rank(low, low, high, text_spacing, scale, reverse)
            end = _position_rank(low + cd, low, high, text_spacing, scale, reverse)

        # Plots the starting and ending points of the CD line
        _plot_line(ax, [(start, height_distance), (end, height_distance)], width_factor, height_factor, linewidth=0.7)

        # Plots the starting ticks of the CD line
        _plot_line(ax, [(start, height_distance + big_tick / 2),
                        (start, height_distance - big_tick / 2)], width_factor, height_factor, linewidth=0.7)

        # Plots the ending ticks of the CD line
        _plot_line(ax, [(end, height_distance + big_tick / 2),
                        (end, height_distance - big_tick / 2)], width_factor, height_factor, linewidth=0.7)

        # Plots the CD line itself
        _plot_text(ax, (start + end) / 2, height_distance - 0.05, f'CD={cd}',
                   width_factor, height_factor, ha='center', va='bottom')

        # Plots non-significant lines
        # Defines a new starting point
        start = top_distance + 0.2

        # Iterates over every non-significant line
        for l, r in n_lines:
            # Defines `x` and `y` points
            x = (_position_rank(sort_ranks[l], low, high, text_spacing, scale, reverse) - 0.05, start)
            y = (_position_rank(sort_ranks[r], low, high, text_spacing, scale, reverse) + 0.05, start)

            # Plots the line
            _plot_line(ax, [x, y], width_factor, height_factor, linewidth=2.5)

            # Adds height to distinguish between lines
            start += 0.1

        # Adding a figure to the canvas
        canvas = FigureCanvasAgg(fig)

        # Printing out the figure
        canvas.print_figure(f'cd_{key}.pdf')
