# pyright: reportUnknownArgumentType=false
from datetime import datetime

import pytest
from astropy.coordinates.earth import Angle
from astropy.time import Time

from aeonlib.eso.models import AbsoluteTimeConstraint, Target
from aeonlib.models import SiderealTarget, Window


def test_constraints_from_window():
    window = Window(
        start=Time(60775.0, scale="utc", format="mjd"),
        end=Time(60776.0, scale="utc", format="mjd"),
    )

    abs_constraint = AbsoluteTimeConstraint.construct_from(window)

    assert abs_constraint.start == datetime(2025, 4, 10, 0, 0)
    assert abs_constraint.end == datetime(2025, 4, 11, 0, 0)


def test_constraints_from_window_must_enter_start():
    with pytest.raises(ValueError):
        _ = AbsoluteTimeConstraint.construct_from(
            Window(start=None, end=Time(60776.0, scale="utc", format="mjd"))
        )


def test_eso_target_from_sidereal_target():
    sidereal_target = SiderealTarget(
        name="Test Target",
        ra=Angle(24.5, unit="deg"),
        dec=Angle(12.5, unit="deg"),
        type="ICRS",
    )

    eso_target = Target(
        dec="00:00:00.000",
        differential_dec=0.0,
        differential_ra=0.0,
        epoch=2000.0,
        equinox="J2000",
        name="No name",
        proper_motion_dec=0.0,
        proper_motion_ra=0.0,
        ra="00:00:00.000",
    )

    eso_target.construct_from(sidereal_target)

    assert eso_target.name == "Test Target"
    assert eso_target.ra == "24:30:00.000"
    assert eso_target.dec == "12:30:00.000"
