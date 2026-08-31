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

    assert set(output) == {"arg0-arg1", "arg0-arg2", "arg1-arg2"}
    assert all(reject in (0, 1) and 0 <= p_value <= 1 for reject, p_value in output.values())


def test_pairwise_requires_two_samples():
    with pytest.raises(ValueError):
        pairwise.u_test(SAMPLES[0])
