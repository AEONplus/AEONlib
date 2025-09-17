import pytest
from pydantic import ValidationError

from aeonlib.salt.models import Salticam


class TestSalticam:
    def test_salticam(self, base_salticam):
        """Test that Salticam configurations can be built."""
        assert True

    def test_at_least_one_filter(self, base_salticam):
        """Test that the filter sequence must have at least one step."""
        salticam = base_salticam.model_dump()
        salticam["filter_sequence"] = []
        with pytest.raises(ValidationError, match="at least 1"):
            Salticam(**salticam)
