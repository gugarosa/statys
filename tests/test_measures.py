import numpy as np
import pytest

from statys import measures


SAMPLE = [0, 0.1, 0.2, 0.3, 0.4, 0.5]


@pytest.mark.parametrize(
    ("measure", "expected"),
    [
        (measures.kurtosis, -1.268571428571428),
        (measures.max, 0.5),
        (measures.mean, 0.25),
        (measures.median, 0.25),
        (measures.min, 0),
        (measures.skewness, 5.804286057433026e-17),
        (measures.std, 0.1707825127659933),
        (measures.var, 0.029166666666666664),
    ],
)
def test_scalar_measures(measure, expected):
    assert measure(SAMPLE)["arg0"] == pytest.approx(expected)


def test_rank_and_multiple_samples():
    output = measures.rank(SAMPLE, [2, 1])

    assert output["arg0"] == pytest.approx(np.arange(1, 7))
    assert output["arg1"] == pytest.approx([2, 1])


def test_measure_requires_a_sample():
    with pytest.raises(ValueError):
        measures.mean()
