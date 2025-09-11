import pytest
from pydantic import ValidationError

from aeonlib.salt.models import Request


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
