from __future__ import annotations

import math
from typing import Annotated, Literal, Any

from astropy import units as u
from pydantic import (
    BaseModel,
    PositiveInt,
    field_validator,
    PlainSerializer,
    BeforeValidator,
    computed_field,
)

from aeonlib.salt.models.types import (
    NirwalsCameraFilter,
    NirwalsExposureType,
    NirwalsFilter,
    NirwalsGain,
    NirwalsGrating,
    NirwalsOffsetType,
    NirwalsSampling,
    PositiveDuration,
)
from aeonlib.salt.models.util import (
    LowerCaseValidator,
    UpperCaseSerializer,
    CapitalizingSerializer,
)
from aeonlib.salt.validators import GreaterEqual, LessEqual
from aeonlib.types import Angle


class Nirwals(BaseModel, validate_assignment=True):
    """
    A NIRWALS configuration.

    Every NIRWALS configuration includes a dither pattern. If you want to repeat this
    pattern, you have to specify the number of cycles.

    Parameters
    ----------
    instrument_name:
        The instrument name, which is "NIRWALS".
    num_cycles
        The number of times the dither pattern should be done.
    grating
        The barcode of the grating to use.
    grating_angle
        The grating angle. This typically is half the articulation angle.
    articulation_angle
        The articulation angle. This must be a multiple of 0.5 degrees between 0 and 100
        degrees (both inclusive).
    filter
        The filter.
    camera_filter
        The camera filter.
    dither pattern
        The dither pattern.
    include_arc
        Whether a nighttime arc should be taken for the observation.
    include_flat
        Whether a nighttime flat should be taken for the observation.
    request_spectrophotometric_standard
        Whether a spectrophotometric standard should be taken for the observation.

    """

    instrument_name: Literal["NIRWALS"] = "NIRWALS"
    num_cycles: PositiveInt = 1
    grating: Annotated[NirwalsGrating, LowerCaseValidator]
    grating_angle: Annotated[Angle, GreaterEqual(0 * u.deg), LessEqual(100 * u.deg)]
    articulation_angle: Angle
    filter: Annotated[NirwalsFilter, LowerCaseValidator, UpperCaseSerializer] = "empty"
    camera_filter: Annotated[
        NirwalsCameraFilter, LowerCaseValidator, CapitalizingSerializer
    ]
    dither_pattern: list[NirwalsDitherPatternStep]
    include_arc: bool = True
    include_flat: bool
    request_spectrophotometric_standard: bool = False

    @field_validator("articulation_angle", mode="after")
    @classmethod
    def check_articulation_angle(cls, angle: Angle) -> Angle:
        error = "The articulation angle must be a multiple of 0.5 degress between 0 and 100 degrees (both inclusive"
        degrees = angle.to(u.deg).value

        if degrees < 0 or degrees > 100:
            raise ValueError(error)

        n = 2 * degrees
        if abs(n - round(n)) > 1e-6:
            raise ValueError(error)

        return angle


class NirwalsDitherPatternStep(BaseModel, validate_assignment=True):
    """
    A step in a NIRWALS dither pattern.

    Each step os characterised by the offset type and the offsets in horizontal and
    vertical direction, the exposure type and time, and other detector-related
    properties. The offset directions are the on-telescope directions (i.e. with the
    field rotated by the position angle)

    If a reference star is provided for the acquisition, for the first step the
    offset type must be "tracker guided offset" and the offsets must be equal to
    those from the reference star to the target.

    Parameters
    ----------
    offset_type
        The offset type.
    horizontal offset
        The offset in horizontal telescope direction. This must be between -100 and 100
        arcseconds (both inclusive).
    vertical_offset
        The offset in vertical telescope direction. This must be between -100 and 100
        arcseconds (both inclusive).
    exposure_type
        The exposure type.
    exposure_time
        The exposure time.
    gain
        The gain to use.
    sampling
        The sampling method to use.
    num_reads
        The number of detector readouts. This must be 1.
    num_ramps
        The number of ramps. This must be 1.
    """

    offset_type: Annotated[
        NirwalsOffsetType,
        LowerCaseValidator,
        PlainSerializer(NirwalsDitherPatternStep.serialize_offset_type),
    ]
    horizontal_offset: Annotated[
        Angle, GreaterEqual(-100 * u.arcsec), LessEqual(100 * u.arcsec)
    ]
    vertical_offset: Annotated[
        Angle, GreaterEqual(-100 * u.arcsec), LessEqual(100 * u.arcsec)
    ]
    exposure_type: Annotated[
        NirwalsExposureType, LowerCaseValidator, CapitalizingSerializer
    ]
    exposure_time: PositiveDuration
    gain: Annotated[NirwalsGain, LowerCaseValidator, CapitalizingSerializer]
    sampling: Annotated[
        NirwalsSampling,
        BeforeValidator(NirwalsDitherPatternStep.validate_sampling),
        PlainSerializer(NirwalsDitherPatternStep.serialize_sampling),
    ]
    num_reads: Literal[1] = 1
    num_ramps: Literal[1] = 1

    @computed_field
    @property
    def num_groups(self) -> int:
        """
        The number of groups.

        The number of groups is equal to the ratio of the exposure time and the product
        of reads and frame rate. A value of 0.728 seconds is assumed for the frame rate.

        Returns
        -------
        The number of groups.
        """
        frame_rate = 0.728 * u.s
        # The actual frame rate value is 0.727750 s. However, as a safety measure and to
        # avoid rounding differences between different pieces of software, a rounded
        # value is used.

        groups = round(
            math.floor(float(self.exposure_time / (self.num_reads * frame_rate)))
        )
        return max(1, groups)

    @staticmethod
    def serialize_offset_type(value: NirwalsOffsetType) -> str:
        if value == "fif offset":
            return "FIF Offset"
        else:
            return value.title()

    @staticmethod
    def serialize_sampling(value: NirwalsSampling) -> str:
        if value == "up-the-ramp":
            return "Up-the-Ramp Group"
        else:
            raise ValueError(f"Sampling cannot be serialized: {value}")

    @staticmethod
    def validate_sampling(value: Any) -> Any:
        if isinstance(value, str):
            value = value.lower()
        if value == "up-the-ramp group":
            value = "up-the-ramp"
        return value
