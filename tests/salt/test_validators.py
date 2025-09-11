from contextlib import nullcontext
from typing import Annotated

import pytest
from pydantic import BaseModel, ValidationError

from aeonlib.salt.validators import GreaterEqual, LessEqual


class GreaterEqualModel(BaseModel):
    a: Annotated[int, GreaterEqual(4)]


class LessEqualModel(BaseModel):
    a: Annotated[int, LessEqual(4)]


class TestValidators:
    @pytest.mark.parametrize(
        "a, expectation",
        [(3, pytest.raises(ValidationError)), (4, nullcontext()), (5, nullcontext())],
    )
    def test_greater_equal(self, a, expectation):
        with expectation:
            GreaterEqualModel(a=a)

    def test_greater_equal_does_not_change_field_value(self):
        """Test that the field value is not changed by the GreaterEqual validator."""
        assert GreaterEqualModel(a=7).a == 7

    @pytest.mark.parametrize(
        "a, expectation",
        [(3, nullcontext()), (4, nullcontext()), (5, pytest.raises(ValidationError))],
    )
    def test_less_equal(self, a, expectation):
        with expectation:
            LessEqualModel(a=a)

    def test_less_equal_does_not_change_field_value(self):
        """Test that the field value is not changed by the LessEqual validator."""
        assert LessEqualModel(a=2).a == 2
