from statys.core import Distribution
from statys.tests import mann_whitney


def test_u_test():
    x = [0, 0.1, 0.2, 0.3, 0.4, 0.5]
    y = [0.07, 0.14, 0.72, 0.32, 0.59, 0.43]
    d = Distribution(x, y)

    output = mann_whitney.u_test(d)

    assert output["arg0-arg1"] == (0, 0.18923879662233944) or output["arg0-arg1"] == (
        0,
        0.3939393939393939,
    )
