from contextlib import nullcontext

import astropy.units as u
import pytest
from pydantic import ValidationError

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


class TestRequest:
    def test_request(self, base_request):
        """Test that a simple request can be built."""
        assert True

    def test_no_blocks(self):
        """Test that at least one block must be supplied."""
        with pytest.raises(ValidationError) as exc_info:
            Request(proposal_code="2025-1-SCI-042", blocks=[])
        assert exc_info.value.errors()[0]["loc"] == ("blocks",)
        assert exc_info.value.errors()[0]["type"] == "too_short"


class TestBlock:
    def test_block(self, base_block):
        """Test that a simple block can be built."""
        assert True

    @pytest.mark.parametrize(
        "num_visits, max_num_visits, expectation",
        [
            (7, None, nullcontext()),
            (7, 8, nullcontext()),
            (7, 7, nullcontext()),
            (7, 6, pytest.raises(ValidationError, match="greater than")),
        ],
    )
    def test_max_visits_and_visits(
        self, num_visits, max_num_visits, expectation, base_block
    ):
        """
        Test that the maximum number of visits must not be less than the number of
        visits.
        """
        block = base_block.model_dump()
        block["num_visits"] = num_visits
        block["max_num_visits"] = max_num_visits

        with expectation:
            Block(**block)

        assert True


class TestSaltSiderealTarget:
    def test_salt_sidereal_target(self, base_target):
        """Test that a simple target can be built."""
        assert True


class TestMagnitudeRange:
    def test_magnitude_range(self, base_magnitude_range):
        """Test that a simple magnitude range can be built."""
        assert True

    @pytest.mark.parametrize(
        "min_magnitude, max_magnitude, expectation",
        [
            (17.1, 17.4, nullcontext()),
            (17.1, 17.1, nullcontext()),
            (17.1, 17.09, pytest.raises(ValidationError, match="greater than")),
        ],
    )
    def test_min_and_max_magnitude(
        self, min_magnitude, max_magnitude, expectation, base_magnitude_range
    ):
        """
        Test that the maximum magnitude must not be less than the minimum magnitude.
        """
        magnitude_range = base_magnitude_range.model_dump()
        magnitude_range["min_magnitude"] = min_magnitude
        magnitude_range["max_magnitude"] = max_magnitude

        with expectation:
            MagnitudeRange(**magnitude_range)

        assert True


class TestConstraints:
    def test_constraints(self, base_constraints):
        """Test that constraints can be built."""
        assert True
