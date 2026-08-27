from datetime import UTC

from gpp_client.generated.enums import TimingWindowInclusion
from gpp_client.generated.input_types import (
    DeclinationInput,
    ParallaxInput,
    ProperMotionComponentInput,
    ProperMotionInput,
    RightAscensionInput,
    SiderealInput,
    TargetPropertiesInput,
    TimingWindowEndInput,
    TimingWindowInput,
)

from aeonlib.models import SiderealTarget, Window


def target_properties_from_aeon(target: SiderealTarget) -> TargetPropertiesInput:
    """Convert an Aeonlib ICRS target to Gemini target properties."""
    if target.type != "ICRS":
        raise ValueError(
            "Gemini target conversion only supports ICRS SiderealTarget objects"
        )

    return TargetPropertiesInput(
        name=target.name,
        sidereal=SiderealInput(
            ra=RightAscensionInput(degrees=target.ra.to_value("deg")),
            dec=DeclinationInput(degrees=target.dec.to_value("deg")),
            epoch=f"J{target.epoch:.3f}",
            proper_motion=ProperMotionInput(
                ra=ProperMotionComponentInput(
                    milliarcseconds_per_year=target.proper_motion_ra
                ),
                dec=ProperMotionComponentInput(
                    milliarcseconds_per_year=target.proper_motion_dec
                ),
            ),
            parallax=ParallaxInput(milliarcseconds=target.parallax),
        ),
    )


def timing_window_from_aeon(window: Window) -> TimingWindowInput:
    """Convert an Aeonlib window to a finite Gemini inclusion window."""
    if window.start is None:
        raise ValueError("Gemini timing windows require a start time")

    return TimingWindowInput(
        inclusion=TimingWindowInclusion.INCLUDE,
        start_utc=window.start.to_datetime(timezone=UTC),
        end=TimingWindowEndInput(at_utc=window.end.to_datetime(timezone=UTC)),
    )
