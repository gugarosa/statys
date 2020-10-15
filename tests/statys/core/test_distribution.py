from statys.core.distribution import Distribution


def test_distribution():
    d = Distribution([0.1, 0.2])

    assert d.arg0 == [0.1, 0.2]
