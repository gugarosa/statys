# Copyright (c) 2020-2026 Gustavo de Rosa.
# Licensed under the Apache License, Version 2.0.

"""Significance and p-value matrix plots.

Inputs are result dictionaries from ``statys.pairwise``. Both matrix halves
display the same stored comparison. A one-sided test keeps the direction of
its original argument order, not the direction of a matrix cell. Missing
comparisons are left blank.

"""

from __future__ import annotations

import re
from collections.abc import Callable, Mapping, Sequence
from pathlib import Path

import numpy as np
from matplotlib.colors import Colormap
from matplotlib.figure import Figure
from numpy.typing import NDArray


def _matrix(results: Mapping[str, tuple[int, float]], value_index: int, diagonal: float) -> NDArray[np.float64]:
    if not results:
        raise ValueError("`results` must contain at least one pairwise result.")

    pairs = []
    for key, result in results.items():
        match = re.fullmatch(r"arg([0-9]+)-arg([0-9]+)", key) if isinstance(key, str) else None
        if match is None:
            raise ValueError(f"`key` must use the arg<i>-arg<j> format, but got {key!r}.")
        left, right = map(int, match.groups())
        if left == right:
            raise ValueError(f"`key` must reference distinct samples, but got {key!r}.")

        pairs.append((left, right, result[value_index]))

    size = max(max(left, right) for left, right, _ in pairs) + 1
    matrix = np.full((size, size), np.nan)
    np.fill_diagonal(matrix, diagonal)

    for left, right, value in pairs:
        matrix[left, right] = matrix[right, left] = value

    return matrix


def _plot(
    matrix: NDArray[np.float64],
    color_map: str | Colormap | None,
    labels: Sequence[str] | None,
    title: str | None,
    formatter: Callable[[float], str],
    output: str | Path | None,
    colors: NDArray[np.float64] | None = None,
) -> Figure:
    size = len(matrix)
    if labels is None:
        labels = [f"$arg_{{{index}}}$" for index in range(size)]
    elif len(labels) != size:
        raise ValueError(f"`labels` must have {size} entries, but got {len(labels)}.")

    figure = Figure()
    axis = figure.subplots()

    axis.set_xticks(np.arange(size), labels=labels)
    axis.set_yticks(np.arange(size), labels=labels)
    axis.tick_params(top=True, bottom=False, labeltop=True, labelbottom=False)
    axis.set_title("" if title is None else title)

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
    results: Mapping[str, tuple[int, float]],
    color_map: str | Colormap | None = "YlOrRd",
    labels: Sequence[str] | None = None,
    title: str | None = None,
    output: str | Path | None = None,
) -> Figure:
    """Plot p-values, coloring ``1 - p`` on a fixed zero-to-one scale.

    Args:
        results: Pairwise ``arg{i}-arg{j}`` keys mapped to ``(reject, p_value)`` tuples.
        color_map: Matplotlib colormap name or object, or ``None`` for Matplotlib's configured default.
        labels: Optional labels in sample-index order, including indices with missing comparisons.
        title: Optional axes title.
        output: Optional filename or path for saving the figure.

    Returns:
        Caller-owned Matplotlib figure showing a symmetric matrix of the stored p-values.

    Raises:
        ValueError: Results are empty, a pair key is invalid, or the label count does not match the matrix.

    See Also:
        :func:`statys.significance.plot_h_index`: Display the rejection decisions instead of p-values.

    Notes:
        Sample indices must be distinct and non-negative. Only the p-value is used, and missing comparisons
        remain blank. The label count must be one greater than the largest index. Omitted labels use
        ``arg_0``, ``arg_1``, and subsequent indices.

        Annotations show p-values, including one on the diagonal. Colors use ``1 - p`` on a fixed scale.
        Lower p-values receive stronger colors with ``YlOrRd``, consistently across separate plots.
        Both halves retain the original comparison's direction, not an opposite-direction test.

        No GUI is opened and no file is written unless output is supplied. Matplotlib and file errors propagate.

    Examples:
        >>> from statys import significance
        >>> figure = significance.plot_p_value({"arg0-arg1": (0, 0.2)})
        >>> figure.axes[0].images[0].get_clim()
        (0.0, 1.0)

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
    results: Mapping[str, tuple[int, float]],
    color_map: str | Colormap | None = "YlOrRd",
    labels: Sequence[str] | None = None,
    title: str | None = None,
    output: str | Path | None = None,
) -> Figure:
    """Plot pairwise null-hypothesis rejection indicators.

    Args:
        results: Pairwise ``arg{i}-arg{j}`` keys mapped to ``(reject, p_value)`` tuples.
        color_map: Matplotlib colormap name or object, or ``None`` for Matplotlib's configured default.
        labels: Optional labels in sample-index order, including indices with missing comparisons.
        title: Optional axes title.
        output: Optional filename or path for saving the figure.

    Returns:
        Caller-owned Matplotlib figure showing a symmetric rejection-indicator matrix with a zero diagonal.

    Raises:
        ValueError: Results are empty, a pair key is invalid, or the label count does not match the matrix.

    See Also:
        :func:`statys.significance.plot_p_value`: Display p-values and the shared matrix conventions.

    Notes:
        Sample indices must be distinct and non-negative. The first tuple element is the zero-or-one
        rejection indicator, plotted as supplied rather than recomputed from p-values. Missing pairs remain blank.
        Omitted labels use ``arg_0``, ``arg_1``, and subsequent indices, including those with missing pairs.
        The label count must be one greater than the largest index.

        Both halves retain the original comparison's direction. No GUI is opened, and no file is written
        unless output is supplied. Matplotlib and file errors propagate.

    Examples:
        >>> from statys import significance
        >>> figure = significance.plot_h_index({"arg0-arg1": (1, 0.01)})
        >>> figure.axes[0].images[0].get_array().tolist()
        [[0.0, 1.0], [1.0, 0.0]]

    """

    matrix = _matrix(results, value_index=0, diagonal=0)
    return _plot(
        matrix,
        color_map,
        labels,
        title,
        lambda value: str(int(value)),
        output,
    )
