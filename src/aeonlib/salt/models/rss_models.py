from pydantic import BaseModel, PositiveInt


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
    configuration: None
    detector: None
    dither_pattern: None
