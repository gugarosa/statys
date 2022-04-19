"""Critical difference-based plotting utilities. Note that is an improved version of the script provided
by https://github.com/biolab/orange3.
"""


from typing import Any, Dict, List, Optional, Tuple

import numpy as np
from matplotlib.axis import Axis
from matplotlib.backends.backend_agg import FigureCanvasAgg
from matplotlib.figure import Figure


def _create_labels(size: Optional[int] = 1) -> List[str]:
    """Creates a list of labels strings.

    Args:
        size: Amount of strings to be created.

    Returns:
        (List[str]): Stringed labels, e.g., x0, x1, ..., xn.

    """

    labels = []

    for i in range(size):
        labels.append(f"$x_{{{i}}}$")

    return labels


def _multiple_range(input_list: List[Any]) -> Tuple[Any, ...]:
    """Performs a multiple range, used to traverse matrices.

    Args:
        input_list: List to be traversed.

    Yields:
        (Tuple[Any, ...]): Iterator of tuples.

    """

    length = len(input_list)

    if length == 0:
        yield ()

    else:
        index = input_list[0]

        if isinstance(index, int):
            index = [index]

        for a in range(*index):
            for b in _multiple_range(input_list[1:]):
                yield tuple([a] + list(b))


def _line_factoring(line: List[float], factor: float) -> List[float]:
    """Factors a line's positioning.

    Args:
        line: Lines to be factored.
        factor: Factor to use in the factoring.

    Returns:
        (List[float]): Factored lines.

    """

    return [a * factor for a in line]


def _plot_line(
    ax: Axis,
    input_list: List[Tuple[int, int]],
    width_factor: float,
    height_factor: float,
    color: Optional[str] = "k",
    **kwargs,
) -> None:
    """Plots pairs of points as lines.

    Args:
        ax: Axis to be plotted.
        input_list: List of pairs of points.
        width_factor: Width factor.
        height_factor: Height factor.
        color: Color to be plotted.

    """

    # Calculates the `x` and `y` elements
    x = _line_factoring(_get_element(input_list, 0), width_factor)
    y = _line_factoring(_get_element(input_list, 1), height_factor)

    # Plots the pair of points
    ax.plot(x, y, color=color, **kwargs)


def _plot_text(
    ax: Axis,
    x: int,
    y: int,
    s: str,
    width_factor: float,
    height_factor: float,
    **kwargs,
) -> None:
    """Plots a text on the desired position.

    Args:
        ax: Axis to be plotted.
        x: `x` position to be plotted.
        y: `y` position to be plotted.
        s: String to be plotted.
        width_factor: Width factor.
        height_factor: Height factor.

    """

    # Plots the text itself
    ax.text(width_factor * x, height_factor * y, s, **kwargs)


def _get_amount_lines(ranks: List[int], cd: float) -> List[Tuple[Any, ...]]:
    """Gets the amount of possible lines to create the plot.

    Args:
        ranks: List of ranks.
        cd: Critical difference.

    Returns:
        (List[Tuple[Any, ...]]): Longest possible amount of lines.

    """

    # Calculates the number of possible ranks
    n_ranks = len(ranks)

    # Transforms them into pairs
    pairs = [(i, j) for i, j in _multiple_range([[n_ranks], [n_ranks]]) if j > i]

    # Remove non-significant pairs
    non_pairs = [(i, j) for i, j in pairs if abs(ranks[i] - ranks[j]) <= cd]

    # Internal function to return the longest pairs
    def get_longest(i: int, j: int, pairs: Tuple[int, int]) -> bool:
        for k, l in pairs:
            # Checks if iterated pair is bigger than current one
            if (k <= i and l > j) or (k < i and l >= j):
                return False

        return True

    # Keeps the longest pair
    longest = [(i, j) for i, j in non_pairs if get_longest(i, j, non_pairs)]

    return longest


def _get_element(input_list: List[Any], n: int) -> List[Any]:
    """Gets a specific element from a list of tuples.

    Args:
        input_list: List to be iterated.
        n: Element to be retrieved.

    Returns:
        (List[Any]): Only retrieved elements.

    """

    if n < 0:
        # Adds the length of the list to gather the desired index
        i = len(input_list[0]) + n

    else:
        # Use the index as usual
        i = n

    return [a[i] for a in input_list]


def _calculate_plot_properties(
    sort_ranks: List[int], cd: float
) -> Tuple[int, float, float, int, float, float]:
    """Calculates a set of properties used to accurately plot the statistical test.

    Args:
        sort_ranks: List holding the sorted ranks.
        cd: Critical difference.

    Returns:
        (Tuple[int, float, float, int, float, float]): Properties used in the plot's construction.

    """

    # Gathers the number of possible ranks and (longest) lines
    n_ranks = len(sort_ranks)
    n_lines = _get_amount_lines(sort_ranks, cd)

    # Instantiates the height distance as 0.25 and calculates top distance
    height_distance = 0.25
    top_distance = height_distance + 0.4

    # Calculates the value of the blanked lines
    blank_lines = 0.2 + 0.2 + (len(n_lines) - 1) * 0.1

    # Gathers the position of non-significant samples
    not_sig_distance = max(2 * 0.2, blank_lines)

    # Finally, calculates the plot's height
    height = top_distance + ((n_ranks + 1) / 2) * 0.2 + not_sig_distance

    return n_ranks, height_distance, top_distance, n_lines, not_sig_distance, height


def _prepare_plot(width: float, height: float) -> Tuple[Figure, Axis]:
    """Prepares the plot prior to its use.

    Args:
        width: Width of the plot.
        height: Height of the plot.

    Returns:
        (Tuple[Figure, Axis]): Figure and axis properties from the plot.

    """

    # Creates a new figure based on inputted width and height
    fig = Figure(figsize=(width, height))

    # Adds the corresponding axes to create a box
    ax = fig.add_axes([0, 0, 1, 1])

    # Sets the outer box display as off
    ax.set_axis_off()

    # Plots its boundaries
    ax.plot([0, 1], [0, 1], c="w")

    # Sets the `x` and `y` limits
    ax.set_xlim(0, 1)
    ax.set_ylim(1, 0)

    return fig, ax


def _position_rank(
    index: int, low: int, high: int, text_spacing: int, scale: float, reverse: bool
) -> int:
    """Positions a rank according to its value.

    Args:
        index: Index to be positioned.
        low: Minimum rank possible.
        high: Maximum rank possible.
        text_spacing: Text spacing inside the plot.
        scale: Plot's scale.
        reverse: Whether plot should use ascending or descending order.

    Returns:
        (int): Rank should be positioned in the plot.

    """

    if reverse:
        x = high - index

    else:
        x = index - low

    return text_spacing + scale / (high - low) * x


def plot_critical_difference(
    cd_dict: Dict[str, Any],
    labels: Optional[List[str]] = None,
    width: Optional[int] = 6,
    text_spacing: Optional[int] = 2,
    reverse: Optional[bool] = False,
) -> None:
    """Plots the critical difference between the averaged ranks.

    Args:
        cd_dict: Dictionary of average ranks and critical differences.
        labels: List of stringed labels.
        width: Plot's width.
        text_spacing: Text spacing inside the plot.
        reverse: Whether plot should use ascending or descending order.

    """

    # Defines the plot's scale
    scale = width - 2 * text_spacing

    for key, v in cd_dict.items():
        # Gathers the minimum and maximum possible ranks
        low, high = 1, v[0].shape[0]

        # Gathers current item ranks and its critical difference
        ranks, cd = v[0], v[1]

        # Defines a sorting-based operator
        sort_operator = sorted([(r, i) for i, r in enumerate(ranks)], reverse=reverse)

        # Gathers the sorted ranks and their indexes
        sort_ranks, sort_idx = _get_element(sort_operator, 0), _get_element(
            sort_operator, 1
        )

        # Checks if labels exists and number of supplied labels equals the number of arguments
        if labels and len(labels) == len(ranks):
            pass

        else:
            # Re-creates the labels list
            labels = _create_labels(len(ranks))

        # Gathers the sorted labels as well
        sort_labels = [labels[i] for i in sort_idx]

        # Calculates a set of properties used to perform an accurate plot
        (
            n_ranks,
            height_distance,
            top_distance,
            n_lines,
            not_sig_distance,
            height,
        ) = _calculate_plot_properties(sort_ranks, cd)

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

            if isinstance(a, int):
                # Gathers the current tick as biggest one
                tick = big_tick

            # Defines `x` and `y` points
            x = (
                _position_rank(a, low, high, text_spacing, scale, reverse),
                top_distance - tick / 2,
            )
            y = (
                _position_rank(a, low, high, text_spacing, scale, reverse),
                top_distance,
            )

            # Plots a new line
            _plot_line(ax, [x, y], width_factor, height_factor, linewidth=0.7)

        # Iterates over every possible value between low and high
        # for plotting the text
        for a in range(low, high + 1):
            # Plots the text label
            _plot_text(
                ax,
                _position_rank(a, low, high, text_spacing, scale, reverse),
                top_distance - tick / 2 - 0.05,
                str(a),
                width_factor,
                height_factor,
                ha="center",
                va="bottom",
            )

        # Iterates over every possible left-sided rank
        for i in range(int((n_ranks + 1) / 2)):
            # Calculates the "line-arrow"
            arrow = top_distance + not_sig_distance + i * 0.2

            # Defines `x`, `y` and `z` points
            x = (
                _position_rank(sort_ranks[i], low, high, text_spacing, scale, reverse),
                top_distance,
            )
            y = (
                _position_rank(sort_ranks[i], low, high, text_spacing, scale, reverse),
                arrow,
            )
            z = (text_spacing - 0.1, arrow)

            # Plots a new line
            _plot_line(ax, [x, y, z], width_factor, height_factor, linewidth=0.7)

            # Plots the text label
            _plot_text(
                ax,
                text_spacing - 0.2,
                arrow,
                sort_labels[i],
                width_factor,
                height_factor,
                ha="right",
                va="center",
            )

        # Iterates over every possible right-sided rank
        for i in range(int((n_ranks + 1) / 2), n_ranks):
            # Calculates the "line-arrow"
            arrow = top_distance + not_sig_distance + (n_ranks - i - 1) * 0.2

            # Defines `x`, `y` and `z` points
            x = (
                _position_rank(sort_ranks[i], low, high, text_spacing, scale, reverse),
                top_distance,
            )
            y = (
                _position_rank(sort_ranks[i], low, high, text_spacing, scale, reverse),
                arrow,
            )
            z = (text_spacing + scale + 0.1, arrow)

            # Plots a new line
            _plot_line(ax, [x, y, z], width_factor, height_factor, linewidth=0.7)

            # Plots the text label
            _plot_text(
                ax,
                text_spacing + scale + 0.2,
                arrow,
                sort_labels[i],
                width_factor,
                height_factor,
                ha="left",
                va="center",
            )

        if reverse:
            # Calculates the starting and ending position from `high` values
            start = _position_rank(high, low, high, text_spacing, scale, reverse)
            end = _position_rank(high - cd, low, high, text_spacing, scale, reverse)

        else:
            # Calculates the starting and ending position from `low` values
            start = _position_rank(low, low, high, text_spacing, scale, reverse)
            end = _position_rank(low + cd, low, high, text_spacing, scale, reverse)

        # Plots the starting and ending points of the CD line
        _plot_line(
            ax,
            [(start, height_distance), (end, height_distance)],
            width_factor,
            height_factor,
            linewidth=0.7,
        )

        # Plots the starting ticks of the CD line
        _plot_line(
            ax,
            [
                (start, height_distance + big_tick / 2),
                (start, height_distance - big_tick / 2),
            ],
            width_factor,
            height_factor,
            linewidth=0.7,
        )

        # Plots the ending ticks of the CD line
        _plot_line(
            ax,
            [
                (end, height_distance + big_tick / 2),
                (end, height_distance - big_tick / 2),
            ],
            width_factor,
            height_factor,
            linewidth=0.7,
        )

        # Plots the CD line itself
        _plot_text(
            ax,
            (start + end) / 2,
            height_distance - 0.05,
            f"CD={cd}",
            width_factor,
            height_factor,
            ha="center",
            va="bottom",
        )

        # Plots non-significant lines
        # Defines a new starting point
        start = top_distance + 0.2

        # Iterates over every non-significant line
        for left, right in n_lines:
            # Defines `x` and `y` points
            x = (
                _position_rank(
                    sort_ranks[left], low, high, text_spacing, scale, reverse
                )
                - 0.05,
                start,
            )
            y = (
                _position_rank(
                    sort_ranks[right], low, high, text_spacing, scale, reverse
                )
                + 0.05,
                start,
            )

            # Plots the line
            _plot_line(ax, [x, y], width_factor, height_factor, linewidth=2.5)

            # Adds height to distinguish between lines
            start += 0.1

        # Adding a figure to the canvas
        canvas = FigureCanvasAgg(fig)

        # Printing out the figure
        canvas.print_figure(f"cd_{key}.pdf")
