from contextlib import nullcontext

import pytest
from pydantic import ValidationError

from aeonlib.salt.models import Block


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


class TestConstraints:
    def test_constraints(self, base_constraints):
        """Test that constraints can be built."""
        assert True
