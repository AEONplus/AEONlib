from contextlib import nullcontext

import astropy.coordinates
import astropy.units as u
import pytest
from pydantic import ValidationError

from aeonlib.salt.models import MagnitudeRange, SaltSiderealTarget


class TestSaltSiderealTarget:
    def test_salt_sidereal_target(self, base_target):
        """Test that a simple target can be built."""
        assert True

    @pytest.mark.parametrize("target_type", ["ALTAZ", "HOUR_ANGLE"])
    def test_type(self, target_type: str, base_target):
        """Test that the target type must be ICRS."""
        target = base_target
        with pytest.raises(ValueError, match="SALT"):
            target.type = target_type

    def test_hour_angle_must_not_exist(self, base_target):
        """Test that no hour angle must be defined."""
        target = base_target
        with pytest.raises(ValueError, match="hour angle"):
            target.hour_angle = 45 * u.deg

    def test_altitude_must_not_exist(self, base_target):
        """Test that no altitude must be defined."""
        target = base_target
        with pytest.raises(ValueError, match="altitude"):
            target.altitude = 45 * u.deg

    def test_azimuth_must_not_exist(self, base_target):
        """Test that no azimuth must be defined."""
        target = base_target
        with pytest.raises(ValueError, match="azimuth"):
            target.azimuth = 45 * u.deg

    @pytest.mark.parametrize(
        "dec, expectation",
        [
            (astropy.coordinates.Angle("-76.001d"), pytest.raises(ValueError)),
            (astropy.coordinates.Angle("-76d"), nullcontext()),
            (astropy.coordinates.Angle("11d"), nullcontext()),
            (astropy.coordinates.Angle("11.0001d"), pytest.raises(ValueError)),
        ],
    )
    def test_dec_range(self, dec, expectation, base_target):
        """Test that the declination must be in SALT's visibility range."""
        target = base_target.model_dump()
        target["dec"] = dec
        with expectation:
            SaltSiderealTarget(**target)  # type: ignore


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
            MagnitudeRange(**magnitude_range)  # type: ignore

        assert True
