from contextlib import nullcontext

from astropy import units as u
import pytest

from aeonlib.salt.models import Nirwals, NirwalsDitherPatternStep


class TestNirwals:
    def test_nirwals(self, base_nirwals):
        # Test that NIRWALS configurations can be built.
        assert True

    @pytest.mark.parametrize(
        "angle, expectation",
        [
            (-1e-7 * u.deg, pytest.raises(ValueError)),
            (0, nullcontext()),
            (0.001, pytest.raises(ValueError)),
            (12.499 * u.deg, pytest.raises(ValueError)),
            (12.5, nullcontext()),
            (12.501 * u.deg, pytest.raises(ValueError)),
            ((74 * u.deg).to(u.rad), nullcontext()),
            (100 * u.deg, nullcontext()),
            ((100 + 1e-7) * u.deg, pytest.raises(ValueError)),
            (100.5 * u.deg, pytest.raises(ValueError)),
            (370 * u.deg, pytest.raises(ValueError)),
        ],
    )
    def test_articulation_angle_must_have_correct_value(
        self, angle, expectation, base_nirwals
    ):
        # Test that the articulation anfle must be a multiple of 0.5 degrees between 0
        # and 100 degrees.
        data = base_nirwals.model_dump()
        data["articulation_angle"] = angle
        with expectation:
            Nirwals(**data)


class TestNirwalsDitherPatternStep:
    def test_nirwals_dither_pattern_step(self):
        # Test that NIRWALS dither pattern step setups can be built.
        assert True

    @pytest.mark.parametrize(
        "exposure_time, num_groups",
        [(0.001 * u.s, 1), (37 * u.s, 50), (70_000 * u.ms, 96)],
    )
    def test_number_of_groups(
        self, exposure_time, num_groups, base_nirwals_dither_pattern_step
    ):
        # Test that the number of groups is calculated correctly.
        data = base_nirwals_dither_pattern_step.model_dump()
        data["exposure_time"] = exposure_time
        step = NirwalsDitherPatternStep(**data)

        assert step.num_groups == num_groups
