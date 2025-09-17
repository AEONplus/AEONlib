from __future__ import annotations

from typing import Annotated, Literal

from annotated_types import MinLen
from pydantic import BaseModel, PositiveInt

from aeonlib.salt.models.types import PositiveDuration, SalticamFilter
from aeonlib.salt.validators import GreaterEqual, LessEqual


class Salticam(BaseModel):
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

    Attributes
    ----------
    num_cycles
        How often to cycle through the filter sequence.
    filter_sequence
        Filter sequence.
    detector
        Detector setup.
    dither_pattern
        Dither pattern.
    include_flats:
        Whether flats should be taken for the observation.
    """

    num_cycles: PositiveInt = 1
    filter_sequence: Annotated[list[FilterSequenceStep], MinLen(1)]
    detector: SalticamDetector
    dither_pattern: None = None
    include_flats: bool


class FilterSequenceStep(BaseModel):
    """
    A step in a filter sequence.

    Attributes
    ----------
    filter
        Filter for the step.
    exposure_time
        Exposure time for the step, as a `astropy.units.Quantity` or as a float in
        seconds.
    """

    filter: SalticamFilter
    exposure_time: PositiveDuration


class SalticamDetector(BaseModel):
    """
    A Salticam detector setup.

    Only "normal" readout mode (i.e. a full frame readout) is supported. The readout
    speed may be "fast" or "slow", the gain "bright" or "faint". Up to 9 CCD rows and
    columns can be binned.

    The setup does not include the exposure time; this is set as part of a filter
    sequence step.
    """

    num_exposures: PositiveInt
    readout_mode: Literal["normal"] = "normal"
    gain: Literal["bright", "faint"]
    readout_speed: Literal["fast", "slow"]
    num_prebinned_rows: Annotated[int, GreaterEqual(1), LessEqual(9)]
    num_prebinned_columns: Annotated[int, GreaterEqual(1), LessEqual(9)]
