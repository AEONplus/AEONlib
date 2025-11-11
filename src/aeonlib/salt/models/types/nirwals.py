from typing import Literal


NirwalsGrating = Literal["NG0950"]
"""A NIRWALS grating."""


NirwalsFilter = Literal["empty"]
"""A NIRWALS filter."""


NirwalsCameraFilter = Literal[
    "block", "clear", "cutoff 1.5um", "cutoff 1.7um", "diffuser"
]
"""A NIRWALS camera filter."""


NirwalsOffsetType = Literal["FIF offset", "tracker guided offset"]
"""An offset type for NIRWALS."""


NirwalsExposureType = Literal["science", "sky"]
"""An exposure type for NIRWALS."""


NirwalsGain = Literal["faint"]
"""A gain option for NIRWALS."""


NirwalsSampling = Literal["up-the-ramp"]
"""A sampling mode for NIRWALS."""
