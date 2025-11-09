from __future__ import annotations

from typing import Literal, Annotated

from astropy import units as u
from pydantic import BaseModel, FilePath, PositiveInt, field_validator

from aeonlib.types import Angle
from aeonlib.salt.models.types import (
    PositiveDuration,
    RssGain,
    RssGrating,
    RssImagingFilter,
    RssOrderBlockingFilter,
    RssReadoutMode,
    RssReadoutSpeed,
    RssSlitMaskIFU,
    SalticamFilter,
)
from aeonlib.salt.validators import GreaterEqual, GreaterThan, LessEqual


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
        Imaging, longslit, multiobject spectroscopy or slit mask IFU configuration.
    detector
        Detector setup.
    dither_pattern
        Dither pattern.
    """

    num_cycles: PositiveInt = 1
    configuration: (
        RssImaging
        | RssLongslitSpectroscopy
        | RssMultiObjectSpectroscopy
        | RssSlitMaskIFUSpectroscopy
    )
    detector: RssDetector
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
        The (optional) polarimetry setup.
    include_flat
        Whether a nighttime flat should be taken for the observation.
    """

    filter: RssImagingFilter | SalticamFilter
    polarimetry: RssPolarimetry | None = None
    include_flat: bool


_WavePlatePattern = (
    Literal["linear", "linear hi", "circular", "all-Stokes"]
    | list[tuple[Angle | None, Angle | None]]
)


class RssSpectroscopy(BaseModel):
    """
    An RSS spectroscopy configuration.

    While the grating, articulation, polarimetry and calibrations are defined by this
    class, the slit mask (or IFU) to use is specified in a child class.

    Attributes
    ----------
    grating
        The barcode of the grating, such as "pg0900".
    grating_angle
        The grating angle. The default is half the articulation angle.
    articulation_angle
        The articulation angle of the camera. This must be either 0 deg or one of the
        values 1.75 deg + (n - 1) * 0.75 deg, where 1 <= n <= 132.
    order_blocking_filter
        The order blocking filter.
    polarimetry
        The (optional) polarimetry setup.
    include_flat
        Whether a nighttime flat should be taken for the observation.
    include_arc
        Whether a nighttime arc should be taken for the observation.
    request_photometric_standard
        Whether a photometric standard should be taken for the observation.

    """

    grating: RssGrating
    grating_angle: Annotated[Angle, GreaterEqual(0 * u.deg), LessEqual(100 * u.deg)]
    articulation_angle: Angle
    order_blocking_filter: RssOrderBlockingFilter
    polarimetry: RssPolarimetry | None = None
    include_flat: bool
    include_arc: bool = True
    request_spectrophotometric_standard: bool = False

    @field_validator("articulation_angle", mode="after")
    @classmethod
    def check_articulation_angle(cls, angle: Angle) -> Angle:
        error = "The articulation angle must either be 0 deg or a value 1.75 deg + (n - 1) * 0.75 deg with 1 <= n <= 132."
        degrees = angle.to(u.deg).value

        if degrees < 0:
            raise ValueError(error)

        grace = 1e-6
        if abs(degrees) < grace:
            return angle

        n = (degrees - 1.75) / 0.75 + 1
        if n < 1 - grace or n > 132 + grace:
            raise ValueError(error)

        if abs(n - round(n)) > grace:
            raise ValueError

        return angle


class RssLongslitSpectroscopy(RssSpectroscopy):
    """
    An RSS longslit spectroscopy setup.

    In addition to the properties required by a generic RSS spectroscopy the user must
    specify the barcode of the longslit to use.

    Attributes
    ----------
    slit
        The barcode of the longslit, such as "PL0125N001".
    """

    slit: str


class RssMultiObjectSpectroscopy(RssSpectroscopy):
    """
    An RSS multiobject spectroscopy (MOS) setup.

    In addition to the properties required by a generic RSS spectroscopy the user must
    specify the path of the file describing the MOS mask. The path must exist and must
    be a file.

    Attributes
    ----------
    mask
        The file path of the file describing the MOS mask.
    """

    mask: FilePath


class RssSlitMaskIFUSpectroscopy(RssSpectroscopy):
    """
    An RSS slit mask integrated field unit (IFU) setup.

    In addition to the properties required by a generic RSS spectroscopy the user must
    specify the barcode of the slit mask IFU to use.

    Attributes
    ----------
    slit_mask_ifu
        The barcode of the slit mask IFU, such as "PF0200N001".
    """

    slit_mask_ifu: RssSlitMaskIFU


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


class RssDetector(BaseModel):
    """
    An Rss detector setup.

    Attributes
    ----------
    exposure_time
        The exposure time. If multiple exposures are requested, this is the time per
        exposure.
    num_exposures
        The number of exposures to take.
    readout_mode
        The readout mode.
    gain
        The gain.
    readout_speed
        The readout speed.
    num_prebinned_rows
        The number of prebinned rows, which must be between 1 and 9 (both inclusive).
    num_prebinned_columns
        The number of prebinned columns, which must be between 1 and 9 (both inclusive).
    window_height
        The height of the detector window, which must be a positive angle less than
        or equal to 518 arcseconds. In most cases there is no need to define a
        detector window.
    """

    exposure_time: PositiveDuration
    num_exposures: int = 1
    readout_mode: RssReadoutMode = "normal"
    gain: RssGain
    readout_speed: RssReadoutSpeed
    num_prebinned_rows: Annotated[int, GreaterEqual(1), LessEqual(9)]
    num_prebinned_columns: Annotated[int, GreaterEqual(1), LessEqual(9)]
    window_height: Annotated[
        Angle | None, GreaterThan(0 * u.arcsec), LessEqual(518 * u.arcsec)
    ] = None
