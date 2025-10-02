# pyright:  reportUnannotatedClassAttribute=false
# This file is generated automatically and should not be edited by hand.

from typing import Any, Annotated, Literal

from annotated_types import Le, Ge
from pydantic import BaseModel, ConfigDict, Field
from pydantic.types import NonNegativeInt, PositiveInt

from aeonlib.models import TARGET_TYPES
from aeonlib.ocs.target_models import Constraints
from aeonlib.ocs.config_models import Roi




class Lco0M4ScicamQhy600ConfigExtraParams(BaseModel):
    model_config = ConfigDict(validate_assignment=True, extra='allow')
    sub_expose: Annotated[bool, "Whether or not to split your exposures into sub_exposures to guide during the observation, and stack them together at the end for the final data product."] = False
    sub_exposure_time: Annotated[float, Ge(15.0), "Exposure time for the sub-exposures in seconds, if sub_expose mode is set"] | None = None


class Lco0M4ScicamQhy600InstrumentConfigExtraParams(BaseModel):
    model_config = ConfigDict(validate_assignment=True, extra='allow')
    defocus: Annotated[float, Ge(-5.0), Le(5.0), "Observations may be defocused to prevent the CCD from saturating on bright targets. This term describes the offset (in mm) of the secondary mirror from its default (focused) position. The limits are ± 5mm."] | None = None


class Lco0M4ScicamQhy600OpticalElements(BaseModel):
    model_config = ConfigDict(validate_assignment=True)
    filter: Literal["OIII", "SII", "Astrodon-Exo", "w", "opaque", "up", "rp", "ip", "gp", "zs", "V", "B", "H-Alpha"]


class Lco0M4ScicamQhy600GuidingConfig(BaseModel):
    model_config = ConfigDict(validate_assignment=True)
    mode: Literal["OFF", "ON"]
    optional: bool
    """Whether the guiding is optional or not"""
    exposure_time: Annotated[int, NonNegativeInt, Le(120)] | None = None
    """Guiding exposure time"""
    extra_params: dict[Any, Any] = {}


class Lco0M4ScicamQhy600AcquisitionConfig(BaseModel):
    model_config = ConfigDict(validate_assignment=True)
    mode: Literal["OFF"]
    exposure_time: Annotated[int, NonNegativeInt, Le(60)] | None = None
    """Acquisition exposure time"""
    extra_params: dict[Any, Any] = {}


class Lco0M4ScicamQhy600Config(BaseModel):
    model_config = ConfigDict(validate_assignment=True)
    exposure_count: PositiveInt
    """The number of exposures to take. This field must be set to a value greater than 0"""
    exposure_time: NonNegativeInt
    """ Exposure time in seconds"""
    mode: Literal["central30x30", "full_frame"]
    rois: list[Roi] | None = None
    extra_params: Lco0M4ScicamQhy600InstrumentConfigExtraParams = Field(default_factory=Lco0M4ScicamQhy600InstrumentConfigExtraParams)
    optical_elements: Lco0M4ScicamQhy600OpticalElements


class Lco0M4ScicamQhy600(BaseModel):
    model_config = ConfigDict(validate_assignment=True)
    type: Literal["EXPOSE", "REPEAT_EXPOSE", "AUTO_FOCUS", "BIAS", "DARK", "STANDARD", "SKY_FLAT"]
    instrument_type: Literal["0M4-SCICAM-QHY600"] = "0M4-SCICAM-QHY600"
    repeat_duration: NonNegativeInt | None = None
    extra_params: Lco0M4ScicamQhy600ConfigExtraParams = Field(default_factory=Lco0M4ScicamQhy600ConfigExtraParams)
    instrument_configs: list[Lco0M4ScicamQhy600Config] = []
    acquisition_config: Lco0M4ScicamQhy600AcquisitionConfig
    guiding_config: Lco0M4ScicamQhy600GuidingConfig
    target: TARGET_TYPES
    constraints: Constraints

    config_class = Lco0M4ScicamQhy600Config
    guiding_config_class = Lco0M4ScicamQhy600GuidingConfig
    acquisition_config_class = Lco0M4ScicamQhy600AcquisitionConfig
    optical_elements_class = Lco0M4ScicamQhy600OpticalElements




class Lco1M0NresScicamConfigExtraParams(BaseModel):
    model_config = ConfigDict(validate_assignment=True, extra='allow')


class Lco1M0NresScicamInstrumentConfigExtraParams(BaseModel):
    model_config = ConfigDict(validate_assignment=True, extra='allow')
    defocus: Annotated[float, Ge(-5.0), Le(5.0), "Observations may be defocused to prevent the CCD from saturating on bright targets. This term describes the offset (in mm) of the secondary mirror from its default (focused) position. The limits are ± 5mm."] | None = None


class Lco1M0NresScicamOpticalElements(BaseModel):
    model_config = ConfigDict(validate_assignment=True)


class Lco1M0NresScicamGuidingConfig(BaseModel):
    model_config = ConfigDict(validate_assignment=True)
    mode: Literal["ON"]
    optional: bool
    """Whether the guiding is optional or not"""
    exposure_time: Annotated[int, NonNegativeInt, Le(120)] | None = None
    """Guiding exposure time"""
    extra_params: dict[Any, Any] = {}


class Lco1M0NresScicamAcquisitionConfig(BaseModel):
    model_config = ConfigDict(validate_assignment=True)
    mode: Literal["WCS", "BRIGHTEST"]
    exposure_time: Annotated[int, NonNegativeInt, Le(60)] | None = None
    """Acquisition exposure time"""
    extra_params: dict[Any, Any] = {}


class Lco1M0NresScicamConfig(BaseModel):
    model_config = ConfigDict(validate_assignment=True)
    exposure_count: PositiveInt
    """The number of exposures to take. This field must be set to a value greater than 0"""
    exposure_time: NonNegativeInt
    """ Exposure time in seconds"""
    mode: Literal["default"]
    rois: list[Roi] | None = None
    extra_params: Lco1M0NresScicamInstrumentConfigExtraParams = Field(default_factory=Lco1M0NresScicamInstrumentConfigExtraParams)
    optical_elements: Lco1M0NresScicamOpticalElements


class Lco1M0NresScicam(BaseModel):
    model_config = ConfigDict(validate_assignment=True)
    type: Literal["NRES_SPECTRUM", "REPEAT_NRES_SPECTRUM", "NRES_EXPOSE", "NRES_TEST", "SCRIPT", "ENGINEERING", "ARC", "LAMP_FLAT", "NRES_BIAS", "NRES_DARK", "AUTO_FOCUS"]
    instrument_type: Literal["1M0-NRES-SCICAM"] = "1M0-NRES-SCICAM"
    repeat_duration: NonNegativeInt | None = None
    extra_params: Lco1M0NresScicamConfigExtraParams = Field(default_factory=Lco1M0NresScicamConfigExtraParams)
    instrument_configs: list[Lco1M0NresScicamConfig] = []
    acquisition_config: Lco1M0NresScicamAcquisitionConfig
    guiding_config: Lco1M0NresScicamGuidingConfig
    target: TARGET_TYPES
    constraints: Constraints

    config_class = Lco1M0NresScicamConfig
    guiding_config_class = Lco1M0NresScicamGuidingConfig
    acquisition_config_class = Lco1M0NresScicamAcquisitionConfig
    optical_elements_class = Lco1M0NresScicamOpticalElements




class Lco1M0ScicamSinistroConfigExtraParams(BaseModel):
    model_config = ConfigDict(validate_assignment=True, extra='allow')


class Lco1M0ScicamSinistroInstrumentConfigExtraParams(BaseModel):
    model_config = ConfigDict(validate_assignment=True, extra='allow')
    defocus: Annotated[float, Ge(-5.0), Le(5.0), "Observations may be defocused to prevent the CCD from saturating on bright targets. This term describes the offset (in mm) of the secondary mirror from its default (focused) position. The limits are ± 5mm."] | None = None


class Lco1M0ScicamSinistroOpticalElements(BaseModel):
    model_config = ConfigDict(validate_assignment=True)
    filter: Literal["I", "R", "U", "w", "Y", "up", "rp", "ip", "gp", "zs", "V", "B", "400um-Pinhole", "150um-Pinhole", "CN"]


class Lco1M0ScicamSinistroGuidingConfig(BaseModel):
    model_config = ConfigDict(validate_assignment=True)
    mode: Literal["OFF", "ON"]
    optional: bool
    """Whether the guiding is optional or not"""
    exposure_time: Annotated[int, NonNegativeInt, Le(120)] | None = None
    """Guiding exposure time"""
    extra_params: dict[Any, Any] = {}


class Lco1M0ScicamSinistroAcquisitionConfig(BaseModel):
    model_config = ConfigDict(validate_assignment=True)
    mode: Literal["OFF"]
    exposure_time: Annotated[int, NonNegativeInt, Le(60)] | None = None
    """Acquisition exposure time"""
    extra_params: dict[Any, Any] = {}


class Lco1M0ScicamSinistroConfig(BaseModel):
    model_config = ConfigDict(validate_assignment=True)
    exposure_count: PositiveInt
    """The number of exposures to take. This field must be set to a value greater than 0"""
    exposure_time: NonNegativeInt
    """ Exposure time in seconds"""
    mode: Literal["full_frame", "central_2k_2x2"]
    rois: list[Roi] | None = None
    extra_params: Lco1M0ScicamSinistroInstrumentConfigExtraParams = Field(default_factory=Lco1M0ScicamSinistroInstrumentConfigExtraParams)
    optical_elements: Lco1M0ScicamSinistroOpticalElements


class Lco1M0ScicamSinistro(BaseModel):
    model_config = ConfigDict(validate_assignment=True)
    type: Literal["EXPOSE", "REPEAT_EXPOSE", "BIAS", "DARK", "STANDARD", "SCRIPT", "AUTO_FOCUS", "ENGINEERING", "SKY_FLAT"]
    instrument_type: Literal["1M0-SCICAM-SINISTRO"] = "1M0-SCICAM-SINISTRO"
    repeat_duration: NonNegativeInt | None = None
    extra_params: Lco1M0ScicamSinistroConfigExtraParams = Field(default_factory=Lco1M0ScicamSinistroConfigExtraParams)
    instrument_configs: list[Lco1M0ScicamSinistroConfig] = []
    acquisition_config: Lco1M0ScicamSinistroAcquisitionConfig
    guiding_config: Lco1M0ScicamSinistroGuidingConfig
    target: TARGET_TYPES
    constraints: Constraints

    config_class = Lco1M0ScicamSinistroConfig
    guiding_config_class = Lco1M0ScicamSinistroGuidingConfig
    acquisition_config_class = Lco1M0ScicamSinistroAcquisitionConfig
    optical_elements_class = Lco1M0ScicamSinistroOpticalElements




class Lco2M0FloydsScicamConfigExtraParams(BaseModel):
    model_config = ConfigDict(validate_assignment=True, extra='allow')


class Lco2M0FloydsScicamInstrumentConfigExtraParams(BaseModel):
    model_config = ConfigDict(validate_assignment=True, extra='allow')
    defocus: Annotated[float, Ge(-5.0), Le(5.0), ""] | None = None


class Lco2M0FloydsScicamOpticalElements(BaseModel):
    model_config = ConfigDict(validate_assignment=True)
    slit: Literal["slit_6.0as", "slit_1.6as", "slit_2.0as", "slit_1.2as"]


class Lco2M0FloydsScicamGuidingConfig(BaseModel):
    model_config = ConfigDict(validate_assignment=True)
    mode: Literal["OFF", "ON"]
    optional: bool
    """Whether the guiding is optional or not"""
    exposure_time: Annotated[int, NonNegativeInt, Le(120)] | None = None
    """Guiding exposure time"""
    extra_params: dict[Any, Any] = {}


class Lco2M0FloydsScicamAcquisitionConfig(BaseModel):
    model_config = ConfigDict(validate_assignment=True)
    mode: Literal["BRIGHTEST", "WCS"]
    exposure_time: Annotated[int, NonNegativeInt, Le(60)] | None = None
    """Acquisition exposure time"""
    extra_params: dict[Any, Any] = {}


class Lco2M0FloydsScicamConfig(BaseModel):
    model_config = ConfigDict(validate_assignment=True)
    exposure_count: PositiveInt
    """The number of exposures to take. This field must be set to a value greater than 0"""
    exposure_time: NonNegativeInt
    """ Exposure time in seconds"""
    mode: Literal["default"]
    rotator_mode: Literal["VFLOAT", "SKY"]
    rois: list[Roi] | None = None
    extra_params: Lco2M0FloydsScicamInstrumentConfigExtraParams = Field(default_factory=Lco2M0FloydsScicamInstrumentConfigExtraParams)
    optical_elements: Lco2M0FloydsScicamOpticalElements


class Lco2M0FloydsScicam(BaseModel):
    model_config = ConfigDict(validate_assignment=True)
    type: Literal["SPECTRUM", "REPEAT_SPECTRUM", "ARC", "ENGINEERING", "SCRIPT", "LAMP_FLAT"]
    instrument_type: Literal["2M0-FLOYDS-SCICAM"] = "2M0-FLOYDS-SCICAM"
    repeat_duration: NonNegativeInt | None = None
    extra_params: Lco2M0FloydsScicamConfigExtraParams = Field(default_factory=Lco2M0FloydsScicamConfigExtraParams)
    instrument_configs: list[Lco2M0FloydsScicamConfig] = []
    acquisition_config: Lco2M0FloydsScicamAcquisitionConfig
    guiding_config: Lco2M0FloydsScicamGuidingConfig
    target: TARGET_TYPES
    constraints: Constraints

    config_class = Lco2M0FloydsScicamConfig
    guiding_config_class = Lco2M0FloydsScicamGuidingConfig
    acquisition_config_class = Lco2M0FloydsScicamAcquisitionConfig
    optical_elements_class = Lco2M0FloydsScicamOpticalElements




class Lco2M0ScicamMuscatConfigExtraParams(BaseModel):
    model_config = ConfigDict(validate_assignment=True, extra='allow')


class Lco2M0ScicamMuscatInstrumentConfigExtraParams(BaseModel):
    model_config = ConfigDict(validate_assignment=True, extra='allow')
    defocus: Annotated[float, Ge(-8.0), Le(8.0), "Observations may be defocused to prevent the CCD from saturating on bright targets. This term describes the offset (in mm) of the secondary mirror from its default (focused) position. The limits are ± 8mm."] | None = None


class Lco2M0ScicamMuscatOpticalElements(BaseModel):
    model_config = ConfigDict(validate_assignment=True)
    narrowband_g_position: Literal["out", "in"]
    narrowband_r_position: Literal["out", "in"]
    narrowband_i_position: Literal["out", "in"]
    narrowband_z_position: Literal["out", "in"]


class Lco2M0ScicamMuscatGuidingConfig(BaseModel):
    model_config = ConfigDict(validate_assignment=True)
    mode: Literal["ON", "OFF"]
    optional: bool
    """Whether the guiding is optional or not"""
    exposure_time: Annotated[int, NonNegativeInt, Le(120)] | None = None
    """Guiding exposure time"""
    extra_params: dict[Any, Any] = {}


class Lco2M0ScicamMuscatAcquisitionConfig(BaseModel):
    model_config = ConfigDict(validate_assignment=True)
    mode: Literal["OFF"]
    exposure_time: Annotated[int, NonNegativeInt, Le(60)] | None = None
    """Acquisition exposure time"""
    extra_params: dict[Any, Any] = {}


class Lco2M0ScicamMuscatConfig(BaseModel):
    model_config = ConfigDict(validate_assignment=True)
    exposure_count: PositiveInt
    """The number of exposures to take. This field must be set to a value greater than 0"""
    exposure_time: NonNegativeInt
    """ Exposure time in seconds"""
    mode: Literal["MUSCAT_SLOW", "MUSCAT_FAST"]
    rois: list[Roi] | None = None
    extra_params: Lco2M0ScicamMuscatInstrumentConfigExtraParams = Field(default_factory=Lco2M0ScicamMuscatInstrumentConfigExtraParams)
    optical_elements: Lco2M0ScicamMuscatOpticalElements


class Lco2M0ScicamMuscat(BaseModel):
    model_config = ConfigDict(validate_assignment=True)
    type: Literal["EXPOSE", "REPEAT_EXPOSE", "BIAS", "DARK", "STANDARD", "SCRIPT", "AUTO_FOCUS", "ENGINEERING", "SKY_FLAT"]
    instrument_type: Literal["2M0-SCICAM-MUSCAT"] = "2M0-SCICAM-MUSCAT"
    repeat_duration: NonNegativeInt | None = None
    extra_params: Lco2M0ScicamMuscatConfigExtraParams = Field(default_factory=Lco2M0ScicamMuscatConfigExtraParams)
    instrument_configs: list[Lco2M0ScicamMuscatConfig] = []
    acquisition_config: Lco2M0ScicamMuscatAcquisitionConfig
    guiding_config: Lco2M0ScicamMuscatGuidingConfig
    target: TARGET_TYPES
    constraints: Constraints

    config_class = Lco2M0ScicamMuscatConfig
    guiding_config_class = Lco2M0ScicamMuscatGuidingConfig
    acquisition_config_class = Lco2M0ScicamMuscatAcquisitionConfig
    optical_elements_class = Lco2M0ScicamMuscatOpticalElements


# Export a type that encompasses all instruments
LCO_INSTRUMENTS = Lco0M4ScicamQhy600 | Lco1M0NresScicam | Lco1M0ScicamSinistro | Lco2M0FloydsScicam | Lco2M0ScicamMuscat