from statys.core import Distribution
from statys.tests import measure


def test_kurtosis():
    x = [0, 0.1, 0.2, 0.3, 0.4, 0.5]
    d = Distribution(x)

    output = measure.kurtosis(d)

    assert output["arg0"] == -1.268571428571428


def test_max():
    x = [0, 0.1, 0.2, 0.3, 0.4, 0.5]
    d = Distribution(x)

    output = measure.max(d)

    assert output["arg0"] == 0.5


def test_mean():
    x = [0, 0.1, 0.2, 0.3, 0.4, 0.5]
    d = Distribution(x)

    output = measure.mean(d)

    assert output["arg0"] == 0.25


def test_median():
    x = [0, 0.1, 0.2, 0.3, 0.4, 0.5]
    d = Distribution(x)

    output = measure.median(d)

    assert output["arg0"] == 0.25


def test_min():
    x = [0, 0.1, 0.2, 0.3, 0.4, 0.5]
    d = Distribution(x)

    output = measure.min(d)

    assert output["arg0"] == 0


def test_rank():
    x = [0, 0.1, 0.2, 0.3, 0.4, 0.5]
    d = Distribution(x)

    output = measure.rank(d)

    assert len(output["arg0"]) == 6


def test_skewness():
    x = [0, 0.1, 0.2, 0.3, 0.4, 0.5]
    d = Distribution(x)

    output = measure.skewness(d)

    assert output["arg0"] == 5.804286057433026e-17


def test_std():
    x = [0, 0.1, 0.2, 0.3, 0.4, 0.5]
    d = Distribution(x)

    output = measure.std(d)

    assert output["arg0"] == 0.1707825127659933


def test_var():
    x = [0, 0.1, 0.2, 0.3, 0.4, 0.5]
    d = Distribution(x)

    output = measure.var(d)

    assert output["arg0"] == 0.029166666666666664
