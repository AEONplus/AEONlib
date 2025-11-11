from typing import Annotated

from astropy import units as u
from pydantic import BaseModel, PositiveInt, field_validator

from aeonlib.salt.models.types import NirwalsCameraFilter, NirwalsFilter, NirwalsGrating
from aeonlib.salt.validators import GreaterEqual, LessEqual
from aeonlib.types import Angle


class Nirwals(BaseModel):
    """
    A NIRWALS configuration.

    Every NIRWALS configuration includes a dither pattern. If you want to repeat this
    pattern, you have to specify the number of cycles.

    Attributes
    ----------
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

    num_cycles: PositiveInt = 1
    grating: NirwalsGrating
    grating_angle: Annotated[Angle, GreaterEqual(0 * u.deg), LessEqual(100 * u.deg)]
    articulation_angle: Angle
    filter: NirwalsFilter = "empty"
    camera_filter: NirwalsCameraFilter
    dither_pattern: None
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
