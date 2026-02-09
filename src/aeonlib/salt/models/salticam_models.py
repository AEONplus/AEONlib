from __future__ import annotations

from typing import Annotated, Literal, Union

from annotated_types import MinLen
from astropy import units as u
from astropy.units import Quantity
from pydantic import BaseModel, PositiveInt, Field, model_validator

from aeonlib.salt.models.types import (
    PositiveDuration,
    SalticamFilter,
    SalticamFilterSerializer,
    AstropyQuantityTypeAnnotation,
)
from aeonlib.salt.models.util import CapitalizingSerializer, LowerCaseValidator
from aeonlib.salt.validators import GreaterEqual, LessEqual


class Salticam(BaseModel, validate_assignment=True):
    """
    A Salticam instrument configuration.

    Several filters can be requested in the configuration. If you want to repeat the
    sequence, you can set a number of cycles. This should not be confused with the
    number of exposures, which is set for the detector.

    For example, if the configuration requests the Johnson U and Johnson V filter, one
    cycle and two exposures correspond to the sequence

    U - U - V - V

    whereas two cycles and one exposure corresponds to

    U - V - U - V

    You may define a dither pattern, in which case the filter sequence (with its cycles
    and exposures) applies to each dither pattern step.

    Parameters
    ----------
    num_cycles
        How often to cycle through the filter sequence.
    filter_sequence
        Filter sequence.
    detector
        Detector setup.
    dither_pattern
        Dither pattern.
    include_flat:
        Whether a nighttime flat should be taken for the observation.
    """

    num_cycles: PositiveInt = 1
    filter_sequence: Annotated[list[SalticamFilterSequenceStep], MinLen(1)]
    detector: SalticamDetector
    dither_pattern: SalticamDitherPattern = None
    include_flat: bool


class SalticamFilterSequenceStep(BaseModel, validate_assignment=True):
    """
    A step in a filter sequence.

    Parameters
    ----------
    filter
        Filter for the step.
    exposure_time
        Exposure time for the step, as a `astropy.units.Quantity` or as a float in
        seconds.
    """

    filter: Annotated[SalticamFilter, LowerCaseValidator, SalticamFilterSerializer]
    exposure_time: PositiveDuration


class SalticamDetector(BaseModel, validate_assignment=True):
    """
    A Salticam detector setup.

    Only "normal" readout mode (i.e. a full frame readout) is supported. The readout
    speed may be "fast" or "slow", the gain "bright" or "faint". Up to 9 CCD rows and
    columns can be binned.

    The setup does not include the exposure time; this is set as part of a filter
    sequence step.
    """

    num_exposures: PositiveInt
    readout_mode: Annotated[Literal["normal"], CapitalizingSerializer] = "normal"
    gain: Annotated[Literal["bright", "faint"], CapitalizingSerializer]
    readout_speed: Annotated[Literal["fast", "slow"], CapitalizingSerializer]
    num_prebinned_rows: Annotated[int, GreaterEqual(1), LessEqual(9)]
    num_prebinned_columns: Annotated[int, GreaterEqual(1), LessEqual(9)]


class SalticamDitherPattern(BaseModel, validate_assignment=True):
    """
    A dither pattern for Salticam.

    The dither pattern is characterised by the number of rows and columns it covers,
    the number of steps to take, and the offset between the steps.

    By default, the number of steps is the product of rows and columns, but you may
    specify a multiple of that number if you want to perform the pattern more than once.

    The offset is in detector coordinates, not in right ascension and declination.
    Therefore, if a particular object orientation is desired, a suitable position
    angle must be chosen so that the dithers coincide with the detector axes.

    Parameters
    ----------
    num_rows
        Number of rows in the pattern.
    num_columns
        Number of columns in the pattern.
    number_steps
        Number of steps to perform.
    offset
        Offset between steps, as a `astropy.units.Quantity` or as a float in arcsec.
    """

    num_rows: PositiveInt
    num_columns: PositiveInt
    num_steps: PositiveInt = Field(
        default_factory=lambda data: data["num_rows"] * data["num_columns"]
    )
    offset: Annotated[
        Union[Quantity, float], AstropyQuantityTypeAnnotation(default_unit=u.arcsec)
    ]

    @model_validator(mode="after")
    def check_number_of_steps(self):
        if self.num_steps % (self.num_rows * self.num_columns) != 0:
            raise ValueError(
                "The number of steps must be the number of rows times the number of "
                "columns, or a multiple thereof."
            )
        return self
