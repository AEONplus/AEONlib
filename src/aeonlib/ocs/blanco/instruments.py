# pyright:  reportUnannotatedClassAttribute=false
# This file is generated automatically and should not be edited by hand.

from typing import Any, Annotated, Literal

from annotated_types import Le, Ge
from pydantic import BaseModel, ConfigDict, Field
from pydantic.types import NonNegativeInt, PositiveInt

from aeonlib.models import TARGET_TYPES
from aeonlib.ocs.target_models import Constraints
from aeonlib.ocs.config_models import Roi




class BlancoNewfirmConfigExtraParams(BaseModel):
    model_config = ConfigDict(validate_assignment=True, extra='allow')
    dither_value: Annotated[int, Ge(0), Le(1600), "The amount in arc seconds between dither points"] = 80
    dither_sequence: Literal["2x2", "3x3", "4x4", "5-point"] = "2x2"
    detector_centering: Literal["none", "det_1", "det_2", "det_3", "det_4"] = "det_1"
    dither_sequence_random_offset: Annotated[bool, "Implements a random offset between dither patterns if repeating the dither pattern, i.e. when sequence repeats > 1"] = True


class BlancoNewfirmInstrumentConfigExtraParams(BaseModel):
    model_config = ConfigDict(validate_assignment=True, extra='allow')
    coadds: Annotated[int, Ge(1), Le(100), "This reduces data volume with short integration times necessary for broadband H and Ks observations. Coadding is digital summation of the images to avoid long integrations that could cause saturation of the detector."] = 1
    sequence_repeats: Annotated[int, Ge(1), Le(500), "The number of times to repeat the dither sequence"] = 1


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
    extra_params: BlancoNewfirmInstrumentConfigExtraParams = Field(default_factory=BlancoNewfirmInstrumentConfigExtraParams)
    optical_elements: BlancoNewfirmOpticalElements


class BlancoNewfirm(BaseModel):
    model_config = ConfigDict(validate_assignment=True)
    type: Literal["EXPOSE", "SKY_FLAT", "STANDARD", "DARK"]
    instrument_type: Literal["BLANCO_NEWFIRM"] = "BLANCO_NEWFIRM"
    repeat_duration: NonNegativeInt | None = None
    extra_params: BlancoNewfirmConfigExtraParams = Field(default_factory=BlancoNewfirmConfigExtraParams)
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
BLANCO_INSTRUMENTS = BlancoNewfirm