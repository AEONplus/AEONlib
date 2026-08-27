from datetime import UTC, datetime

import pytest
from astropy.time import Time
from gpp_client.generated.enums import TimingWindowInclusion

from aeonlib.gemini.conversions import (
    target_properties_from_aeon,
    timing_window_from_aeon,
)
from aeonlib.models import SiderealTarget, Window


def test_target_properties_from_aeon():
    target = SiderealTarget(
        name="test target",
        type="ICRS",
        ra=12.3,
        dec=-45.6,
        epoch=2015,
        proper_motion_ra=1.2,
        proper_motion_dec=-3.4,
        parallax=5.6,
    )

    result = target_properties_from_aeon(target)

    assert result.name == "test target"
    assert result.sidereal is not None
    assert result.sidereal.ra is not None
    assert result.sidereal.ra.degrees == 12.3
    assert result.sidereal.dec is not None
    assert result.sidereal.dec.degrees == -45.6
    assert result.sidereal.epoch == "J2015.000"
    assert result.sidereal.proper_motion is not None
    assert result.sidereal.proper_motion.ra.milliarcseconds_per_year == 1.2
    assert result.sidereal.proper_motion.dec.milliarcseconds_per_year == -3.4
    assert result.sidereal.parallax is not None
    assert result.sidereal.parallax.milliarcseconds == 5.6


def test_target_properties_rejects_non_icrs():
    target = SiderealTarget(name="test", type="HOUR_ANGLE", ra=12.3, dec=-45.6)
    with pytest.raises(ValueError, match="only supports ICRS"):
        target_properties_from_aeon(target)


def test_timing_window_from_aeon():
    window = Window(
        start=Time("2026-08-27T01:02:03", scale="utc"),
        end=Time("2026-08-28T04:05:06", scale="utc"),
    )

    result = timing_window_from_aeon(window)

    assert result.inclusion is TimingWindowInclusion.INCLUDE
    assert result.start_utc == datetime(2026, 8, 27, 1, 2, 3, tzinfo=UTC)
    assert result.end is not None
    assert result.end.at_utc == datetime(2026, 8, 28, 4, 5, 6, tzinfo=UTC)
    assert result.end.after is None
    assert result.end.repeat is None


def test_timing_window_requires_start():
    window = Window(start=None, end=Time("2026-08-28T04:05:06", scale="utc"))

    with pytest.raises(ValueError, match="require a start time"):
        timing_window_from_aeon(window)
