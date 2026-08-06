import random
import uuid

import pytest
from pydantic import ValidationError

from aeonlib.cfht.facility import (
    CFHTFacility,
    EntityNotFoundError,
    VersionMismatchError,
)
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


@pytest.fixture(scope="module")
def facility() -> CFHTFacility:
    return CFHTFacility()


def test_programs(facility: CFHTFacility):
    programs = facility.programs()
    assert programs[0].pi_info
    assert programs[0].pi_info.first_name == "AEON"


def example_fixed_target(
    program_token: str, instrument: Instrument, test_run_id: str
) -> TargetData:
    return TargetData(
        token=f"{program_token}-{random.randint(1000000000, 9999999999)}",
        name=f"my new aeonlib test target {test_run_id}",
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


def example_moving_target(
    program_token: str, instrument: Instrument, test_run_id: str
) -> TargetData:
    return TargetData(
        token=f"{program_token}-{random.randint(1000000000, 9999999999)}",
        name=f"my new aeonlib moving target {test_run_id}",
        moving_target=TargetDataMovingTarget(
            ephemeris_point=[
                MovingTargetEphemeris(
                    mjd=61041.0 + i,
                    coordinate=SkyCoordinate(
                        ra=random.uniform(0, 359.9999),
                        dec=random.uniform(-90, 90),
                    ),
                )
                for i in range(5)
            ]
        ),
        magnitude=TargetDataMagnitude(
            **{required_mag_by_instrument[instrument]: DoubleValue(value=10.0)}
        ),
        temperature_effective=1234.5,
        standard_star=False,
        pointing_offset_token=f"00AZ00-PO+{instrument.value}+1",
    )


def target_api_examples(
    facility: CFHTFacility, instrument: Instrument, test_run_id: str
):
    """
    Complete API examples for Kealahou targets
    """
    program_token = facility.program_token
    assert program_token is not None

    targets = facility.targets()
    for target in targets:
        assert target.name is not None
        # assert "Test" in target.name  # TODO: find a better invariant

    new_target = example_fixed_target(program_token, instrument, test_run_id)

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
    new_target.magnitude = mag
    old_version = new_target.version if new_target.version is not None else 0
    target = facility.create_or_update_target(new_target, instrument)
    assert target.version == old_version + 1
    old_version += 1

    # Update target
    update_target = target
    update_target.standard_star = True
    target = facility.create_or_update_target(update_target, instrument)
    assert target.standard_star is True
    assert target.version == old_version + 1

    # Attempt to update target with invalid version
    # TODO should aeonlib handle versioning client side?
    with pytest.raises(VersionMismatchError):
        update_target.temperature_effective = 2345.6
        facility.create_or_update_target(update_target, instrument)

    # Fetch single target
    token = target.token
    assert token, "target token should not be None"
    target = facility.get_target(token)
    assert token == target.token

    # Delete the new (unobserved) target
    assert target.token
    facility.delete_target(target.token)
    with pytest.raises(EntityNotFoundError):
        facility.get_target(target.token)

    # create moving target
    new_moving_target = example_moving_target(program_token, instrument, test_run_id)
    moving_target = facility.create_or_update_target(new_moving_target, instrument)

    # Delete moving target
    assert moving_target.token
    facility.delete_target(moving_target.token)
    with pytest.raises(EntityNotFoundError):
        facility.get_target(moving_target.token)


def test_example(facility: CFHTFacility):
    test_run_id = f"{uuid.uuid4()}"[:8]
    programs = facility.programs()
    for program in programs:
        facility.select_program(program)
        program_data = program.program_data
        assert program_data is not None
        time_allocation = program_data.time_allocation
        assert time_allocation is not None
        instrument = time_allocation[0].instrument
        assert instrument is not None
        target_api_examples(facility, instrument, test_run_id)
