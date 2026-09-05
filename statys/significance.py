"""Significance and p-value matrix plots.

Inputs are result dictionaries from ``statys.pairwise``. Both matrix halves
display the same stored comparison; a one-sided test keeps the direction of
its original argument order, not the direction of a matrix cell. Missing
comparisons are left blank.
"""

import re
from pathlib import Path

import numpy as np
from matplotlib.figure import Figure


def _matrix(results, value_index, diagonal):
    if not results:
        raise ValueError("at least one pairwise result is required")

    pairs = []
    for key, result in results.items():
        match = (
            re.fullmatch(r"arg([0-9]+)-arg([0-9]+)", key)
            if isinstance(key, str)
            else None
        )
        if match is None:
            raise ValueError(f"invalid pairwise result key: {key!r}")
        left, right = map(int, match.groups())
        if left == right:
            raise ValueError(f"invalid pairwise result key: {key!r}")
        pairs.append((left, right, result[value_index]))

    size = max(max(left, right) for left, right, _ in pairs) + 1
    matrix = np.full((size, size), np.nan)
    np.fill_diagonal(matrix, diagonal)
    for left, right, value in pairs:
        matrix[left, right] = matrix[right, left] = value
    return matrix


def _plot(matrix, color_map, labels, title, formatter, output, colors=None):
    size = len(matrix)
    if labels is None:
        labels = [f"$arg_{{{index}}}$" for index in range(size)]
    elif len(labels) != size:
        raise ValueError("labels and matrix must have the same length")

    figure = Figure()
    axis = figure.subplots()
    axis.set_xticks(np.arange(size), labels=labels)
    axis.set_yticks(np.arange(size), labels=labels)
    axis.tick_params(top=True, bottom=False, labeltop=True, labelbottom=False)
    axis.set_title(title)
    axis.set_xticks(np.arange(size + 1) - 0.5, minor=True)
    axis.set_yticks(np.arange(size + 1) - 0.5, minor=True)
    axis.grid(which="minor", color="w", linewidth=3)
    axis.tick_params(which="minor", bottom=False, left=False)
    for spine in axis.spines.values():
        spine.set_visible(False)

    for (row, column), value in np.ndenumerate(matrix):
        if not np.isnan(value):
            axis.text(
                column,
                row,
                formatter(value),
                ha="center",
                va="center",
            )
    axis.imshow(matrix if colors is None else colors, cmap=color_map, vmin=0, vmax=1)

    if output is not None:
        figure.savefig(output)
    return figure


def plot_p_value(
    results,
    color_map="YlOrRd",
    labels=None,
    title=None,
    output: str | Path | None = None,
) -> Figure:
    """Plot p-values, coloring ``1 - p`` on a fixed zero-to-one scale.

    Annotations show the original p-values. Lower p-values receive stronger
    colors with the default colormap, consistently across separate plots.
    """

    matrix = _matrix(results, value_index=1, diagonal=1)
    return _plot(
        matrix,
        color_map,
        labels,
        title,
        lambda value: f"{value:.3f}",
        output,
        colors=1 - matrix,
    )


def plot_h_index(
    results,
    color_map="YlOrRd",
    labels=None,
    title=None,
    output: str | Path | None = None,
) -> Figure:
    """Plot pairwise null-hypothesis rejection indicators."""

    matrix = _matrix(results, value_index=0, diagonal=0)
    return _plot(
        matrix,
        color_map,
        labels,
        title,
        lambda value: str(int(value)),
        output,
    )
