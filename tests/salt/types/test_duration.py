from contextlib import nullcontext

import pytest

from astropy import units as u
from pydantic import ValidationError, BaseModel

from aeonlib.salt.models.types import Duration, PositiveDuration


class A(BaseModel):
    a: Duration


class B(BaseModel):
    b: PositiveDuration


class TestDuration:
    @pytest.mark.parametrize("a", [5, 5 * u.s])
    def test_duration(self, a):
        """Test that durations are stored with a unit."""
        v = A(a=a)
        assert v.a.value == 5
        assert v.a.unit == u.s


class TestPositiveDuration:
    @pytest.mark.parametrize(
        "b, expectation",
        [
            (-5.6, pytest.raises(ValidationError)),
            (-3 * u.s, pytest.raises(ValidationError)),
            (0, pytest.raises(ValidationError)),
            (0 * u.s, pytest.raises(ValidationError)),
            (0.001, nullcontext()),
            (67 * u.s, nullcontext()),
        ],
    )
    def test_positive_duration_must_be_positive(self, b, expectation):
        with expectation:
            B(b=b)
        assert True
