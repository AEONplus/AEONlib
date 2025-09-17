# This file is generated automatically and should not be edited by hand.

from typing import Any, Annotated, Literal, Union

from annotated_types import Le
from pydantic import BaseModel, ConfigDict
from pydantic.types import NonNegativeInt, PositiveInt

from aeonlib.models import TARGET_TYPES
from aeonlib.ocs.target_models import Constraints
from aeonlib.ocs.config_models import Roi


class BlancoNewfirmOpticalElements(BaseModel):
    model_config = ConfigDict(validate_assignment=True)
    filter: Literal["JX", "HX", "KXs"]


class BlancoNewfirmGuidingConfig(BaseModel):
    model_config = ConfigDict(validate_assignment=True)
    mode: Literal["ON"]
    optional: bool
    """Whether the guiding is optional or not"""
    exposure_time: Annotated[int, NonNegativeInt, Le(120)] | None = None
    """Guiding exposure time"""
    extra_params: dict[Any, Any] = {}


class BlancoNewfirmAcquisitionConfig(BaseModel):
    model_config = ConfigDict(validate_assignment=True)
    mode: Literal["MANUAL"]
    exposure_time: Annotated[int, NonNegativeInt, Le(60)] | None = None
    """Acquisition exposure time"""
    extra_params: dict[Any, Any] = {}


class BlancoNewfirmConfig(BaseModel):
    model_config = ConfigDict(validate_assignment=True)
    exposure_count: PositiveInt
    """The number of exposures to take. This field must be set to a value greater than 0"""
    exposure_time: NonNegativeInt
    """ Exposure time in seconds"""
    mode: Literal["fowler1", "fowler2"]
    rois: list[Roi] | None = None
    extra_params: dict[Any, Any] = {}
    optical_elements: BlancoNewfirmOpticalElements


class BlancoNewfirm(BaseModel):
    model_config = ConfigDict(validate_assignment=True)
    type: Literal["EXPOSE", "SKY_FLAT", "STANDARD", "DARK"]
    instrument_type: Literal["BLANCO_NEWFIRM"] = "BLANCO_NEWFIRM"
    repeat_duration: NonNegativeInt | None = None
    extra_params: dict[Any, Any] = {}
    instrument_configs: list[BlancoNewfirmConfig] = []
    acquisition_config: BlancoNewfirmAcquisitionConfig
    guiding_config: BlancoNewfirmGuidingConfig
    target: TARGET_TYPES
    constraints: Constraints

    config_class = BlancoNewfirmConfig
    guiding_config_class = BlancoNewfirmGuidingConfig
    acquisition_config_class = BlancoNewfirmAcquisitionConfig
    optical_elements_class = BlancoNewfirmOpticalElements


# Export a type that encompasses all instruments
BLANCO_INSTRUMENTS = Union[
    BlancoNewfirm,
]