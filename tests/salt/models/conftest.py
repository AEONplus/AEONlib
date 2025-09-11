import astropy.coordinates
import pytest

from aeonlib.salt.models import (
    Request,
    Block,
    MagnitudeRange,
    SaltSiderealTarget,
    Constraints,
)


@pytest.fixture()
def base_request(base_block):
    """A simple request to edit or build from."""
    return Request(proposal_code="2025-1-SCI-042", blocks=[base_block])


@pytest.fixture()
def base_block(base_target):
    """A simple block to build or edit from."""
    return Block(
        name="Test",
        priority=1,
        ranking="high",
        num_visits=1,
        constraints=None,
        target=base_target,
        acquisition=None,
        instrument=None,
    )


@pytest.fixture()
def base_target(base_magnitude_range):
    """A simple sidereal target to build or edit from."""
    return SaltSiderealTarget(
        name="Test Target",
        type="ICRS",
        ra=0,
        dec=0,
        target_type="Nova",
        magnitude_range=base_magnitude_range,
    )


@pytest.fixture()
def base_magnitude_range():
    """A simple magnitude range to build or edit from."""
    return MagnitudeRange(min_magnitude=17.1, max_magnitude=17.5, bandpass="V")


@pytest.fixture()
def base_constraints():
    return Constraints(
        transparency="thick cloud",
        max_lunar_phase_percentage=50,
        min_lunar_distance=astropy.coordinates.Angle("45d"),
        max_seeing=3,
    )
