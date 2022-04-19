from statys.core import Distribution
from statys.tests import friedman


def test_friedman():
    x = [[0, 0.1, 0.2, 0.3, 0.4, 0.5], [0, 0.1, 0.2, 0.3, 0.4, 0.5]]
    d = Distribution(x)

    output = friedman.friedman(d)

    assert output["arg0"] == ((10.76923076923077, 11), (0.0, (11, 0)))


def test_friedman_with_posthoc():
    x = [[0, 0.1, 0.2, 0.3, 0.4, 0.5], [0, 0.1, 0.2, 0.3, 0.4, 0.5]]
    d = Distribution(x)

    output = friedman.friedman_with_posthoc(d, axis=1)

    assert len(output["arg0"][0]) == 6
    assert output["arg0"][1] == 5.331310596344878
