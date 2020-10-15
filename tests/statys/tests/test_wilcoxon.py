from statys.core import Distribution
from statys.tests import wilcoxon


def test_signed_rank():
    x = [0, 0.1, 0.2, 0.3, 0.4, 0.5]
    y = [0.07, 0.14, 0.72, 0.32, 0.59, 0.43]
    d = Distribution(x, y)

    output = wilcoxon.signed_rank(d)

    assert output['arg0-arg1'] == (0, 0.15625)


def test_rank_sum():
    x = [0, 0.1, 0.2, 0.3, 0.4, 0.5]
    y = [0.07, 0.14, 0.72, 0.32, 0.59, 0.43]
    d = Distribution(x, y)

    output = wilcoxon.rank_sum(d)

    assert output['arg0-arg1'] == (0, 0.3366683676100388)
