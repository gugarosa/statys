from statys.utils import constants


def test_constants():
    assert len(constants.CRITICAL_VALUES['nemenyi']) == 100
