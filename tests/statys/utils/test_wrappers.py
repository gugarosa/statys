from statys.core import Distribution
from statys.utils import wrappers


def test_calculate_hypothesis():
    p = 0.1
    alpha = 0.05

    h = wrappers.calculate_hypothesis(p, alpha)

    assert h == 0


def test_measure_pipeline():
    def f(x):
        return True

    d = Distribution([0.1, 0.2])

    output = wrappers.measure_pipeline(f, d)

    assert output['arg0'] == True


def test_statistical_pipeline():
    def f(x, y):
        return [0, 0]

    d = Distribution([0.1, 0.2], [0.3, 0.4])
    alpha = 0.05

    output = wrappers.statistical_pipeline(f, d, alpha)

    assert output['arg0-arg1'] == (1, 0)
