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
            ([(10 * u.deg, 20 * u.deg)], nullcontext()),
            ([(10 * u.deg, 20 * u.deg)] * 8, nullcontext()),
            ([(10 * u.deg, 20 * u.deg)] * 9, pytest.raises(ValueError)),
        ],
    )
    def test_pattern_must_have_between_1_and_8_steps(self, pattern, expectation):
        """Test that the wave pattern must have between 1 and 8 steps."""
        with expectation:
            RssPolarimetry(wave_plate_pattern=pattern)
