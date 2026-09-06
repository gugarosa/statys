from itertools import combinations, combinations_with_replacement

import numpy as np
import pytest
from matplotlib.figure import Figure

from statys import plot_critical_difference
from statys.critical import _maximal_intervals


def test_plot_critical_difference(tmp_path):
    output = tmp_path / "critical-difference.pdf"
    figure = plot_critical_difference(
        [1.5, 2.25, 2.25],
        1.657,
        labels=["A", "B", "C"],
        reverse=True,
        output=output,
    )

    assert isinstance(figure, Figure)
    assert output.exists()


def test_maximal_intervals_match_pairwise_non_significance():
    for size in range(2, 7):
        for values in combinations_with_replacement([1, 1.5, 2.5, 4], size):
            for critical_difference in (0, 0.5, 1, 3):
                groups = [
                    set(range(left, right + 1))
                    for left, right in combinations(range(size), 2)
                    if all(
                        abs(values[i] - values[j]) <= critical_difference
                        for i, j in combinations(range(left, right + 1), 2)
                    )
                ]
                expected = sorted(
                    (min(group), max(group))
                    for group in groups
                    if not any(group < other for other in groups)
                )

                assert (
                    _maximal_intervals(np.asarray(values), critical_difference)
                    == expected
                )
                assert _maximal_intervals(
                    np.asarray(values[::-1]), critical_difference
                ) == sorted(
                    (size - 1 - right, size - 1 - left) for left, right in expected
                )


@pytest.mark.parametrize("reverse", [False, True])
def test_diagram_keeps_overlapping_non_significant_groups(reverse):
    figure = plot_critical_difference([1, 2, 3], 1, reverse=reverse)
    groups = [line for line in figure.axes[0].lines if line.get_linewidth() == 2.5]

    assert len(groups) == 2
    np.testing.assert_allclose(groups[0].get_xdata(), np.array([1.95, 3.05]) / 6)
    np.testing.assert_allclose(groups[1].get_xdata(), np.array([2.95, 4.05]) / 6)


@pytest.mark.parametrize("reverse", [False, True])
def test_default_labels_cover_multi_digit_indices(reverse):
    figure = plot_critical_difference(np.arange(1, 12), 1, reverse=reverse)

    assert "$x_{10}$" in {text.get_text() for text in figure.axes[0].texts}
