import random
import uuid
from collections.abc import Iterator

import pytest

from aeonlib.cfht.conversions import target_data_from_aeon
from aeonlib.cfht.facility import (
    CFHTFacility,
    EntityNotFoundError,
    ServerError,
    VersionMismatchError,
)
from aeonlib.cfht.models import (
    ExposureData,
    Instrument,
    MovingTargetEphemeris,  # TODO: replace with common non-sidereal model
    ObservingBlockObservingComponent,
    ObservingGroupData,
    ObservingGroupDataObservingBlock,
    ObservingTemplateData,
    OgPriority,
    ProgramInfo,
    SingleObservingGroup,
    SkyCoordinate,
    TargetData,
    TargetDataMagnitude,
    TargetDataMovingTarget,  # TODO: replace with common non-sidereal target model
    TargetType,
)
from aeonlib.models import SiderealTarget

pytestmark = pytest.mark.online

example_mag_by_instrument: dict[Instrument, str] = {
    Instrument.spirou: "h",
    Instrument.espadons: "v",
    Instrument.megacam: "ab",
}


@pytest.fixture(scope="module")
def facility() -> CFHTFacility:
    return CFHTFacility()


@pytest.fixture(scope="module")
def test_run_id() -> str:
    return uuid.uuid4().hex[:8]


@pytest.fixture(scope="module")
def program_facilities(facility: CFHTFacility) -> list[CFHTFacility]:
    facilities = [
        CFHTFacility(program_token=data.token)
        for program in facility.programs()
        if (data := program.program_data)
        if data.token
    ]
    assert facilities, "No programs with tokens were returned"
    return facilities


def program_instruments(
    facilities: list[CFHTFacility],
) -> Iterator[tuple[CFHTFacility, str, Instrument]]:
    for facility in facilities:
        program_token = facility.program_token
        assert program_token is not None
        instruments = facility.instruments()
        assert instruments, f"No instruments allocated to {program_token}"
        unsupported = instruments.difference(example_mag_by_instrument)
        assert not unsupported, (
            "Example required mag not defined "
            f"for: {', '.join(sorted(i.value for i in unsupported))}"
        )
        for instrument in instruments:
            yield facility, program_token, instrument


def example_fixed_target(
    program_token: str, instrument: Instrument, test_run_id: str
) -> TargetData:
    # Start with an Aeonlib common SiderealTarget
    sidereal_target = SiderealTarget(
        name=f"my new aeonlib test target {test_run_id}",
        type="ICRS",
        ra=random.uniform(0, 359.9999),
        dec=random.uniform(-90, 90),
    )
    # Get a CFHT TargetData
    target_data = target_data_from_aeon(sidereal_target)

    # Add CFHT specific fields
    target_data.token = f"{program_token}-{random.randint(1000000000, 9999999999)}"
    target_data.fixed_target.estimated_radial_velocity_kmps = (
        234.0 if instrument == Instrument.spirou else None
    )
    target_data.magnitude = TargetDataMagnitude(
        **{example_mag_by_instrument[instrument]: 10.0}
    )
    target_data.temperature_effective = 1234.5
    target_data.standard_star = False
    target_data.pointing_offset_token = f"00AZ00-PO+{instrument.value}+1"

    return target_data


def example_moving_target(
    program_token: str, instrument: Instrument, test_run_id: str
) -> TargetData:
    # For now constructing a moving target needs to be done manually as
    # generating the ephemeris points automatically is not yet supported
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
        magnitude=TargetDataMagnitude(**{example_mag_by_instrument[instrument]: 10.0}),
        temperature_effective=1234.5,
        standard_star=False,
        pointing_offset_token=f"00AZ00-PO+{instrument.value}+1",
    )


def test_programs(facility: CFHTFacility):
    programs = facility.programs()
    assert isinstance(programs, list)
    assert all(isinstance(program, ProgramInfo) for program in programs)


def test_get_targets(program_facilities: list[CFHTFacility]):
    for facility in program_facilities:
        targets = facility.targets()
        assert isinstance(targets, list)
        assert all(isinstance(target, TargetData) for target in targets)


@pytest.mark.side_effect
def test_create_fixed_targets(program_facilities: list[CFHTFacility], test_run_id: str):
    for facility, program_token, instrument in program_instruments(program_facilities):
        new_target = example_fixed_target(program_token, instrument, test_run_id)
        target = facility.create_or_update_target(new_target, instrument)
        try:
            assert target.version == 1
        finally:
            if target.token is not None:
                facility.delete_target(target.token)


@pytest.mark.side_effect
def test_create_moving_targets(
    program_facilities: list[CFHTFacility], test_run_id: str
):
    for facility, program_token, instrument in program_instruments(program_facilities):
        new_target = example_moving_target(program_token, instrument, test_run_id)
        target = facility.create_or_update_target(new_target, instrument)
        try:
            assert target.version == 1
        finally:
            if target.token is not None:
                facility.delete_target(target.token)


@pytest.mark.side_effect
def test_get_target(program_facilities: list[CFHTFacility], test_run_id: str):
    for facility, program_token, instrument in program_instruments(program_facilities):
        new_target = example_fixed_target(program_token, instrument, test_run_id)
        target = facility.create_or_update_target(new_target, instrument)
        try:
            assert target.token is not None
            fetched_target = facility.get_target(target.token)
            assert fetched_target.token == target.token
        finally:
            if target.token is not None:
                facility.delete_target(target.token)


@pytest.mark.side_effect
def test_delete_target(program_facilities: list[CFHTFacility], test_run_id: str):
    for facility, program_token, instrument in program_instruments(program_facilities):
        new_target = example_fixed_target(program_token, instrument, test_run_id)
        target = facility.create_or_update_target(new_target, instrument)
        assert target.token is not None
        facility.delete_target(target.token)
        with pytest.raises(EntityNotFoundError):
            facility.get_target(target.token)


@pytest.mark.side_effect
def test_update_fixed_targets(program_facilities: list[CFHTFacility], test_run_id: str):
    for facility, program_token, instrument in program_instruments(program_facilities):
        new_target = example_fixed_target(program_token, instrument, test_run_id)
        target = facility.create_or_update_target(new_target, instrument)
        try:
            assert target.version == 1
            updated_name = f"updates aeonlib target {test_run_id}"
            target.name = updated_name
            target = facility.create_or_update_target(target, instrument)
            assert target.name == updated_name
            assert target.version == 2
        finally:
            if target.token is not None:
                facility.delete_target(target.token)


@pytest.mark.side_effect
def test_target_bad_version(program_facilities: list[CFHTFacility], test_run_id: str):
    facility, program_token, instrument = next(program_instruments(program_facilities))
    new_target = example_fixed_target(program_token, instrument, test_run_id)
    target = facility.create_or_update_target(new_target, instrument)
    try:
        assert target.version == 1
        target.version = 0
        with pytest.raises(VersionMismatchError):
            facility.create_or_update_target(target, instrument)
    finally:
        if target.token is not None:
            facility.delete_target(target.token)


def test_get_observing_templates(program_facilities: list[CFHTFacility]):
    for facility in program_facilities:
        templates = facility.observing_templates()
        assert isinstance(templates, list)
        assert all(
            isinstance(template, ObservingTemplateData) for template in templates
        )


@pytest.mark.side_effect
def test_create_observing_group(
    program_facilities: list[CFHTFacility], test_run_id: str
):
    facility, program_token, instrument = next(program_instruments(program_facilities))
    templates = facility.observing_templates()
    assert templates, "No observing templates available"
    first_ot = templates[0]
    new_target = example_fixed_target(program_token, instrument, test_run_id)
    target = facility.create_or_update_target(new_target, instrument)
    new_observing_group = ObservingGroupData(
        token=f"{program_token}-{random.randint(1000000000, 9999999999)}",
        og_priority=OgPriority.medium,
        target_type=TargetType.object,
        single_observing_group=SingleObservingGroup(
            observing_block=ObservingGroupDataObservingBlock(
                observing_component=[
                    ObservingBlockObservingComponent(
                        target_token=target.token,
                        observing_template_token=first_ot.token,
                    )
                ]
            )
        ),
    )
    observing_group = facility.create_observing_group(new_observing_group)
    assert isinstance(observing_group, ObservingGroupData)
    try:
        assert observing_group.token
        assert observing_group.label

        # Attempt to delete the target that is used in an observing group
        with pytest.raises(ServerError):
            if target.token is not None:
                facility.delete_target(target.token)
    finally:
        facility.delete_observing_group(observing_group.token)
        if target.token is not None:
            facility.delete_target(target.token)


def test_get_exposures(program_facilities: list[CFHTFacility]):
    for facility in program_facilities:
        exposures = facility.exposures()
        assert isinstance(exposures, list)
        assert all(isinstance(exposure, ExposureData) for exposure in exposures)
