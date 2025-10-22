from contextlib import nullcontext
from typing import Annotated

import pytest
from pydantic import BaseModel, ValidationError

from aeonlib.validators import Ge, Gt, Le, Lt


class GtModel(BaseModel):
    a: Annotated[int, Gt(4)]


class GeModel(BaseModel):
    a: Annotated[int, Ge(4)]


class LtModel(BaseModel):
    a: Annotated[int, Lt(4)]


class LeModel(BaseModel):
    a: Annotated[int, Le(4)]


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
        """Test that the Gt validator validates correctly."""
        with expectation:
            GtModel(a=a)

    def test_greater_than_does_not_change_field_value(self):
        """Test that the field value is not changed by the Gt validator."""
        assert GtModel(a=7).a == 7

    @pytest.mark.parametrize(
        "a, expectation",
        [(3, pytest.raises(ValidationError)), (4, nullcontext()), (5, nullcontext())],
    )
    def test_greater_equal(self, a, expectation):
        """Test that the Ge validator validates correctly."""
        with expectation:
            GeModel(a=a)

    def test_greater_equal_does_not_change_field_value(self):
        """Test that the field value is not changed by the Ge validator."""
        assert GeModel(a=7).a == 7

    @pytest.mark.parametrize(
        "a, expectation",
        [
            (3, nullcontext()),
            (4, pytest.raises(ValidationError)),
            (5, pytest.raises(ValidationError)),
        ],
    )
    def test_less_than(self, a, expectation):
        """Test that the Lt validator validates correctly."""
        with expectation:
            LtModel(a=a)

    def test_less_than_does_not_change_field_value(self):
        """Test that the field value is not changed by the Lt validator."""
        assert LtModel(a=2).a == 2

    @pytest.mark.parametrize(
        "a, expectation",
        [(3, nullcontext()), (4, nullcontext()), (5, pytest.raises(ValidationError))],
    )
    def test_less_equal(self, a, expectation):
        """Test that the Le validator validates correctly."""
        with expectation:
            LeModel(a=a)

    def test_less_equal_does_not_change_field_value(self):
        """Test that the field value is not changed by the Le validator."""
        assert LeModel(a=2).a == 2
