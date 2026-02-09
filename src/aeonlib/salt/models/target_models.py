"""This module contains Pydantic models for targets to observe with SALT."""

from __future__ import annotations

from typing import Self

import astropy.coordinates
from pydantic import BaseModel, NonNegativeFloat, field_validator, model_validator

from aeonlib.models import SiderealTarget
from aeonlib.salt.models.types import MagnitudeBandpass, TargetType
from aeonlib.salt.validators import check_in_visibility_range


class SaltSiderealTarget(SiderealTarget):
    """
    A sidereal target to observe with SALT.

    This model extends the `SiderealTarget` model by adding a target type and a
    magnitude range.

    Parameters
    ----------
    target_type
        Target type. This must be the label for SIMBAD object type (see
        http://simbad.cds.unistra.fr/guide/otypes.htx). Examples are "TTau*" and
        "StarburstG".
    magnitude_range
        Magnitude range for the range.
    """

    target_type: TargetType
    magnitude_range: MagnitudeRange

    @field_validator("dec", mode="after")
    @classmethod
    def check_declination_viewable(cls, value: astropy.coordinates.Angle):
        return check_in_visibility_range(value)


class MagnitudeRange(BaseModel, validate_assignment=True):
    """
    A magnitude range.

    The minimum (brightest) and maximum (faintest) magnitude must be give for a
    particular bandpass filter.

    Parameters
    ----------
    min_magnitude
        Minimum (brightest) magnitude.
    max_magnitude
        Maximum (faintest) magnitude. This must be greater than or equal to the minimum
        magnitude.
    bandpass
        Bandpass filter for which the magnitude range is given.
    """

    min_magnitude: NonNegativeFloat

    max_magnitude: NonNegativeFloat

    bandpass: MagnitudeBandpass

    @model_validator(mode="after")
    def check_max_magnitude_is_at_least_min_magnitude(self) -> Self:
        if self.min_magnitude > self.max_magnitude:
            raise ValueError(
                "max_magnitude must be greater than or equal to min_magnitude."
            )

        return self
