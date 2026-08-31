from matplotlib.figure import Figure

from statys import plot_critical_difference


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
