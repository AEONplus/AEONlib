from contextlib import nullcontext

import pytest
from pydantic import ValidationError

from aeonlib.salt.models import Request, Block


@pytest.fixture()
def base_request(base_block):
    """A simple request to edit or build from."""
    return Request(proposal_code="2025-1-SCI-042", blocks=[base_block])


@pytest.fixture()
def base_block():
    """A simple block to build or edit from."""
    return Block(
        name="Test",
        priority=1,
        ranking="high",
        num_visits=1,
        constraints=None,
        target=None,
        acquisition=None,
        instrument=None,
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
