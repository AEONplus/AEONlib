from contextlib import nullcontext

import astropy.coordinates
import pytest
from pydantic import ValidationError

from aeonlib.salt.models import MagnitudeRange, SaltSiderealTarget


class TestSaltSiderealTarget:
    def test_salt_sidereal_target(self, base_target):
        """Test that a simple target can be built."""
        assert True

    @pytest.mark.parametrize(
        "ra, expectation",
        [
            (astropy.coordinates.Angle("-76.001d"), pytest.raises(ValueError)),
            (astropy.coordinates.Angle("-76d"), nullcontext()),
            (astropy.coordinates.Angle("11d"), nullcontext()),
            (astropy.coordinates.Angle("11.0001d"), pytest.raises(ValueError)),
        ],
    )
    def test_ra_range(self, ra, expectation, base_target):
        """Test that the right ascension must be between -76 and 11 degrees."""
        target = base_target.model_dump()
        target["ra"] = ra
        with expectation:
            SaltSiderealTarget(**target)


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
