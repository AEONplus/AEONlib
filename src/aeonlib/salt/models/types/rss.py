from typing import Literal

RssImagingFilter = Literal[
    "pi04340",
    "pi04400",
    "pi04465",
    "pi04530",
    "pi04600",
    "pi04670",
    "pi04740",
    "pi04820",
    "pi04895",
    "pi04975",
    "pi05060",
    "pi05145",
    "pi05235",
    "pi05325",
    "pi05420",
    "pi05520",
    "pi05620",
    "pi05725",
    "pi05830",
    "pi05945",
    "pi06055",
    "pi06170",
    "pi06290",
    "pi06410",
    "pi06530",
    "pi06645",
    "pi06765",
    "pi06885",
    "pi07005",
    "pi07130",
    "pi07260",
    "pi07390",
    "pi07535",
    "pi07685",
    "pi07840",
    "pi08005",
    "pi08175",
    "pi08350",
    "pi08535",
    "pi08730",
]
"""An imaging filter for RSS."""


RssOrderBlockingFilter = Literal["pc00000", "pc03200", "pc03400", "pc03850", "pc04600"]
"""An order blocking filter for RSS."""


RssGrating = Literal["pg0700", "pg0900", "pg1300", "pg1800", "pg2300", "pg3000"]
"""An RSS grating."""
