"""Critical-difference diagrams.

The diagram layout is adapted from the Orange project's plotting code:
https://github.com/biolab/orange3.
"""

from __future__ import annotations

from collections.abc import Sequence
from pathlib import Path
from typing import Any

import numpy as np
from matplotlib.figure import Figure
from numpy.typing import ArrayLike, NDArray


def _maximal_intervals(
    ranks: NDArray[np.float64], critical_difference: float
) -> list[tuple[int, int]]:
    """Find maximal non-significant groups in ascending or descending ranks."""

    intervals: list[tuple[int, int]] = []
    right = 0
    for left in range(len(ranks) - 1):
        right = max(left, right)
        while (
            right + 1 < len(ranks)
            and abs(ranks[left] - ranks[right + 1]) <= critical_difference
        ):
            right += 1

        # A window ending no farther right is contained in the previous one.
        if right > left and (not intervals or right > intervals[-1][1]):
            intervals.append((left, right))

    return intervals


def plot_critical_difference(
    ranks: ArrayLike,
    critical_difference: float,
    labels: Sequence[str] | None = None,
    width: float = 6,
    text_spacing: float = 2,
    reverse: bool = False,
    output: str | Path | None = None,
) -> Figure:
    """Create a critical-difference diagram and optionally save it.

    Parameters
    ----------
    ranks : array_like of shape (n_treatments,)
        Average ranks for at least two treatments, normally returned by
        ``statys.nemenyi``. Input order need not be sorted and is not
        modified.
    critical_difference : float
        Non-negative threshold for differences between average ranks.
    labels : sequence of str, optional
        One label per rank, in the same input order. Default labels are
        ``x_0``, ``x_1``, etc.
    width : float, default=6
        Figure width in inches; must exceed twice `text_spacing`.
    text_spacing : float, default=2
        Horizontal space in inches reserved for labels on each side.
    reverse : bool, default=False
        Display ranks in decreasing order from left to right. This
        changes the display, not which score direction receives rank one.
    output : str or pathlib.Path, optional
        Save destination, with format inferred by Matplotlib from the
        extension. No file is written when omitted.

    Returns
    -------
    matplotlib.figure.Figure
        A new figure owned by the caller, without opening a GUI window.
        It can be customized through its axes or saved with ``savefig``.
        Thick bars connect maximal groups whose rank differences do not
        exceed the threshold; such groups may overlap.

    Raises
    ------
    ValueError
        If ranks are not one-dimensional with at least two values, the
        threshold is negative, the width does not exceed twice the label
        spacing, or the number of labels differs from the rank count.
        Matplotlib and file-writing errors propagate unchanged.

    See Also
    --------
    statys.nemenyi : Compute average ranks and their critical difference.

    Examples
    --------
    >>> from statys import plot_critical_difference
    >>> figure = plot_critical_difference([1, 2, 3], 1, labels=["A", "B", "C"])
    >>> len(figure.axes)
    1
    """

    ranks = np.asarray(ranks, dtype=float)
    if ranks.ndim != 1 or len(ranks) < 2:
        raise ValueError("ranks must contain at least two values")
    if critical_difference < 0:
        raise ValueError("critical_difference must be non-negative")
    if width <= 2 * text_spacing:
        raise ValueError("width must be greater than twice text_spacing")

    if labels is None:
        labels = [f"$x_{{{index}}}$" for index in range(len(ranks))]
    elif len(labels) != len(ranks):
        raise ValueError("labels and ranks must have the same length")

    order = np.argsort(ranks)
    if reverse:
        order = order[::-1]
    ranks = ranks[order]
    labels = [labels[index] for index in order]

    count = len(ranks)
    low, high = 1, count
    intervals = _maximal_intervals(ranks, critical_difference)

    height_distance = 0.25
    top_distance = 0.65
    blank_lines = 0.4 + max(0, len(intervals) - 1) * 0.1
    interval_distance = max(0.4, blank_lines)
    height = top_distance + ((count + 1) / 2) * 0.2 + interval_distance
    scale = width - 2 * text_spacing

    figure = Figure(figsize=(width, height))
    axis = figure.add_axes((0, 0, 1, 1))
    axis.set_axis_off()
    axis.set_xlim(0, 1)
    axis.set_ylim(1, 0)

    def position(rank: float) -> float:
        offset = high - rank if reverse else rank - low
        return text_spacing + scale * offset / (high - low)

    def line(points: Sequence[tuple[float, float]], **kwargs: Any) -> None:
        x, y = zip(*points)
        axis.plot(np.asarray(x) / width, np.asarray(y) / height, **kwargs)

    def text(x: float, y: float, value: str, **kwargs: Any) -> None:
        axis.text(x / width, y / height, value, **kwargs)

    line(
        [(text_spacing, top_distance), (width - text_spacing, top_distance)],
        color="k",
        linewidth=0.7,
    )

    big_tick, small_tick = 0.1, 0.05
    for value in [*np.arange(low, high, 0.5), high]:
        tick = big_tick if float(value).is_integer() else small_tick
        x = position(value)
        line(
            [(x, top_distance - tick / 2), (x, top_distance)],
            color="k",
            linewidth=0.7,
        )

    for value in range(low, high + 1):
        text(
            position(value),
            top_distance - big_tick / 2 - 0.05,
            str(value),
            ha="center",
            va="bottom",
        )

    midpoint = (count + 1) // 2
    for index in range(midpoint):
        arrow = top_distance + interval_distance + index * 0.2
        line(
            [
                (position(ranks[index]), top_distance),
                (position(ranks[index]), arrow),
                (text_spacing - 0.1, arrow),
            ],
            color="k",
            linewidth=0.7,
        )
        text(
            text_spacing - 0.2,
            arrow,
            labels[index],
            ha="right",
            va="center",
        )

    for index in range(midpoint, count):
        arrow = top_distance + interval_distance + (count - index - 1) * 0.2
        line(
            [
                (position(ranks[index]), top_distance),
                (position(ranks[index]), arrow),
                (text_spacing + scale + 0.1, arrow),
            ],
            color="k",
            linewidth=0.7,
        )
        text(
            text_spacing + scale + 0.2,
            arrow,
            labels[index],
            ha="left",
            va="center",
        )

    anchor = high if reverse else low
    start = position(anchor)
    end = position(
        anchor - critical_difference if reverse else anchor + critical_difference
    )
    line(
        [(start, height_distance), (end, height_distance)],
        color="k",
        linewidth=0.7,
    )
    for point in (start, end):
        line(
            [
                (point, height_distance + big_tick / 2),
                (point, height_distance - big_tick / 2),
            ],
            color="k",
            linewidth=0.7,
        )
    text(
        (start + end) / 2,
        height_distance - 0.05,
        f"CD={critical_difference:.3g}",
        ha="center",
        va="bottom",
    )

    interval_height = top_distance + 0.2
    for left, right in intervals:
        line(
            [
                (position(ranks[left]) - 0.05, interval_height),
                (position(ranks[right]) + 0.05, interval_height),
            ],
            color="k",
            linewidth=2.5,
        )
        interval_height += 0.1

    if output is not None:
        figure.savefig(output)

    return figure
