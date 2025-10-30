import math
from contextlib import nullcontext

import pytest
from astropy import units as u

from aeonlib.salt.models import RssPolarimetry


class TestRss:
    def test_rss(self, base_rss):
        """Test that RSS configurations can be built."""
        assert True


class TestRssImaging:
    def test_rss_imaging(self, base_rss_imaging):
        """Test that RSS imaging configurations can be built."""
        assert True


class TestRssPolarimetry:
    def test_rss_polarimetry(self, base_rss_polarimetry):
        """Test that RSS polarimetry setups can be built."""
        assert True

    @pytest.mark.parametrize(
        "pattern, expectation",
        [
            ("linear", nullcontext()),
            ("all-Stokes", nullcontext()),
            ([], pytest.raises(ValueError)),
            ([(45 * u.deg, 90 * u.deg)], nullcontext()),
            ([(45 * u.deg, 90 * u.deg)] * 8, nullcontext()),
            ([(45 * u.deg, 90 * u.deg)] * 9, pytest.raises(ValueError)),
        ],
    )
    def test_pattern_must_have_between_1_and_8_steps(self, pattern, expectation):
        """Test that the wave pattern must have between 1 and 8 steps."""
        with expectation:
            RssPolarimetry(wave_plate_pattern=pattern)

    @pytest.mark.parametrize(
        "angle, expectation",
        [
            (0, nullcontext()),
            (11.25, nullcontext()),
            ((math.pi / 4) * u.rad, nullcontext()),  # 45 degrees in radians
            (303.75, nullcontext()),
            (-0.01, pytest.raises(ValueError)),
            (-11.25, pytest.raises(ValueError)),
            (11.24, pytest.raises(ValueError)),
            (303.76, pytest.raises(ValueError)),
            (360, pytest.raises(ValueError)),
            (405, pytest.raises(ValueError)),
        ],
    )
    def test_angles_must_have_allowed_value(self, angle, expectation):
        # Test that wave plater pattern angles must be a multiple of 11.25 deg between
        # 0 deg (inclusive) and 360 deg (exclusive).
        with expectation:
            RssPolarimetry(wave_plate_pattern=[(angle, 45 * u.deg)])
            RssPolarimetry(wave_plate_pattern=[(45 * u.deg, angle)])
