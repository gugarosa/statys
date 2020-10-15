"""Critical difference-based plotting utilities. Note that is an improved version of the script provided
by https://github.com/biolab/orange3.
"""


import matplotlib.pyplot as plt
import numpy
from matplotlib.backends.backend_agg import FigureCanvasAgg
from matplotlib.figure import Figure


def _create_labels(size=1):
    """Creates a list of labels strings.

    Args:
        size (int): Amount of strings to be created.

    Returns:
        A list of stringed labels, e.g., arg0, arg1, ..., argn.

    """

    # Creates a list of empty labels
    labels = []

    # Iterates through every possible size
    for i in range(size):
        # Appends the label string
        labels.append(f'$arg_{i}$')

    return labels


def _multiple_range(l):
    """Performs a multiple range, used to traverse matrices.

    Args:
        l (List): List to be traversed.

    Yields:
        An iterator of tuples.

    """

    # Checks if list does not exists
    if not len(l):
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


# def _plot_text(x, y, s, *args, **kwargs):
#     """
#     """

#     #
#     ax.text(width_factor * x, height_factor * y, s, *args, **kwargs)


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
    pairs = [(i, j)
             for i, j in _multiple_range([[n_ranks], [n_ranks]]) if j > i]

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
        sort_operator = sorted([(r, i)
                                for i, r in enumerate(ranks)], reverse=reverse)

        # Gathers the sorted ranks and their indexes
        sort_ranks, sort_idx = _get_element(
            sort_operator, 0), _get_element(sort_operator, 1)

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

        # Plots the first line
        _plot_line(ax, [(text_spacing, top_distance), (width - text_spacing, top_distance)], width_factor, height_factor, linewidth=0.7)

        # Defines regular, big and small ticks sizes
        big_tick = 0.1
        small_tick = 0.05

        def text(x, y, s, *args, **kwargs):
        #
            ax.text(width_factor * x, height_factor * y, s, *args, **kwargs)
        
        # Iterates over every possible value between low and high
        for a in list(numpy.arange(low, high, 0.5)) + [high]:
            # Gathers the current tick as smallest one
            tick = small_tick

            if a == int(a):
                tick = big_tick
            _plot_line(ax, [(_position_rank(a, low, high, text_spacing, scale, reverse), top_distance - tick / 2),
                  (_position_rank(a, low, high, text_spacing, scale, reverse), top_distance)], width_factor, height_factor, linewidth=0.7)

        for a in range(low, high + 1):
            text(_position_rank(a, low, high, text_spacing, scale, reverse),
                 top_distance - tick / 2 - 0.05, str(a), ha="center", va="bottom")

        for i in range(int((n_ranks + 1) / 2)):
            chei = top_distance + not_sig_distance + i * 0.2
            _plot_line(ax, [(_position_rank(sort_ranks[i], low, high, text_spacing, scale, reverse), top_distance), (_position_rank(
                sort_ranks[i], low, high, text_spacing, scale, reverse), chei), (text_spacing - 0.1, chei)], width_factor, height_factor, linewidth=0.7)
            text(text_spacing - 0.2, chei,
                 sort_labels[i], ha="right", va="center")

        for i in range(int((n_ranks + 1) / 2), n_ranks):
            chei = top_distance + not_sig_distance + (n_ranks - i - 1) * 0.2
            _plot_line(ax, [(_position_rank(sort_ranks[i], low, high, text_spacing, scale, reverse), top_distance), (_position_rank(
                sort_ranks[i], low, high, text_spacing, scale, reverse), chei), (text_spacing + scale + 0.1, chei)], width_factor, height_factor, linewidth=0.7)
            text(text_spacing + scale + 0.2, chei,
                 sort_labels[i], ha="left", va="center")

        # begin, end = _position_rank(high, low, high, text_spacing, scale), _position_rank(
            # high - cd, low, high, text_spacing, scale)
        begin, end = _position_rank(low, low, high, text_spacing, scale, reverse), _position_rank(
            low + cd, low, high, text_spacing, scale, reverse)

        # print(begin, end, low, high, cd)

        _plot_line(ax, [(begin, height_distance), (end, height_distance)], width_factor, height_factor, linewidth=0.7)
        _plot_line(ax, [(begin, height_distance + big_tick / 2),
              (begin, height_distance - big_tick / 2)], width_factor, height_factor, linewidth=0.7)
        _plot_line(ax, [(end, height_distance + big_tick / 2),
              (end, height_distance - big_tick / 2)], width_factor, height_factor, linewidth=0.7)
        text((begin + end) / 2, height_distance - 0.05, "CD=" +
             str('%.4f' % float(cd)), ha="center", va="bottom")

        # non significance lines
        def draw_lines(lines, side=0.05, height=0.1):
            start = top_distance + 0.2
            for l, r in lines:
                _plot_line(ax, [(_position_rank(sort_ranks[l], low, high, text_spacing, scale, reverse) - side, start),
                      (_position_rank(sort_ranks[r], low, high, text_spacing, scale, reverse) + side, start)], width_factor, height_factor, linewidth=2.5)
                start += height

        draw_lines(n_lines)

        canvas = FigureCanvasAgg(fig)
        canvas.print_figure(f'file_{key}.pdf')
