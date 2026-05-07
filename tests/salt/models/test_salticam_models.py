from contextlib import nullcontext

import pytest
from pydantic import ValidationError

from aeonlib.salt.models import Salticam, SalticamDitherPattern


class TestSalticam:
    def test_salticam(self, base_salticam):
        """Test that Salticam configurations can be built."""
        assert True

    def test_at_least_one_filter(self, base_salticam):
        """Test that the filter sequence must have at least one step."""
        salticam = base_salticam.model_dump()
        salticam["filter_sequence"] = []
        with pytest.raises(ValidationError, match="at least 1"):
            Salticam(**salticam)  # type: ignore


class TestSalticamFilterSequenceStep:
    def test_salticam_filter_sequence_step(self, base_salticam_filter_sequence_step):
        """Test that filter sequence steps can be built."""
        assert True


class TestSalticamDetector:
    def test_salticam_detector(self, base_salticam_detector):
        """Test that Salticam detector setups can be built."""
        assert True


class TestSalticamDitherPattern:
    def test_salticam_dither_pattern(self, base_salticam_dither_pattern):
        """Test that Salticam dither pattern can be built."""
        assert True

    def test_default_number_of_steps(self, base_salticam_dither_pattern):
        dither_pattern = base_salticam_dither_pattern.model_dump()
        dither_pattern["num_rows"] = 4
        dither_pattern["num_columns"] = 3
        if "num_steps" in dither_pattern:
            del dither_pattern["num_steps"]
        assert SalticamDitherPattern(**dither_pattern).num_steps == 12  # type: ignore

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
        base_salticam_dither_pattern,
    ):
        dither_pattern = base_salticam_dither_pattern.model_dump()
        dither_pattern["num_rows"] = num_rows
        dither_pattern["num_columns"] = num_columns
        dither_pattern["num_steps"] = num_steps
        with expectation:
            SalticamDitherPattern(**dither_pattern)  # type: ignore
