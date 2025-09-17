from typing import Annotated

from annotated_types import MinLen
from pydantic import BaseModel, PositiveInt


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
    filter_sequence: Annotated[list[None], MinLen(1)]
    detector: None
    dither_pattern: None = None
    include_flats: bool
