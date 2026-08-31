import numpy as np
import pytest

from statys import friedman, nemenyi


DATA = np.array(
    [
        [1, 2, 3],
        [2, 1, 3],
        [1, 3, 2],
        [2, 3, 1],
    ]
)


def test_friedman():
    statistic, iman = friedman(DATA)

    assert statistic == (pytest.approx(1.5), 2)
    assert iman == (pytest.approx(0.6923076923076923), (2, 6))


def test_nemenyi():
    ranks, critical_difference = nemenyi(DATA)

    assert ranks == pytest.approx([1.5, 2.25, 2.25])
    assert critical_difference == pytest.approx(1.65724657769906)


def test_invalid_data():
    with pytest.raises(ValueError):
        friedman([1, 2, 3])

    with pytest.raises(ValueError):
        nemenyi(DATA, alpha=1)
