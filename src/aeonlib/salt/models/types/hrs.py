from typing import Literal

HrsMode = Literal[
    "low resolution", "medium resolution", "high resolution", "high stability"
]
"""An HRS instrument mode."""


HrsPrvCalibration = Literal["ThAr", "thar"]
"""An HRS precision radial velocity calibration."""
