import pytest
from pydantic import ValidationError

from aeonlib.models import SiderealTarget
from aeonlib.utils.django import omit_none


def test_omit_none():
    sidereal_target_given = {
        "name": "test with None",
        "type": "ICRS",
        "ra": 12.3,
        "dec": 45.6,
        "epoch": None,  # we want the default for this
    }

    with pytest.raises(ValidationError):
        # None is not a valid value for epoch
        SiderealTarget.model_validate(sidereal_target_given)

    sidereal_target = SiderealTarget(**omit_none(sidereal_target_given))
    assert sidereal_target.epoch == 2000
