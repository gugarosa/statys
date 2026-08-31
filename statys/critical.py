"""Critical-difference diagrams."""

from itertools import combinations
from pathlib import Path
from collections.abc import Sequence

import numpy as np
from matplotlib.figure import Figure


def _maximal_intervals(ranks: np.ndarray, critical_difference: float):
    intervals = [
        (left, right)
        for left, right in combinations(range(len(ranks)), 2)
        if abs(ranks[left] - ranks[right]) <= critical_difference
    ]
    return [
        (left, right)
        for left, right in intervals
        if not any(
            (outer_left <= left and outer_right > right)
            or (outer_left < left and outer_right >= right)
            for outer_left, outer_right in intervals
        )
    ]


def plot_critical_difference(
    ranks: Sequence[float],
    critical_difference: float,
    labels: Sequence[str] | None = None,
    width: float = 6,
    text_spacing: float = 2,
    reverse: bool = False,
    output: str | Path | None = None,
) -> Figure:
    """Create a critical-difference diagram and optionally save it."""

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
    axis = figure.add_axes([0, 0, 1, 1])
    axis.set_axis_off()
    axis.set_xlim(0, 1)
    axis.set_ylim(1, 0)

    def position(rank: float) -> float:
        offset = high - rank if reverse else rank - low
        return text_spacing + scale * offset / (high - low)

    def line(points, **kwargs) -> None:
        x, y = zip(*points)
        axis.plot(np.asarray(x) / width, np.asarray(y) / height, **kwargs)

    def text(x: float, y: float, value: str, **kwargs) -> None:
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
    end = position(anchor - critical_difference if reverse else anchor + critical_difference)
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
