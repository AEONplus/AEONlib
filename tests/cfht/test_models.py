import pytest

from aeonlib.cfht.conversions import (
    FixedTargetData,
    _sidereal_target_payload,
    target_data_from_aeon,
)
from aeonlib.cfht.models import (
    TargetData,
    TargetDataFixedTarget,
    TargetDataMagnitude,
)
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


def test_double_value_field_accepts_float():
    fixed_target = TargetDataFixedTarget(estimated_radial_velocity_kmps=234.0)

    assert fixed_target.estimated_radial_velocity_kmps == 234.0
    assert fixed_target.api_dump() == {
        "estimated_radial_velocity_kmps": {"value": 234.0}
    }


def test_aliased_double_value_field_accepts_float():
    magnitude = TargetDataMagnitude(v=10.0)

    assert magnitude.v == 10.0
    assert magnitude.api_dump() == {"v": {"value": 10.0}}


def test_double_value_field_accepts_wrapped_api_input():
    magnitude = TargetDataMagnitude.model_validate({"v": {"value": 10.0}})
    assert magnitude.v == 10.0

    null_magnitude = TargetDataMagnitude.model_validate({"v": {"value": None}})
    assert null_magnitude.v is None


def test_double_value_field_accepts_float_assignment():
    magnitude = TargetDataMagnitude()

    magnitude.a_b = 10.0

    assert magnitude.a_b == 10.0
    assert magnitude.api_dump() == {"a_b": {"value": 10.0}}
