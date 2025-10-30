from __future__ import annotations

from typing import Literal

from astropy import units as u
from pydantic import BaseModel, PositiveInt, field_validator

from aeonlib.types import Angle
from aeonlib.salt.models.types.filters import RssImagingFilter, SalticamFilter


class Rss(BaseModel):
    """
    An RSS configuration.

    RSS can be used in different configurations:

    - Imaging.
    - Longslit spectroscopy.
    - Multiobject spectroscopy (MOS).
    - Spectroscopy with a Slit Mask Integrated Fibre Unit (IFU).

    All of these may be used for polarimetric observations, i.e. with a wave plate
    pattern for a half wave plate H and a quarter wave plate Q. If you want to
    perform this pattern more than once, you can specify a number of cycles. These
    should not be confused with the number of exposures, which is defined for the
    detector.

    For example, assume you perform polarimetry with a pattern (H1, Q1), (H2,  Q2).
    Then two cycles and 1 exposure would result in the following observing
    sequence:

    (H1, Q1) - (H2, Q2) - (H1, Q1) - (H2, Q2)

    On the other hand, one cycle and two exposures would result in the following
    sequence:

    (H1, Q1) - (H1, Q1) - (H2, Q2) - (H2, Q2)

    You may define a dither pattern, in which case the wave plate sequence (with its
    cycles and exposures) applies to each dither pattern step.

    Attributes
    ----------
    num_cycles
        How often to cycle through the wave plate sequence. This is only relevant if
        you perform polarimetry.
    configuration
        Imaging or spectroscopy configuration.
    detector
        Detector setup.
    dither_pattern
        Dither pattern.
    """

    num_cycles: PositiveInt = 1
    configuration: RssImaging
    detector: None
    dither_pattern: None


class RssImaging(BaseModel):
    """
    An RSS imaging configuration.

    Attributes
    ----------
    filter
        The filter to use. This may be one of RSS's own imaging filters or one of the
        filters used by Salticam.
    polarimetry
        The (optional) polarimetry setup to use.
    include_flat
        Whether a nighttime flat should be taken for the observation.
    """

    filter: RssImagingFilter | SalticamFilter
    polarimetry: RssPolarimetry | None
    include_flat: bool


_WavePlatePattern = (
    Literal["linear", "linear hi", "circular", "all-Stokes"]
    | list[tuple[Angle | None, Angle | None]]
)


class RssPolarimetry(BaseModel):
    """
    An RSS polarimetry setup.

    The setup is defined by a wave plate pattern, which may be specified by the name
    of a predefined pattern ("linear", "linear hi", "circular" or "all-Stokes") or by
    explicitly defining the list of half and quarter wave plate angles. In case of
    the latter, the list must consist of pairs of angles, with the first angle being
    that of the half wave plate and the second being that of the quarter wave plate.
    Each angle must bee a multiple of 11.25 degrees. It may be None if the respective
    wave plate is not used.

    For example, the "linear" and "circular" patterns could be given as::

        linear = RssPolarimetry(wave_plate_pattern="linear")
        circular = RssPolarimetry(wave_plate_pattern="linear")

    or as::

        from astropy import units as u

        linear = RssPolarimetry(
            wave_plate_pattern=[
                (0 * u.deg, None),
                (45 * u.deg, None),
                (22.5 * u.deg, None),
                (67.5 * u.deg, None),
            ]
        )
        circular = RssPolarimetry(
            wave_plate_pattern=[(0 * u.deg, 45 * u.deg), (0 * u.deg, 315 * u.deg)]
        )

    A wave plate pattern may have up to 8 steps.
    """

    wave_plate_pattern: _WavePlatePattern

    @field_validator("wave_plate_pattern", mode="after")
    @classmethod
    def check_pattern_size(cls, value: _WavePlatePattern) -> _WavePlatePattern:
        if isinstance(value, str):
            return value

        if len(value) < 1 or len(value) > 8:
            raise ValueError("The wave plate pattern must have between 1 and 8 steps.")

        return value

    @classmethod
    def _check_pattern_step(cls, step: tuple[Angle, Angle]) -> None:
        error = (
            "Each angle in a wave plate pattern must be a multiple of 11.25 degrees "
            "between 0 degrees (inclusive) and 360 degrees (exclusive)."
        )
        for angle in step:
            if angle < 0 * u.deg or angle >= 360 * u.deg:
                raise ValueError(error)

            # Check that the ratio of the angle and 11.25 deg is (very close to) an
            # integer.
            x = (angle.to(u.deg) / 11.25).value
            if abs(round(x) - x) > 1e-6:
                raise ValueError(error)

    @field_validator("wave_plate_pattern", mode="after")
    @classmethod
    def check_angle_values(cls, value: _WavePlatePattern) -> _WavePlatePattern:
        if isinstance(value, str):
            return value

        for step in value:
            RssPolarimetry._check_pattern_step(step)

        return value
