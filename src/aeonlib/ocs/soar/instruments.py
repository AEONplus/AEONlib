# pyright:  reportUnannotatedClassAttribute=false
# This file is generated automatically and should not be edited by hand.

from typing import Any, Annotated, ClassVar, Literal

from annotated_types import Le, Ge
from pydantic import BaseModel, ConfigDict, Field
from pydantic.types import NonNegativeInt, PositiveInt

from aeonlib.models import TARGET_TYPES
from aeonlib.ocs.target_models import Constraints
from aeonlib.ocs.config_models import Roi


class SoarGhtsBluecamInstrumentConfigExtraParams(BaseModel):
    model_config = ConfigDict(validate_assignment=True, extra='allow')
    defocus: Annotated[float, Ge(-5.0), Le(5.0), "Observations may be defocused to prevent the CCD from saturating on bright targets. This term describes the offset (in mm) of the secondary mirror from its default (focused) position. The limits are ± 5mm."] | None = None


class SoarGhtsBluecamOpticalElements(BaseModel):
    model_config = ConfigDict(validate_assignment=True)


class SoarGhtsBluecamGuidingConfig(BaseModel):
    model_config = ConfigDict(validate_assignment=True)
    mode: Literal["ON"]
    optional: bool
    """Whether the guiding is optional or not"""
    exposure_time: Annotated[int, NonNegativeInt, Le(120)] | None = None
    """Guiding exposure time"""
    extra_params: dict[Any, Any] = {}


class SoarGhtsBluecamAcquisitionConfig(BaseModel):
    model_config = ConfigDict(validate_assignment=True)
    mode: Literal["MANUAL"]
    exposure_time: Annotated[int, NonNegativeInt, Le(60)] | None = None
    """Acquisition exposure time"""
    extra_params: dict[Any, Any] = {}


class SoarGhtsBluecamConfig(BaseModel):
    model_config = ConfigDict(validate_assignment=True)
    exposure_count: PositiveInt
    """The number of exposures to take. This field must be set to a value greater than 0"""
    exposure_time: NonNegativeInt
    """ Exposure time in seconds"""
    mode: Literal["GHTS_B_600UV_2x2_slit1p5", "GHTS_B_400m1_2x2", "GHTS_B_600UV_2x2_slit1p0", "GHTS_B_930m2_1x2_slit0p45"]
    rotator_mode: Literal["SKY"]
    rois: list[Roi] | None = None
    extra_params: SoarGhtsBluecamInstrumentConfigExtraParams = Field(default_factory=SoarGhtsBluecamInstrumentConfigExtraParams)
    optical_elements: SoarGhtsBluecamOpticalElements


class SoarGhtsBluecam(BaseModel):
    model_config = ConfigDict(validate_assignment=True)
    type: Literal["SPECTRUM", "ENGINEERING", "SCRIPT", "LAMP_FLAT", "ARC"]
    instrument_type: Literal["SOAR_GHTS_BLUECAM"] = "SOAR_GHTS_BLUECAM"
    repeat_duration: NonNegativeInt | None = None
    instrument_configs: list[SoarGhtsBluecamConfig] = []
    acquisition_config: SoarGhtsBluecamAcquisitionConfig
    guiding_config: SoarGhtsBluecamGuidingConfig
    target: TARGET_TYPES
    constraints: Constraints

    config_class: ClassVar = SoarGhtsBluecamConfig
    guiding_config_class: ClassVar = SoarGhtsBluecamGuidingConfig
    acquisition_config_class: ClassVar = SoarGhtsBluecamAcquisitionConfig
    optical_elements_class: ClassVar = SoarGhtsBluecamOpticalElements


class SoarGhtsBluecamImagerInstrumentConfigExtraParams(BaseModel):
    model_config = ConfigDict(validate_assignment=True, extra='allow')
    defocus: Annotated[float, Ge(-5.0), Le(5.0), "Observations may be defocused to prevent the CCD from saturating on bright targets. This term describes the offset (in mm) of the secondary mirror from its default (focused) position. The limits are ± 5mm."] | None = None


class SoarGhtsBluecamImagerOpticalElements(BaseModel):
    model_config = ConfigDict(validate_assignment=True)
    filter: Literal["u-SDSS", "g-SDSS", "r-SDSS", "i-SDSS"]


class SoarGhtsBluecamImagerGuidingConfig(BaseModel):
    model_config = ConfigDict(validate_assignment=True)
    mode: Literal["OFF", "ON"]
    optional: bool
    """Whether the guiding is optional or not"""
    exposure_time: Annotated[int, NonNegativeInt, Le(120)] | None = None
    """Guiding exposure time"""
    extra_params: dict[Any, Any] = {}


class SoarGhtsBluecamImagerAcquisitionConfig(BaseModel):
    model_config = ConfigDict(validate_assignment=True)
    mode: Literal["MANUAL"]
    exposure_time: Annotated[int, NonNegativeInt, Le(60)] | None = None
    """Acquisition exposure time"""
    extra_params: dict[Any, Any] = {}


class SoarGhtsBluecamImagerConfig(BaseModel):
    model_config = ConfigDict(validate_assignment=True)
    exposure_count: PositiveInt
    """The number of exposures to take. This field must be set to a value greater than 0"""
    exposure_time: NonNegativeInt
    """ Exposure time in seconds"""
    mode: Literal["GHTS_B_Image_2x2"]
    rotator_mode: Literal["SKY"]
    rois: list[Roi] | None = None
    extra_params: SoarGhtsBluecamImagerInstrumentConfigExtraParams = Field(default_factory=SoarGhtsBluecamImagerInstrumentConfigExtraParams)
    optical_elements: SoarGhtsBluecamImagerOpticalElements


class SoarGhtsBluecamImager(BaseModel):
    model_config = ConfigDict(validate_assignment=True)
    type: Literal["EXPOSE"]
    instrument_type: Literal["SOAR_GHTS_BLUECAM_IMAGER"] = "SOAR_GHTS_BLUECAM_IMAGER"
    repeat_duration: NonNegativeInt | None = None
    instrument_configs: list[SoarGhtsBluecamImagerConfig] = []
    acquisition_config: SoarGhtsBluecamImagerAcquisitionConfig
    guiding_config: SoarGhtsBluecamImagerGuidingConfig
    target: TARGET_TYPES
    constraints: Constraints

    config_class: ClassVar = SoarGhtsBluecamImagerConfig
    guiding_config_class: ClassVar = SoarGhtsBluecamImagerGuidingConfig
    acquisition_config_class: ClassVar = SoarGhtsBluecamImagerAcquisitionConfig
    optical_elements_class: ClassVar = SoarGhtsBluecamImagerOpticalElements


class SoarGhtsRedcamInstrumentConfigExtraParams(BaseModel):
    model_config = ConfigDict(validate_assignment=True, extra='allow')
    defocus: Annotated[float, Ge(-5.0), Le(5.0), "Observations may be defocused to prevent the CCD from saturating on bright targets. This term describes the offset (in mm) of the secondary mirror from its default (focused) position. The limits are ± 5mm."] | None = None


class SoarGhtsRedcamOpticalElements(BaseModel):
    model_config = ConfigDict(validate_assignment=True)


class SoarGhtsRedcamGuidingConfig(BaseModel):
    model_config = ConfigDict(validate_assignment=True)
    mode: Literal["ON"]
    optional: bool
    """Whether the guiding is optional or not"""
    exposure_time: Annotated[int, NonNegativeInt, Le(120)] | None = None
    """Guiding exposure time"""
    extra_params: dict[Any, Any] = {}


class SoarGhtsRedcamAcquisitionConfig(BaseModel):
    model_config = ConfigDict(validate_assignment=True)
    mode: Literal["MANUAL"]
    exposure_time: Annotated[int, NonNegativeInt, Le(60)] | None = None
    """Acquisition exposure time"""
    extra_params: dict[Any, Any] = {}


class SoarGhtsRedcamConfig(BaseModel):
    model_config = ConfigDict(validate_assignment=True)
    exposure_count: PositiveInt
    """The number of exposures to take. This field must be set to a value greater than 0"""
    exposure_time: NonNegativeInt
    """ Exposure time in seconds"""
    mode: Literal["GHTS_R_2100_5000A_1x2_slit1p0", "GHTS_R_400m1_2x2", "GHTS_R_400m2_2x2"]
    rotator_mode: Literal["SKY"]
    rois: list[Roi] | None = None
    extra_params: SoarGhtsRedcamInstrumentConfigExtraParams = Field(default_factory=SoarGhtsRedcamInstrumentConfigExtraParams)
    optical_elements: SoarGhtsRedcamOpticalElements


class SoarGhtsRedcam(BaseModel):
    model_config = ConfigDict(validate_assignment=True)
    type: Literal["SPECTRUM", "ENGINEERING", "SCRIPT", "ARC", "LAMP_FLAT"]
    instrument_type: Literal["SOAR_GHTS_REDCAM"] = "SOAR_GHTS_REDCAM"
    repeat_duration: NonNegativeInt | None = None
    instrument_configs: list[SoarGhtsRedcamConfig] = []
    acquisition_config: SoarGhtsRedcamAcquisitionConfig
    guiding_config: SoarGhtsRedcamGuidingConfig
    target: TARGET_TYPES
    constraints: Constraints

    config_class: ClassVar = SoarGhtsRedcamConfig
    guiding_config_class: ClassVar = SoarGhtsRedcamGuidingConfig
    acquisition_config_class: ClassVar = SoarGhtsRedcamAcquisitionConfig
    optical_elements_class: ClassVar = SoarGhtsRedcamOpticalElements


class SoarGhtsRedcamImagerInstrumentConfigExtraParams(BaseModel):
    model_config = ConfigDict(validate_assignment=True, extra='allow')
    defocus: Annotated[float, Ge(-5.0), Le(5.0), "Observations may be defocused to prevent the CCD from saturating on bright targets. This term describes the offset (in mm) of the secondary mirror from its default (focused) position. The limits are ± 5mm."] | None = None


class SoarGhtsRedcamImagerOpticalElements(BaseModel):
    model_config = ConfigDict(validate_assignment=True)
    filter: Literal["g-SDSS", "r-SDSS", "i-SDSS", "z-SDSS"]


class SoarGhtsRedcamImagerGuidingConfig(BaseModel):
    model_config = ConfigDict(validate_assignment=True)
    mode: Literal["OFF", "ON"]
    optional: bool
    """Whether the guiding is optional or not"""
    exposure_time: Annotated[int, NonNegativeInt, Le(120)] | None = None
    """Guiding exposure time"""
    extra_params: dict[Any, Any] = {}


class SoarGhtsRedcamImagerAcquisitionConfig(BaseModel):
    model_config = ConfigDict(validate_assignment=True)
    mode: Literal["MANUAL"]
    exposure_time: Annotated[int, NonNegativeInt, Le(60)] | None = None
    """Acquisition exposure time"""
    extra_params: dict[Any, Any] = {}


class SoarGhtsRedcamImagerConfig(BaseModel):
    model_config = ConfigDict(validate_assignment=True)
    exposure_count: PositiveInt
    """The number of exposures to take. This field must be set to a value greater than 0"""
    exposure_time: NonNegativeInt
    """ Exposure time in seconds"""
    mode: Literal["GHTS_R_Image_2x2"]
    rotator_mode: Literal["SKY"]
    rois: list[Roi] | None = None
    extra_params: SoarGhtsRedcamImagerInstrumentConfigExtraParams = Field(default_factory=SoarGhtsRedcamImagerInstrumentConfigExtraParams)
    optical_elements: SoarGhtsRedcamImagerOpticalElements


class SoarGhtsRedcamImager(BaseModel):
    model_config = ConfigDict(validate_assignment=True)
    type: Literal["EXPOSE"]
    instrument_type: Literal["SOAR_GHTS_REDCAM_IMAGER"] = "SOAR_GHTS_REDCAM_IMAGER"
    repeat_duration: NonNegativeInt | None = None
    instrument_configs: list[SoarGhtsRedcamImagerConfig] = []
    acquisition_config: SoarGhtsRedcamImagerAcquisitionConfig
    guiding_config: SoarGhtsRedcamImagerGuidingConfig
    target: TARGET_TYPES
    constraints: Constraints

    config_class: ClassVar = SoarGhtsRedcamImagerConfig
    guiding_config_class: ClassVar = SoarGhtsRedcamImagerGuidingConfig
    acquisition_config_class: ClassVar = SoarGhtsRedcamImagerAcquisitionConfig
    optical_elements_class: ClassVar = SoarGhtsRedcamImagerOpticalElements


class SoarTriplespecOpticalElements(BaseModel):
    model_config = ConfigDict(validate_assignment=True)


class SoarTriplespecGuidingConfig(BaseModel):
    model_config = ConfigDict(validate_assignment=True)
    mode: Literal["ON"]
    optional: bool
    """Whether the guiding is optional or not"""
    exposure_time: Annotated[int, NonNegativeInt, Le(120)] | None = None
    """Guiding exposure time"""
    extra_params: dict[Any, Any] = {}


class SoarTriplespecAcquisitionConfig(BaseModel):
    model_config = ConfigDict(validate_assignment=True)
    mode: Literal["MANUAL"]
    exposure_time: Annotated[int, NonNegativeInt, Le(60)] | None = None
    """Acquisition exposure time"""
    extra_params: dict[Any, Any] = {}


class SoarTriplespecConfig(BaseModel):
    model_config = ConfigDict(validate_assignment=True)
    exposure_count: PositiveInt
    """The number of exposures to take. This field must be set to a value greater than 0"""
    exposure_time: NonNegativeInt
    """ Exposure time in seconds"""
    mode: Literal["fowler1_coadds2", "fowler4_coadds1", "fowler8_coadds1", "fowler16_coadds1", "fowler1_coadds1"]
    rotator_mode: Literal["SKY"]
    rois: list[Roi] | None = None
    optical_elements: SoarTriplespecOpticalElements


class SoarTriplespec(BaseModel):
    model_config = ConfigDict(validate_assignment=True)
    type: Literal["SPECTRUM", "STANDARD", "ARC", "LAMP_FLAT", "BIAS"]
    instrument_type: Literal["SOAR_TRIPLESPEC"] = "SOAR_TRIPLESPEC"
    repeat_duration: NonNegativeInt | None = None
    instrument_configs: list[SoarTriplespecConfig] = []
    acquisition_config: SoarTriplespecAcquisitionConfig
    guiding_config: SoarTriplespecGuidingConfig
    target: TARGET_TYPES
    constraints: Constraints

    config_class: ClassVar = SoarTriplespecConfig
    guiding_config_class: ClassVar = SoarTriplespecGuidingConfig
    acquisition_config_class: ClassVar = SoarTriplespecAcquisitionConfig
    optical_elements_class: ClassVar = SoarTriplespecOpticalElements


# Export a type that encompasses all instruments
SOAR_INSTRUMENTS = SoarGhtsBluecam | SoarGhtsBluecamImager | SoarGhtsRedcam | SoarGhtsRedcamImager | SoarTriplespec