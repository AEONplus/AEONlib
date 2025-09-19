from contextlib import nullcontext

import astropy.coordinates
import pytest
from pydantic import ValidationError

from aeonlib.salt.models import Block
from aeonlib.salt.models.block_models import ReferenceStar


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
            Block(**block)  # type: ignore

        assert True


class TestConstraints:
    def test_constraints(self, base_constraints):
        """Test that constraints can be built."""
        assert True


class TestAcquisition:
    def test_acquisition(self, base_acquisition):
        """Test that acquisitions can be built."""
        assert True


class TestReferenceStar:
    def test_reference_star(self, base_reference_star):
        """Test that reference stars can be built."""
        assert True

    @pytest.mark.parametrize(
        "dec, expectation",
        [
            (astropy.coordinates.Angle("-76.001d"), pytest.raises(ValueError)),
            (astropy.coordinates.Angle("-76d"), nullcontext()),
            (astropy.coordinates.Angle("11d"), nullcontext()),
            (astropy.coordinates.Angle("11.0001d"), pytest.raises(ValueError)),
        ],
    )
    def test_dec_range(self, dec, expectation, base_reference_star):
        ref_star = base_reference_star.model_dump()
        ref_star["dec"] = dec
        with expectation:
            ReferenceStar(**ref_star)  # type: ignore
