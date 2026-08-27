from functools import singledispatch
from typing import Any, overload

from aeonlib.models import TARGET_TYPES, SiderealTarget

from .models import TargetData, TargetDataFixedTarget

# This is a bit over-engineered at the moment. I started writing
# it before I realized that non-sidereal targets were going to require
# a lot more work. Well, the infrastructure is here if we ever implement
# non-sidereal target conversions.


class FixedTargetData(TargetData):
    """CFHT target data guaranteed to contain sidereal target fields."""

    fixed_target: TargetDataFixedTarget


def _sidereal_target_payload(target: SiderealTarget) -> dict[str, Any]:
    return {
        "name": target.name,
        "fixed_target": {
            "coordinate": {
                "ra": target.ra.to_value("deg"),
                "dec": target.dec.to_value("deg"),
            },
            "proper_motion": {
                "ra_mas": target.proper_motion_ra,
                "dec_mas": target.proper_motion_dec,
            },
        },
    }


@singledispatch
def _target_data_from_aeon(target: object) -> TargetData:
    raise TypeError(f"Cannot convert {type(target).__name__} to CFHT TargetData")


@_target_data_from_aeon.register
def _convert_sidereal_target_data(target: SiderealTarget) -> FixedTargetData:
    return FixedTargetData.model_validate(_sidereal_target_payload(target))


# TODO: Register non-sidereal target conversions here.
# They will require a JPL Horizons client or API call because CFHT
# uses a series of astrometric coordinates instead of orbital elements.


@overload
def target_data_from_aeon(target: SiderealTarget) -> FixedTargetData: ...


@overload
def target_data_from_aeon(target: TARGET_TYPES) -> TargetData: ...


def target_data_from_aeon(target: TARGET_TYPES) -> TargetData:
    return _target_data_from_aeon(target)
