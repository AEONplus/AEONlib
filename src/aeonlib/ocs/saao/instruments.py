from typing import Annotated, Any, Literal, Union

from annotated_types import Le
from pydantic import BaseModel, ConfigDict
from pydantic.types import NonNegativeInt, PositiveInt

from aeonlib.models import TARGET_TYPES
from aeonlib.ocs.config_models import Roi
from aeonlib.ocs.target_models import Constraints


class SAAO1M0AMookodiImgOpticalElements(BaseModel):
    model_config = ConfigDict(validate_assignment=True)
    filter: Literal["z'", "u'", "g'", "r'", "i'", "out"]
    obfilter: Literal["out", "Clear", "OrdBlck_Fltr"]
    slit: Literal["out", "mk-wide", "mk-narrow"]
    grism: Literal["out", "in"]


class SAAO1M0AMookodiImgGuidingConfig(BaseModel):
    model_config = ConfigDict(validate_assignment=True)
    mode: Literal["GUIDE OFF", "GUIDE ON"]
    optional: bool
    """Whether the guiding is optional or not"""
    exposure_time: Annotated[int, NonNegativeInt, Le(120)] | None = None
    """Guiding exposure time"""
    extra_params: dict[Any, Any] = {}


class SAAO1M0AMookodiImgAcquisitionConfig(BaseModel):
    model_config = ConfigDict(validate_assignment=True)
    mode: Literal["AcN:OFF&Acq:OFF", "AcN:OFF&Acq:ON", "AcN:ON&Acq:ON"]
    exposure_time: Annotated[int, NonNegativeInt, Le(60)] | None = None
    """Acquisition exposure time"""
    extra_params: dict[Any, Any] = {}


class SAAO1M0AMookodiImgConfig(BaseModel):
    model_config = ConfigDict(validate_assignment=True)
    exposure_count: PositiveInt
    """The number of exposures to take. This field must be set to a value greater than 0"""
    exposure_time: NonNegativeInt
    """ Exposure time in seconds"""
    mode: Literal[
        "1x1HighFastOpen", "1x1HighSlowAuto", "1x1HighFastAuto", "2x2HighFastOpen"
    ]
    rois: list[Roi] | None = None
    extra_params: dict[Any, Any] = {}
    optical_elements: SAAO1M0AMookodiImgOpticalElements


class SAAO1M0AMookodiImg(BaseModel):
    model_config = ConfigDict(validate_assignment=True)
    type: Literal["DARK", "BIAS", "REPEAT_EXPOSE", "EXPOSE", "STANDARD"]
    instrument_type: Literal["1M0A_MOOKODI-IMG"] = "1M0A_MOOKODI-IMG"
    repeat_duration: NonNegativeInt | None = None
    extra_params: dict[Any, Any] = {}
    instrument_configs: list[SAAO1M0AMookodiImgConfig] = []
    acquisition_config: SAAO1M0AMookodiImgAcquisitionConfig
    guiding_config: SAAO1M0AMookodiImgGuidingConfig
    target: TARGET_TYPES
    constraints: Constraints

    config_class = SAAO1M0AMookodiImgConfig
    guiding_config_class = SAAO1M0AMookodiImgGuidingConfig
    acquisition_config_class = SAAO1M0AMookodiImgAcquisitionConfig
    optical_elements_class = SAAO1M0AMookodiImgOpticalElements


class SAAO1M0AMookodiSpecOpticalElements(BaseModel):
    model_config = ConfigDict(validate_assignment=True)
    filter: Literal["z'", "u'", "g'", "r'", "i'", "out"]
    obfilter: Literal["out", "Clear", "OrdBlck_Fltr"]
    slit: Literal["out", "mk-wide", "mk-narrow"]
    grism: Literal["out", "in"]


class SAAO1M0AMookodiSpecGuidingConfig(BaseModel):
    model_config = ConfigDict(validate_assignment=True)
    mode: Literal["GUIDE OFF", "GUIDE ON"]
    optional: bool
    """Whether the guiding is optional or not"""
    exposure_time: Annotated[int, NonNegativeInt, Le(120)] | None = None
    """Guiding exposure time"""
    extra_params: dict[Any, Any] = {}


class SAAO1M0AMookodiSpecAcquisitionConfig(BaseModel):
    model_config = ConfigDict(validate_assignment=True)
    mode: Literal["AcN:OFF&Acq:OFF", "AcN:OFF&Acq:ON", "AcN:ON&Acq:ON"]
    exposure_time: Annotated[int, NonNegativeInt, Le(60)] | None = None
    """Acquisition exposure time"""
    extra_params: dict[Any, Any] = {}


class SAAO1M0AMookodiSpecConfig(BaseModel):
    model_config = ConfigDict(validate_assignment=True)
    exposure_count: PositiveInt
    """The number of exposures to take. This field must be set to a value greater than 0"""
    exposure_time: NonNegativeInt
    """ Exposure time in seconds"""
    mode: Literal["1x1HighSlowAuto", "1x1HighFastAuto", "1x1HighFastOpen"]
    rois: list[Roi] | None = None
    extra_params: dict[Any, Any] = {}
    optical_elements: SAAO1M0AMookodiSpecOpticalElements


class SAAO1M0AMookodiSpec(BaseModel):
    model_config = ConfigDict(validate_assignment=True)
    type: Literal["STANDARD", "EXPOSE", "BIAS", "ARC_LAMP", "SKY_FLAT"]
    instrument_type: Literal["1M0A_MOOKODI_SPEC"] = "1M0A_MOOKODI_SPEC"
    repeat_duration: NonNegativeInt | None = None
    extra_params: dict[Any, Any] = {}
    instrument_configs: list[SAAO1M0AMookodiSpecConfig] = []
    acquisition_config: SAAO1M0AMookodiSpecAcquisitionConfig
    guiding_config: SAAO1M0AMookodiSpecGuidingConfig
    target: TARGET_TYPES
    constraints: Constraints

    config_class = SAAO1M0AMookodiSpecConfig
    guiding_config_class = SAAO1M0AMookodiSpecGuidingConfig
    acquisition_config_class = SAAO1M0AMookodiSpecAcquisitionConfig
    optical_elements_class = SAAO1M0AMookodiSpecOpticalElements


class SAAO1M9AShocnwonderImgOpticalElements(BaseModel):
    model_config = ConfigDict(validate_assignment=True)
    Binning: Literal["1x1", "2x2", "4x4", "8x8", "16x16"]
    Gain: Literal["gain1.0", "gain2.0"]
    Triggering: Literal["trig_int", "trig_ext", "trig_ext_s"]
    Cube: Literal["true", "false"]
    Subframe: Literal["512x512", "256x256", "128x128", "64x64", "full_frame"]
    filter: Literal["out", "U", "B", "V", "R", "I", "u'", "g'", "r'", "i'", "z'"]


class SAAO1M9AShocnwonderImgGuidingConfig(BaseModel):
    model_config = ConfigDict(validate_assignment=True)
    mode: Literal["GUIDE OFF", "GUIDE ON"]
    optional: bool
    """Whether the guiding is optional or not"""
    exposure_time: Annotated[int, NonNegativeInt, Le(120)] | None = None
    """Guiding exposure time"""
    extra_params: dict[Any, Any] = {}


class SAAO1M9AShocnwonderImgAcquisitionConfig(BaseModel):
    model_config = ConfigDict(validate_assignment=True)
    mode: Literal["AcN:OFF&Acq:OFF", "AcN:OFF&Acq:ON", "AcN:ON&Acq:ON"]
    exposure_time: Annotated[int, NonNegativeInt, Le(60)] | None = None
    """Acquisition exposure time"""
    extra_params: dict[Any, Any] = {}


class SAAO1M9AShocnwonderImgConfig(BaseModel):
    model_config = ConfigDict(validate_assignment=True)
    exposure_count: PositiveInt
    """The number of exposures to take. This field must be set to a value greater than 0"""
    exposure_time: NonNegativeInt
    """ Exposure time in seconds"""
    mode: Literal["0.1MHz", "1MHz"]
    rois: list[Roi] | None = None
    extra_params: dict[Any, Any] = {}
    optical_elements: SAAO1M9AShocnwonderImgOpticalElements


class SAAO1M9AShocnwonderImg(BaseModel):
    model_config = ConfigDict(validate_assignment=True)
    type: Literal["EXPOSE"]
    instrument_type: Literal["1M9A_SHOCNWONDER-IMG"] = "1M9A_SHOCNWONDER-IMG"
    repeat_duration: NonNegativeInt | None = None
    extra_params: dict[Any, Any] = {}
    instrument_configs: list[SAAO1M9AShocnwonderImgConfig] = []
    acquisition_config: SAAO1M9AShocnwonderImgAcquisitionConfig
    guiding_config: SAAO1M9AShocnwonderImgGuidingConfig
    target: TARGET_TYPES
    constraints: Constraints

    config_class = SAAO1M9AShocnwonderImgConfig
    guiding_config_class = SAAO1M9AShocnwonderImgGuidingConfig
    acquisition_config_class = SAAO1M9AShocnwonderImgAcquisitionConfig
    optical_elements_class = SAAO1M9AShocnwonderImgOpticalElements


class SAAO1M9ASpupnicSpecOpticalElements(BaseModel):
    model_config = ConfigDict(validate_assignment=True)
    obfilter: Literal["out", "Clear", "OrdBlck_Fltr"]
    slit: Literal["out", "mk-wide", "mk-narrow"]
    spup_grating: Literal[
        "spup_gr4",
        "spup_gr5",
        "spup_gr6",
        "spup_gr7",
        "spup_gr8",
        "spup_gr9",
        "spup_gr10",
        "spup_gr11",
        "spup_gr12",
        "spup_gr13",
    ]
    spup_slit: Literal["spupslit_w10.5", "spupslit_w18.5", "spupslit_w12.5"]


class SAAO1M9ASpupnicSpecGuidingConfig(BaseModel):
    model_config = ConfigDict(validate_assignment=True)
    mode: Literal["GUIDE OFF", "GUIDE ON"]
    optional: bool
    """Whether the guiding is optional or not"""
    exposure_time: Annotated[int, NonNegativeInt, Le(120)] | None = None
    """Guiding exposure time"""
    extra_params: dict[Any, Any] = {}


class SAAO1M9ASpupnicSpecAcquisitionConfig(BaseModel):
    model_config = ConfigDict(validate_assignment=True)
    mode: Literal["AcN:OFF&Acq:OFF", "AcN:OFF&Acq:ON", "AcN:ON&Acq:ON"]
    exposure_time: Annotated[int, NonNegativeInt, Le(60)] | None = None
    """Acquisition exposure time"""
    extra_params: dict[Any, Any] = {}


class SAAO1M9ASpupnicSpecConfig(BaseModel):
    model_config = ConfigDict(validate_assignment=True)
    exposure_count: PositiveInt
    """The number of exposures to take. This field must be set to a value greater than 0"""
    exposure_time: NonNegativeInt
    """ Exposure time in seconds"""
    mode: Literal["1x1HighFastOpen", "1x1HighSlowAuto", "1x1HighFastAuto"]
    rois: list[Roi] | None = None
    extra_params: dict[Any, Any] = {}
    optical_elements: SAAO1M9ASpupnicSpecOpticalElements


class SAAO1M9ASpupnicSpec(BaseModel):
    model_config = ConfigDict(validate_assignment=True)
    type: Literal["EXPOSE", "LAMP_FLAT", "ARC_LAMP", "BIAS", "STANDARD"]
    instrument_type: Literal["1M9A_SPUPNIC-SPEC"] = "1M9A_SPUPNIC-SPEC"
    repeat_duration: NonNegativeInt | None = None
    extra_params: dict[Any, Any] = {}
    instrument_configs: list[SAAO1M9ASpupnicSpecConfig] = []
    acquisition_config: SAAO1M9ASpupnicSpecAcquisitionConfig
    guiding_config: SAAO1M9ASpupnicSpecGuidingConfig
    target: TARGET_TYPES
    constraints: Constraints

    config_class = SAAO1M9ASpupnicSpecConfig
    guiding_config_class = SAAO1M9ASpupnicSpecGuidingConfig
    acquisition_config_class = SAAO1M9ASpupnicSpecAcquisitionConfig
    optical_elements_class = SAAO1M9ASpupnicSpecOpticalElements


class SAAOSiboniseImgOpticalElements(BaseModel):
    model_config = ConfigDict(validate_assignment=True)
    filter: Literal[
        "out",
        "U",
        "B",
        "V",
        "R",
        "I",
        "Clear",
        "O2p8nm",
        "Halpha3p2nm",
        "Halpha4p0nm",
        "HeII4p0nm",
    ]
    Bin: Literal["1x1", "2x2", "3x3", "4x4", "5x5", "6x6"]
    Gain: Literal["bright_gain", "faint_gain"]


class SAAOSiboniseImgGuidingConfig(BaseModel):
    model_config = ConfigDict(validate_assignment=True)
    mode: Literal["GUIDE OFF", "GUIDE ON"]
    optional: bool
    """Whether the guiding is optional or not"""
    exposure_time: Annotated[int, NonNegativeInt, Le(120)] | None = None
    """Guiding exposure time"""
    extra_params: dict[Any, Any] = {}


class SAAOSiboniseImgAcquisitionConfig(BaseModel):
    model_config = ConfigDict(validate_assignment=True)
    mode: Literal["AcN:OFF&Acq:OFF", "AcN:OFF&Acq:ON", "AcN:ON&Acq:ON"]
    exposure_time: Annotated[int, NonNegativeInt, Le(60)] | None = None
    """Acquisition exposure time"""
    extra_params: dict[Any, Any] = {}


class SAAOSiboniseImgConfig(BaseModel):
    model_config = ConfigDict(validate_assignment=True)
    exposure_count: PositiveInt
    """The number of exposures to take. This field must be set to a value greater than 0"""
    exposure_time: NonNegativeInt
    """ Exposure time in seconds"""
    mode: Literal["fast", "slow"]
    rois: list[Roi] | None = None
    extra_params: dict[Any, Any] = {}
    optical_elements: SAAOSiboniseImgOpticalElements


class SAAOSiboniseImg(BaseModel):
    model_config = ConfigDict(validate_assignment=True)
    type: Literal["EXPOSE", "REPEAT_EXPOSE"]
    instrument_type: Literal["SIBONISE_IMG"] = "SIBONISE_IMG"
    repeat_duration: NonNegativeInt | None = None
    extra_params: dict[Any, Any] = {}
    instrument_configs: list[SAAOSiboniseImgConfig] = []
    acquisition_config: SAAOSiboniseImgAcquisitionConfig
    guiding_config: SAAOSiboniseImgGuidingConfig
    target: TARGET_TYPES
    constraints: Constraints

    config_class = SAAOSiboniseImgConfig
    guiding_config_class = SAAOSiboniseImgGuidingConfig
    acquisition_config_class = SAAOSiboniseImgAcquisitionConfig
    optical_elements_class = SAAOSiboniseImgOpticalElements


# Export a type that encompasses all instruments
SAAO_INSTRUMENTS = Union[
    SAAO1M0AMookodiImg,
    SAAO1M0AMookodiSpec,
    SAAO1M9AShocnwonderImg,
    SAAO1M9ASpupnicSpec,
    SAAOSiboniseImg,
]
