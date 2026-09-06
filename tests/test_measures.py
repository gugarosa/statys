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


@pytest.mark.parametrize(
    ("measure", "expected"),
    [
        (measures.max, [5, 7]),
        (measures.mean, [3, 5]),
        (measures.median, [3, 5]),
        (measures.min, [1, 3]),
        (measures.std, [2, 2]),
        (measures.var, [4, 4]),
    ],
)
def test_axis_reductions_keep_array_results(measure, expected):
    sample = np.array([[1, 3], [5, 7]])
    original = sample.copy()

    output = measure(sample, sample + 1, axis=0)

    assert list(output) == ["arg0", "arg1"]
    np.testing.assert_array_equal(output["arg0"], expected)
    np.testing.assert_array_equal(sample, original)


def test_mean_retains_dtype_and_output_buffer_options():
    sample = np.array([[1, 3], [5, 7]], dtype=np.float32)
    output = np.empty(2, dtype=np.float64)

    result = measures.mean(sample, axis=0, dtype=np.float64, out=output)

    assert result["arg0"] is output
    assert output.dtype == np.float64
    np.testing.assert_array_equal(output, [3, 5])


@pytest.mark.parametrize("measure", [measures.std, measures.var])
def test_sample_variability_option(measure):
    assert measure([1, 2, 3], ddof=1)["arg0"] == pytest.approx(1)


def test_rank_axis_and_tie_method():
    result = measures.rank([[3, 1, 1], [2, 2, 1]], axis=1, method="dense")

    np.testing.assert_array_equal(result["arg0"], [[2, 1, 1], [2, 2, 1]])


def test_measures_do_not_silently_filter_nan_values():
    assert np.isnan(measures.mean([1, np.nan, 3])["arg0"])
    result = measures.skewness([1, np.nan, 2, 3], nan_policy="omit")
    assert result["arg0"] == pytest.approx(0)
