from contextlib import nullcontext
from typing import Annotated

import pytest
from pydantic import BaseModel, ValidationError

from aeonlib.salt.validators import GreaterEqual, GreaterThan, LessEqual, LessThan


class GreaterThanModel(BaseModel):
    a: Annotated[int, GreaterThan(4)]


class GreaterEqualModel(BaseModel):
    a: Annotated[int, GreaterEqual(4)]


class LessThanModel(BaseModel):
    a: Annotated[int, LessThan(4)]


class LessEqualModel(BaseModel):
    a: Annotated[int, LessEqual(4)]


class TestValidators:
    @pytest.mark.parametrize(
        "a, expectation",
        [
            (3, pytest.raises(ValidationError)),
            (4, pytest.raises(ValidationError)),
            (5, nullcontext()),
        ],
    )
    def test_greater_than(self, a, expectation):
        """Test that the GreaterThan validator validates correctly."""
        with expectation:
            GreaterThanModel(a=a)

    def test_greater_than_does_not_change_field_value(self):
        """Test that the field value is not changed by the GreaterThan validator."""
        assert GreaterThanModel(a=7).a == 7

    @pytest.mark.parametrize(
        "a, expectation",
        [(3, pytest.raises(ValidationError)), (4, nullcontext()), (5, nullcontext())],
    )
    def test_greater_equal(self, a, expectation):
        """Test that the GreaterEqual validator validates correctly."""
        with expectation:
            GreaterEqualModel(a=a)

    def test_greater_equal_does_not_change_field_value(self):
        """Test that the field value is not changed by the GreaterEqual validator."""
        assert GreaterEqualModel(a=7).a == 7

    @pytest.mark.parametrize(
        "a, expectation",
        [
            (3, nullcontext()),
            (4, pytest.raises(ValidationError)),
            (5, pytest.raises(ValidationError)),
        ],
    )
    def test_less_than(self, a, expectation):
        """Test that the LessThan validator validates correctly."""
        with expectation:
            LessThanModel(a=a)

    def test_less_than_does_not_change_field_value(self):
        """Test that the field value is not changed by the LessThan validator."""
        assert LessThanModel(a=2).a == 2

    @pytest.mark.parametrize(
        "a, expectation",
        [(3, nullcontext()), (4, nullcontext()), (5, pytest.raises(ValidationError))],
    )
    def test_less_equal(self, a, expectation):
        """Test that the LessEqual validator validates correctly."""
        with expectation:
            LessEqualModel(a=a)

    def test_less_equal_does_not_change_field_value(self):
        """Test that the field value is not changed by the LessEqual validator."""
        assert LessEqualModel(a=2).a == 2
