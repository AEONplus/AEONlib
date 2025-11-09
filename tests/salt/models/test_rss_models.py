import math
from contextlib import nullcontext

import pytest
from astropy import units as u
from pydantic import ValidationError

from aeonlib.salt.models import RssDitherPattern, RssPolarimetry, RssSpectroscopy


class TestRss:
    def test_rss(self, base_rss):
        """Test that RSS configurations can be built."""
        assert True


class TestRssImaging:
    def test_rss_imaging(self, base_rss_imaging):
        """Test that RSS imaging configurations can be built."""
        assert True


class TestRssSpectroscopy:
    def test_rss_spectroscopy(self, base_rss_spectroscopy):
        """Test that RSS spectroscopy setups can be built."""
        assert True

    @pytest.mark.parametrize(
        "angle, expectation",
        [
            (-40, pytest.raises(ValueError)),
            (0, nullcontext()),
            (0.01, pytest.raises(ValueError)),
            (0.125, pytest.raises(ValueError)),
            (64.73, pytest.raises(ValueError)),
            (64.75, nullcontext()),
            (64.75 * u.deg, nullcontext()),
            ((64.75 * u.deg).to(u.rad), nullcontext()),
            (64.76 * u.deg, pytest.raises(ValueError)),
            (100, nullcontext()),
            (100.75, pytest.raises(ValueError)),
            (400, pytest.raises(ValueError)),
        ],
    )
    def test_articulation_angle_must_have_allowed_value(
        self, angle, expectation, base_rss_spectroscopy
    ):
        spectroscopy = base_rss_spectroscopy.model_dump()
        spectroscopy["articulation_angle"] = angle
        with expectation:
            RssSpectroscopy(**spectroscopy)


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
        # Test that wave plate pattern angles must be a multiple of 11.25 deg between
        # 0 deg (inclusive) and 360 deg (exclusive).
        with expectation:
            RssPolarimetry(wave_plate_pattern=[(angle, 45 * u.deg)])
            RssPolarimetry(wave_plate_pattern=[(45 * u.deg, angle)])


class TestRssLongslitSpectroscopy:
    def test_rss_longslit_spectroscopy(self, base_rss_longslit_spectroscopy):
        # Test that RSS longslit spectroscopy setups can be built.
        assert True


class TestRssMultiObjectSpectroscopy:
    def test_rss_multi_object_spectroscopy(self, base_rss_multi_object_spectroscopy):
        # Test that RSS multiobject spectroscopy setups can be built.
        assert True


class TestRssSlitMaskIFUSpectroscopy:
    def test_slit_mask_ifu_spectroscopy(self, base_rss_slit_mask_ifu_spectroscopy):
        # Test that RSS slit mask IFU spectroscopy setups can be built.
        assert True


class TestRssDetector:
    def test_rss_detector(self, base_rss_detector):
        # Test that RSS detector setups can be built.
        assert True


class TestRssDitherPattern:
    def test_rss_dither_pattern(self, base_rss_dither_pattern):
        """Test that RSS dither pattern can be built."""
        assert True

    def test_default_number_of_steps(self, base_rss_dither_pattern):
        dither_pattern = base_rss_dither_pattern.model_dump()
        dither_pattern["num_rows"] = 4
        dither_pattern["num_columns"] = 3
        if "num_steps" in dither_pattern:
            del dither_pattern["num_steps"]
        assert RssDitherPattern(**dither_pattern).num_steps == 12  # type: ignore

    @pytest.mark.parametrize(
        "num_rows, num_columns, num_steps, expectation",
        [
            (1, 1, 1, nullcontext()),
            (1, 1, 5, nullcontext()),
            (1, 2, 2, nullcontext()),
            (2, 1, 6, nullcontext()),
            (3, 5, 15, nullcontext()),
            (5, 3, 45, nullcontext()),
            (5, 2, 9, pytest.raises(ValidationError)),
            (3, 7, 43, pytest.raises(ValidationError)),
        ],
    )
    def test_only_complete_patterns_allowed(
        self,
        num_rows,
        num_columns,
        num_steps,
        expectation,
        base_rss_dither_pattern,
    ):
        dither_pattern = base_rss_dither_pattern.model_dump()
        dither_pattern["num_rows"] = num_rows
        dither_pattern["num_columns"] = num_columns
        dither_pattern["num_steps"] = num_steps
        with expectation:
            RssDitherPattern(**dither_pattern)  # type: ignore
