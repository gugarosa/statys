from statys.core import Distribution
from statys.plotters import significance
from statys.tests import wilcoxon


def test_plot_h_index():
    x = [0, 0.1, 0.2, 0.3, 0.4, 0.5]
    y = [0.07, 0.14, 0.72, 0.32, 0.59, 0.43]
    z = [2.17, 9.14, 999.72, 8.32, 7.19, 9.43]

    d = Distribution(x, y, z)

    signed_rank = wilcoxon.signed_rank(d)

    significance.plot_h_index(signed_rank)


def test_plot_p_value():
    x = [0, 0.1, 0.2, 0.3, 0.4, 0.5]
    y = [0.07, 0.14, 0.72, 0.32, 0.59, 0.43]
    z = [2.17, 9.14, 999.72, 8.32, 7.19, 9.43]

    d = Distribution(x, y, z)

    signed_rank = wilcoxon.signed_rank(d)

    significance.plot_p_value(signed_rank)
