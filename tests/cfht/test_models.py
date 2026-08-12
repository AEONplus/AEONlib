import pytest

from aeonlib.cfht.conversions import (
    FixedTargetData,
    _sidereal_target_payload,
    target_data_from_aeon,
)
from aeonlib.cfht.models import TargetData
from aeonlib.models import SiderealTarget


@pytest.fixture(scope="module")
def sidereal_target():
    return SiderealTarget(
        name="test",
        type="ICRS",
        ra=12.3,
        dec=45.6,
        proper_motion_ra=1.0,
        proper_motion_dec=0.1,
    )


def test_sidereal_target_payload(sidereal_target):
    payload = _sidereal_target_payload(sidereal_target)
    assert payload["name"] == "test"
    assert payload["fixed_target"]["coordinate"]["ra"] == 12.3
    assert payload["fixed_target"]["coordinate"]["dec"] == 45.6
    assert payload["fixed_target"]["proper_motion"]["ra_mas"] == 1.0
    assert payload["fixed_target"]["proper_motion"]["dec_mas"] == 0.1


def test_sidereal_target_to_target_data(sidereal_target):
    result = target_data_from_aeon(sidereal_target)
    assert isinstance(result, FixedTargetData)
    assert isinstance(result, TargetData)
    assert result.name == "test"
    assert result.fixed_target
    assert result.moving_target is None
    assert result.fixed_target.coordinate
    assert result.fixed_target.coordinate.ra == 12.3
    assert result.fixed_target.coordinate.dec == 45.6
    assert result.fixed_target.proper_motion
    assert result.fixed_target.proper_motion.ra_mas == 1.0
    assert result.fixed_target.proper_motion.dec_mas == 0.1
