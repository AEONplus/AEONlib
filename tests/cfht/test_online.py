import random

import pytest
from pydantic import ValidationError

from aeonlib.cfht.facility import CFHTFacility
from aeonlib.cfht.models import (
    DoubleValue,  # TODO: should be removed or coerced from float
    Instrument,
    MovingTargetEphemeris,  # TODO: replace with common non-sidereal model
    SkyCoordinate,
    TargetData,
    TargetDataFixedTarget,  # TODO: replace with common target model
    TargetDataMagnitude,
    TargetDataMovingTarget,  # TODO: replace with common non-sidereal target model
)

pytestmark = pytest.mark.online

required_mag_by_instrument: dict[Instrument, str] = {
    Instrument.spirou: "h",
    Instrument.espadons: "v",
    Instrument.megacam: "ab",
}


FACILITY = CFHTFacility()


def test_programs():
    programs = FACILITY.programs()
    assert programs[0].pi_info
    assert programs[0].pi_info.first_name == "AEON"


def example_fixed_target(program_token: str, instrument: Instrument) -> TargetData:
    return TargetData(
        token=f"{program_token}-{random.randint(1000000000, 9999999999)}",
        name="my new aeonlib test target",
        fixed_target=TargetDataFixedTarget(  # TODO: use Aeonlib common Target
            coordinate=SkyCoordinate(
                ra=random.uniform(0, 359.9999),
                dec=random.uniform(-90, 90),
            ),
            proper_motion=None,
            estimated_radial_velocity_kmps=DoubleValue(
                value=234.0
            )  # TODO: remove the need for DoubleValue
            if instrument == Instrument.spirou
            else None,
        ),
        magnitude=None,
        temperature_effective=1234.5,
        standard_star=False,
        pointing_offset_token=f"00AZ00-PO+{instrument.value}+1",
    )


def example_moving_target(program_token: str, instrument: Instrument) -> TargetData:
    return TargetData(
        token=f"{program_token}-{random.randint(1000000000, 9999999999)}",
        name="my new aeonlib moving target",
        moving_target=TargetDataMovingTarget(
            ephemeris_point=[
                MovingTargetEphemeris(
                    mjd=61041.0 + i,
                    coordinate=SkyCoordinate(
                        ra=random.uniform(0, 359.9999),
                        dec=random.uniform(-90, 90),
                    ),
                )
                for i in range(0, 5)
            ]
        ),
        magnitude=None,
        temperature_effective=1234.5,
        standard_star=False,
        pointing_offset_token=f"00AZ00-PO+{instrument.value}+1",
    )


def target_api_examples(program_token: str, instrument: Instrument):
    """
    Complete API examples for Kealahou targets
    """
    targets = FACILITY.targets(program_token)
    for target in targets:
        assert target.name is not None
        # assert "Test" in target.name  # TODO: find a better invariant

    new_target = example_fixed_target(program_token, instrument)

    # This is the part in the example.py where the target is assigned an
    # incorrect format for RA and sent to the API. We can't get that far in Aeonlib
    # because Pydantic will raise a Validation Error before it can be sumitted.

    assert new_target.fixed_target is not None
    assert new_target.fixed_target.coordinate is not None
    assert new_target.fixed_target.coordinate.ra is not None
    old_ra = new_target.fixed_target.coordinate.ra
    with pytest.raises(ValidationError):
        new_target.fixed_target.coordinate.ra = "invalid"  # type: ignore
    assert new_target.fixed_target.coordinate.ra == old_ra

    # Successfully create new target with instrument-specific checks
    new_target.fixed_target.coordinate.ra = 20.7
    mag = TargetDataMagnitude()
    setattr(mag, required_mag_by_instrument[instrument], DoubleValue(value=10.0))
    print(mag)
    new_target.magnitude = mag
    old_version = new_target.version if new_target.version is not None else 0
    target = FACILITY.create_or_update_target(program_token, new_target, instrument)
    assert target.version == old_version + 1
    old_version += 1

    # Update target
    update_target = target
    update_target.standard_star = True
    target = FACILITY.create_or_update_target(program_token, update_target, instrument)
    assert target.standard_star is True
    assert target.version == old_version + 1


def test_example():
    programs = FACILITY.programs()
    for program in programs:
        program_data = program.program_data
        assert program_data is not None
        program_token = program_data.token
        assert program_token is not None
        time_allocation = program_data.time_allocation
        assert time_allocation is not None
        instrument = time_allocation[0].instrument
        assert instrument is not None
        target_api_examples(program_token, instrument)
