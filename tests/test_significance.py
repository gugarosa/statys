import numpy as np
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
        1 - np.array([[1, 0.2, 0.01], [0.2, 1, 0.03], [0.01, 0.03, 1]])
    )
    assert p_output.exists()
    assert h_output.exists()
