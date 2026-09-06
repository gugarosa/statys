from types import MappingProxyType

import numpy as np
import pytest
from matplotlib import colormaps, pyplot
from matplotlib.figure import Figure

from statys import significance

RESULTS = {
    "arg0-arg1": (0, 0.2),
    "arg0-arg2": (1, 0.01),
    "arg1-arg2": (1, 0.03),
}


def test_significance_plots(tmp_path):
    p_output = tmp_path / "p-values.pdf"
    h_output = tmp_path / "hypotheses.pdf"

    p_figure = significance.plot_p_value(
        RESULTS,
        labels=["A", "B", "C"],
        output=p_output,
    )
    h_figure = significance.plot_h_index(RESULTS, output=h_output)

    assert isinstance(p_figure, Figure)
    assert isinstance(h_figure, Figure)
    np.testing.assert_allclose(
        p_figure.axes[0].images[0].get_array(),
        1 - np.array([[1, 0.2, 0.01], [0.2, 1, 0.03], [0.01, 0.03, 1]]),
    )
    np.testing.assert_array_equal(
        h_figure.axes[0].images[0].get_array(),
        [[0, 0, 1], [0, 0, 1], [1, 1, 0]],
    )
    assert p_output.exists()
    assert h_output.exists()


@pytest.mark.parametrize("p_value", [0.01, 0.8, 0.99])
def test_p_value_colors_use_a_fixed_probability_scale(p_value):
    figure = significance.plot_p_value({"arg0-arg1": (0, p_value)})
    image = figure.axes[0].images[0]

    assert image.get_clim() == (0, 1)
    assert image.norm(1 - p_value) == pytest.approx(1 - p_value)


@pytest.mark.parametrize(
    ("plotter", "color"),
    [(significance.plot_p_value, 0.99), (significance.plot_h_index, 1)],
)
def test_missing_comparisons_remain_blank(plotter, color):
    figure = plotter({"arg0-arg2": (1, 0.01)})

    np.testing.assert_allclose(
        figure.axes[0].images[0].get_array().filled(np.nan),
        [[0, np.nan, color], [np.nan, 0, np.nan], [color, np.nan, 0]],
    )


@pytest.mark.parametrize(
    "plotter", [significance.plot_p_value, significance.plot_h_index]
)
@pytest.mark.parametrize(
    "key",
    [None, 1, "0-1", "arg0-arg-1", "arg0-arg0", "arg0-arg1-arg2", "argx-arg1"],
)
def test_invalid_pairwise_keys(plotter, key):
    with pytest.raises(ValueError, match="invalid pairwise result key"):
        plotter({key: (1, 0.01)})


@pytest.mark.parametrize(
    "plotter", [significance.plot_p_value, significance.plot_h_index]
)
def test_plots_accept_read_only_mappings_without_global_state(
    plotter, tmp_path, monkeypatch
):
    results = MappingProxyType(RESULTS)
    original = dict(results)
    figures = pyplot.get_fignums()
    color_map = colormaps["Blues"]
    monkeypatch.chdir(tmp_path)

    figure = plotter(results, color_map=color_map, labels=("A", "B", "C"))

    assert figure.axes[0].images[0].get_cmap() is color_map
    assert dict(results) == original
    assert pyplot.get_fignums() == figures
    assert not list(tmp_path.iterdir())


@pytest.mark.parametrize(
    ("plotter", "color"),
    [(significance.plot_p_value, 0.8), (significance.plot_h_index, 0)],
)
def test_multi_digit_indices_determine_labels_and_matrix_size(plotter, color):
    figure = plotter({"arg0-arg10": (0, 0.2)})
    axis = figure.axes[0]
    matrix = axis.images[0].get_array()

    assert matrix.shape == (11, 11)
    assert axis.get_xticklabels()[10].get_text() == "$arg_{10}$"
    assert axis.get_yticklabels()[10].get_text() == "$arg_{10}$"
    assert matrix[0, 10] == pytest.approx(color)
    assert matrix[10, 0] == pytest.approx(color)
    assert np.ma.is_masked(matrix[0, 1])
