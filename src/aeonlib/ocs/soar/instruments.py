from typing import Any, Annotated, Literal, Union

from annotated_types import Le
from pydantic import BaseModel, ConfigDict
from pydantic.types import NonNegativeInt, PositiveInt

from aeonlib.models import SiderealTarget, NonSiderealTarget
from aeonlib.ocs.target_models import Constraints
from aeonlib.ocs.config_models import Roi


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
    mode: Literal["GHTS_B_400m1_2x2"]
    rotator_mode: Literal["SKY"]
    rois: list[Roi] | None = None
    extra_params: dict[Any, Any] = {}
    optical_elements: SoarGhtsBluecamOpticalElements


class SoarGhtsBluecam(BaseModel):
    model_config = ConfigDict(validate_assignment=True)
    type: Literal["SPECTRUM", "ENGINEERING", "SCRIPT", "LAMP_FLAT", "ARC"]
    instrument_type: Literal["SOAR_GHTS_BLUECAM"] = "SOAR_GHTS_BLUECAM"
    repeat_duration: NonNegativeInt | None = None
    extra_params: dict[Any, Any] = {}
    instrument_configs: list[SoarGhtsBluecamConfig] = []
    acquisition_config: SoarGhtsBluecamAcquisitionConfig
    guiding_config: SoarGhtsBluecamGuidingConfig
    target: SiderealTarget | NonSiderealTarget
    constraints: Constraints

    config_class = SoarGhtsBluecamConfig
    guiding_config_class = SoarGhtsBluecamGuidingConfig
    acquisition_config_class = SoarGhtsBluecamAcquisitionConfig
    optical_elements_class = SoarGhtsBluecamOpticalElements


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
    extra_params: dict[Any, Any] = {}
    optical_elements: SoarGhtsBluecamImagerOpticalElements


class SoarGhtsBluecamImager(BaseModel):
    model_config = ConfigDict(validate_assignment=True)
    type: Literal["EXPOSE"]
    instrument_type: Literal["SOAR_GHTS_BLUECAM_IMAGER"] = "SOAR_GHTS_BLUECAM_IMAGER"
    repeat_duration: NonNegativeInt | None = None
    extra_params: dict[Any, Any] = {}
    instrument_configs: list[SoarGhtsBluecamImagerConfig] = []
    acquisition_config: SoarGhtsBluecamImagerAcquisitionConfig
    guiding_config: SoarGhtsBluecamImagerGuidingConfig
    target: SiderealTarget | NonSiderealTarget
    constraints: Constraints

    config_class = SoarGhtsBluecamImagerConfig
    guiding_config_class = SoarGhtsBluecamImagerGuidingConfig
    acquisition_config_class = SoarGhtsBluecamImagerAcquisitionConfig
    optical_elements_class = SoarGhtsBluecamImagerOpticalElements


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
    mode: Literal["GHTS_R_1200_CaNIR_6300A_1x2_slit0p8", "GHTS_R_400m1_2x2", "GHTS_R_400m2_2x2", "GHTS_R_1200_CaNIR_1x2_slit0p8", "GHTS_R_2100_5000A_1x2_slit1p0", "GHTS_R_2100_6507A_1x2_slit0p45"]
    rotator_mode: Literal["SKY"]
    rois: list[Roi] | None = None
    extra_params: dict[Any, Any] = {}
    optical_elements: SoarGhtsRedcamOpticalElements


class SoarGhtsRedcam(BaseModel):
    model_config = ConfigDict(validate_assignment=True)
    type: Literal["SPECTRUM", "ENGINEERING", "SCRIPT", "ARC", "LAMP_FLAT"]
    instrument_type: Literal["SOAR_GHTS_REDCAM"] = "SOAR_GHTS_REDCAM"
    repeat_duration: NonNegativeInt | None = None
    extra_params: dict[Any, Any] = {}
    instrument_configs: list[SoarGhtsRedcamConfig] = []
    acquisition_config: SoarGhtsRedcamAcquisitionConfig
    guiding_config: SoarGhtsRedcamGuidingConfig
    target: SiderealTarget | NonSiderealTarget
    constraints: Constraints

    config_class = SoarGhtsRedcamConfig
    guiding_config_class = SoarGhtsRedcamGuidingConfig
    acquisition_config_class = SoarGhtsRedcamAcquisitionConfig
    optical_elements_class = SoarGhtsRedcamOpticalElements


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
    extra_params: dict[Any, Any] = {}
    optical_elements: SoarGhtsRedcamImagerOpticalElements


class SoarGhtsRedcamImager(BaseModel):
    model_config = ConfigDict(validate_assignment=True)
    type: Literal["EXPOSE"]
    instrument_type: Literal["SOAR_GHTS_REDCAM_IMAGER"] = "SOAR_GHTS_REDCAM_IMAGER"
    repeat_duration: NonNegativeInt | None = None
    extra_params: dict[Any, Any] = {}
    instrument_configs: list[SoarGhtsRedcamImagerConfig] = []
    acquisition_config: SoarGhtsRedcamImagerAcquisitionConfig
    guiding_config: SoarGhtsRedcamImagerGuidingConfig
    target: SiderealTarget | NonSiderealTarget
    constraints: Constraints

    config_class = SoarGhtsRedcamImagerConfig
    guiding_config_class = SoarGhtsRedcamImagerGuidingConfig
    acquisition_config_class = SoarGhtsRedcamImagerAcquisitionConfig
    optical_elements_class = SoarGhtsRedcamImagerOpticalElements


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
    extra_params: dict[Any, Any] = {}
    optical_elements: SoarTriplespecOpticalElements


class SoarTriplespec(BaseModel):
    model_config = ConfigDict(validate_assignment=True)
    type: Literal["SPECTRUM", "STANDARD", "ARC", "LAMP_FLAT", "BIAS"]
    instrument_type: Literal["SOAR_TRIPLESPEC"] = "SOAR_TRIPLESPEC"
    repeat_duration: NonNegativeInt | None = None
    extra_params: dict[Any, Any] = {}
    instrument_configs: list[SoarTriplespecConfig] = []
    acquisition_config: SoarTriplespecAcquisitionConfig
    guiding_config: SoarTriplespecGuidingConfig
    target: SiderealTarget | NonSiderealTarget
    constraints: Constraints

    config_class = SoarTriplespecConfig
    guiding_config_class = SoarTriplespecGuidingConfig
    acquisition_config_class = SoarTriplespecAcquisitionConfig
    optical_elements_class = SoarTriplespecOpticalElements


# Export a type that encompasses all instruments
SOAR_INSTRUMENTS = Union[
    SoarGhtsBluecam,
    SoarGhtsBluecamImager,
    SoarGhtsRedcam,
    SoarGhtsRedcamImager,
    SoarTriplespec,
]