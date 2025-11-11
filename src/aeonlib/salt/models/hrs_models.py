from __future__ import annotations

from typing import Annotated, Self

from astropy import units as u
from pydantic import BaseModel, Field, PositiveInt, model_validator

from aeonlib.salt.models.types import HrsMode, HrsPrvCalibration, PositiveDuration
from aeonlib.salt.validators import GreaterEqual, LessEqual
from aeonlib.types import Angle


class Hrs(BaseModel):
    """
    An HRS setup.

    HRS can be used in any of four modes, namely low resolution, medium resolution, high
    resolution and high stability. A high precision velocity calibration (using a ThAr
    kamp) is available for the high stability mode, but not for any of the other modes.

    A sequence of exposure times can be defined for the red and blue detector arm. If
    this sequence shall be executed more than once, a number of cycles need to be set.

    Attributes
    ----------
    num_cycles
        How often the exposure time patterns shall be executed.
    mode
        The instrument mode, such low resolution or high stability.
    prv_calibration
        The high precision velocity calibration to use. This must be None for all modes
        other than high stability, for which it must be "ThAr".
    fibre_separation
        The angle between the target and sky fibres. This must be between 16 and 63
        arcseconds (both inclusive).
    blue_arm: None
        The detector setup for the red arm.
    red_arm: None
        The detector setup for the blue arm.
    """

    num_cycles: PositiveInt = 1
    mode: HrsMode
    prv_calibration: HrsPrvCalibration | None = Field(
        default_factory=lambda data: (
            "ThAr" if data["mode"] == "high stability" else None
        )
    )
    fibre_separation: Annotated[
        Angle, GreaterEqual(16 * u.arcsec), LessEqual(63 * u.arcsec)
    ] = (60 * u.arcsec)
    blue_arm: HrsDetector
    red_arm: HrsDetector

    @model_validator(mode="after")
    def check_prv_calibration(self) -> Self:
        if self.mode == "high stability":
            if self.prv_calibration != "ThAr":
                raise ValueError(
                    'prv_calibration must be "ThAr" for the high stability mode.'
                )
        else:
            if self.prv_calibration is not None:
                raise ValueError(
                    f"prv_calibration must be None for the {self.mode} mode."
                )
        return self


class HrsDetector(BaseModel):
    """
    An HRS detector setup.

    A list of exposure times for the detector has to be specified. These exposure times
    may be different for the blue and the red detector.

    Other detector properties, such as the readout speed or the binning, cannot be set.
    """

    exposure_times: list[PositiveDuration]
