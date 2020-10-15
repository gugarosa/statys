from statys.core import Distribution
from statys.plotters import critical
from statys.tests import friedman


def test_plot_critical_difference():
    x = [0, 0.1, 0.2, 0.3, 0.4, 0.5]
    y = [0.07, 0.14, 0.72, 0.32, 0.59, 0.43]

    d = Distribution(x, y)

    friedman_nemenyi = friedman.friedman_with_posthoc(d)

    critical.plot_critical_difference(friedman_nemenyi)
