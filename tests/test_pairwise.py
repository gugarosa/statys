import numpy as np
import pytest

from statys import pairwise

SAMPLES = (
    [0, 0.1, 0.2, 0.3, 0.4, 0.5],
    [0.07, 0.14, 0.72, 0.32, 0.59, 0.43],
    [0.9, 0.8, 0.7, 0.6, 0.5, 0.4],
)


@pytest.mark.parametrize(
    "test",
    [pairwise.u_test, pairwise.signed_rank, pairwise.rank_sum],
)
def test_pairwise_comparisons(test):
    output = test(*SAMPLES)

    assert list(output) == ["arg0-arg1", "arg0-arg2", "arg1-arg2"]
    assert all(
        reject in (0, 1) and 0 <= p_value <= 1 for reject, p_value in output.values()
    )


def test_pairwise_requires_two_samples():
    with pytest.raises(ValueError):
        pairwise.u_test(SAMPLES[0])


@pytest.mark.parametrize(
    "test",
    [pairwise.u_test, pairwise.signed_rank, pairwise.rank_sum],
)
def test_pairwise_undefined_p_value(test):
    with pytest.raises(ValueError, match="arg0-arg1.*non-finite p-value"):
        test([1, np.nan, 3], [4, 5, 6])


@pytest.mark.parametrize(
    "test",
    [pairwise.u_test, pairwise.signed_rank, pairwise.rank_sum],
)
def test_pairwise_explicit_nan_policy(test):
    actual = test([1, np.nan, 3], [4, np.nan, 6], nan_policy="omit")

    assert actual == test([1, 3], [4, 6])


def test_pairwise_error_identifies_the_failed_pair():
    with pytest.raises(ValueError, match="arg0-arg2.*non-finite p-value"):
        pairwise.u_test([1, 2, 3], [4, 5, 6], [7, np.nan, 9])


def test_u_test_exact_p_value_and_rejection_threshold():
    results = pairwise.u_test([1, 2], [3, 4], method="exact", alpha=1 / 3)

    # Two of the six equally likely allocations are as extreme as this split.
    reject, p_value = results["arg0-arg1"]
    assert p_value == pytest.approx(1 / 3)
    assert reject == 0


def test_signed_rank_exact_p_value():
    results = pairwise.signed_rank([1, 2, 3, 4], [5, 7, 9, 11], method="exact")

    assert results["arg0-arg1"] == (0, 2 / 16)


@pytest.mark.parametrize(("alternative", "expected"), [("less", 1 / 6), ("greater", 1)])
def test_one_sided_alternatives_follow_input_order(alternative, expected):
    result = pairwise.u_test([1, 2], [3, 4], method="exact", alternative=alternative)

    assert result["arg0-arg1"][1] == pytest.approx(expected)


def test_scipy_keyword_errors_propagate():
    with pytest.raises(TypeError, match="unexpected keyword argument"):
        pairwise.u_test([1, 2], [3, 4], unexpected_option=True)
