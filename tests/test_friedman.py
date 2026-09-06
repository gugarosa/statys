# Copyright (c) 2020-2026 Gustavo de Rosa.
# Licensed under the Apache License, Version 2.0.

from math import inf

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


@pytest.mark.parametrize("row", [[1, 2, 3], [1, 2, 3, 3], [1, 2, 3, 4, 4]])
def test_friedman_perfect_agreement(row):
    data = np.asarray([row, np.asarray(row) + 10])

    statistic, iman = friedman(data)

    degrees = len(row) - 1
    assert statistic == (pytest.approx(2 * degrees), degrees)
    assert iman == (inf, (degrees, degrees))


def test_friedman_near_perfect_agreement():
    count = 10000
    data = np.tile(np.arange(count), (2, 1))
    data[1, :2] = [1, 0]

    _, (iman, _) = friedman(data)

    # One swapped pair has residual rank sum of squares 1, not zero
    expected = count * (count**2 - 1) / 6 - 1
    assert iman == pytest.approx(expected, rel=1e-12)


def test_friedman_with_ties():
    data = np.array([[1, 2, 2], [3, 3, 1], [2, 1, 3]])
    original = data.copy()

    for values in (data, data[::-1, ::-1]):
        statistic, iman = friedman(values)
        assert statistic == (pytest.approx(1 / 5), 2)
        assert iman == (pytest.approx(2 / 29), (2, 4))
    np.testing.assert_array_equal(data, original)


def test_friedman_undefined_statistics():
    with pytest.warns(RuntimeWarning, match="invalid value"):
        statistic, iman = friedman([[1, 1, 1], [2, 2, 2]])

    assert np.isnan(statistic[0])
    assert np.isnan(iman[0])

    statistic, iman = friedman([[1, 2, 3], [2, np.nan, 4]])
    assert np.isnan(statistic[0])
    assert np.isnan(iman[0])


def test_nemenyi():
    ranks, critical_difference = nemenyi(DATA)

    assert ranks == pytest.approx([1.5, 2.25, 2.25])
    assert critical_difference == pytest.approx(1.65724657769906)


def test_invalid_data():
    with pytest.raises(ValueError, match=r"^`data` must contain at least two blocks and two treatments\.$"):
        friedman([1, 2, 3])

    with pytest.raises(ValueError, match=r"^`data` must contain at least three treatments for Friedman's test\.$"):
        friedman(DATA[:, :2])

    with pytest.raises(ValueError, match=r"^`alpha` must be between 0 and 1, but got 1\.$"):
        nemenyi(DATA, alpha=1)
