from typing import Any, Annotated, Literal, Union

from annotated_types import Le
from pydantic import BaseModel, ConfigDict
from pydantic.types import NonNegativeInt, PositiveInt

from aeonlib.models import SiderealTarget, NonSiderealTarget
from aeonlib.ocs.target_models import Constraints
from aeonlib.ocs.config_models import Roi


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
    extra_params: dict[Any, Any] = {}
    optical_elements: Lco0M4ScicamQhy600OpticalElements


class Lco0M4ScicamQhy600(BaseModel):
    model_config = ConfigDict(validate_assignment=True)
    type: Literal["EXPOSE", "REPEAT_EXPOSE", "AUTO_FOCUS", "BIAS", "DARK", "STANDARD", "SKY_FLAT"]
    instrument_type: Literal["0M4-SCICAM-QHY600"] = "0M4-SCICAM-QHY600"
    repeat_duration: NonNegativeInt | None = None
    extra_params: dict[Any, Any] = {}
    instrument_configs: list[Lco0M4ScicamQhy600Config] = []
    acquisition_config: Lco0M4ScicamQhy600AcquisitionConfig
    guiding_config: Lco0M4ScicamQhy600GuidingConfig
    target: SiderealTarget | NonSiderealTarget
    constraints: Constraints

    config_class = Lco0M4ScicamQhy600Config
    guiding_config_class = Lco0M4ScicamQhy600GuidingConfig
    acquisition_config_class = Lco0M4ScicamQhy600AcquisitionConfig
    optical_elements_class = Lco0M4ScicamQhy600OpticalElements


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
    extra_params: dict[Any, Any] = {}
    optical_elements: Lco1M0NresScicamOpticalElements


class Lco1M0NresScicam(BaseModel):
    model_config = ConfigDict(validate_assignment=True)
    type: Literal["NRES_SPECTRUM", "REPEAT_NRES_SPECTRUM", "NRES_EXPOSE", "NRES_TEST", "SCRIPT", "ENGINEERING", "ARC", "LAMP_FLAT", "NRES_BIAS", "NRES_DARK", "AUTO_FOCUS"]
    instrument_type: Literal["1M0-NRES-SCICAM"] = "1M0-NRES-SCICAM"
    repeat_duration: NonNegativeInt | None = None
    extra_params: dict[Any, Any] = {}
    instrument_configs: list[Lco1M0NresScicamConfig] = []
    acquisition_config: Lco1M0NresScicamAcquisitionConfig
    guiding_config: Lco1M0NresScicamGuidingConfig
    target: SiderealTarget | NonSiderealTarget
    constraints: Constraints

    config_class = Lco1M0NresScicamConfig
    guiding_config_class = Lco1M0NresScicamGuidingConfig
    acquisition_config_class = Lco1M0NresScicamAcquisitionConfig
    optical_elements_class = Lco1M0NresScicamOpticalElements


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
    extra_params: dict[Any, Any] = {}
    optical_elements: Lco1M0ScicamSinistroOpticalElements


class Lco1M0ScicamSinistro(BaseModel):
    model_config = ConfigDict(validate_assignment=True)
    type: Literal["EXPOSE", "REPEAT_EXPOSE", "BIAS", "DARK", "STANDARD", "SCRIPT", "AUTO_FOCUS", "ENGINEERING", "SKY_FLAT"]
    instrument_type: Literal["1M0-SCICAM-SINISTRO"] = "1M0-SCICAM-SINISTRO"
    repeat_duration: NonNegativeInt | None = None
    extra_params: dict[Any, Any] = {}
    instrument_configs: list[Lco1M0ScicamSinistroConfig] = []
    acquisition_config: Lco1M0ScicamSinistroAcquisitionConfig
    guiding_config: Lco1M0ScicamSinistroGuidingConfig
    target: SiderealTarget | NonSiderealTarget
    constraints: Constraints

    config_class = Lco1M0ScicamSinistroConfig
    guiding_config_class = Lco1M0ScicamSinistroGuidingConfig
    acquisition_config_class = Lco1M0ScicamSinistroAcquisitionConfig
    optical_elements_class = Lco1M0ScicamSinistroOpticalElements


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
    extra_params: dict[Any, Any] = {}
    optical_elements: Lco2M0FloydsScicamOpticalElements


class Lco2M0FloydsScicam(BaseModel):
    model_config = ConfigDict(validate_assignment=True)
    type: Literal["SPECTRUM", "REPEAT_SPECTRUM", "ARC", "ENGINEERING", "SCRIPT", "LAMP_FLAT"]
    instrument_type: Literal["2M0-FLOYDS-SCICAM"] = "2M0-FLOYDS-SCICAM"
    repeat_duration: NonNegativeInt | None = None
    extra_params: dict[Any, Any] = {}
    instrument_configs: list[Lco2M0FloydsScicamConfig] = []
    acquisition_config: Lco2M0FloydsScicamAcquisitionConfig
    guiding_config: Lco2M0FloydsScicamGuidingConfig
    target: SiderealTarget | NonSiderealTarget
    constraints: Constraints

    config_class = Lco2M0FloydsScicamConfig
    guiding_config_class = Lco2M0FloydsScicamGuidingConfig
    acquisition_config_class = Lco2M0FloydsScicamAcquisitionConfig
    optical_elements_class = Lco2M0FloydsScicamOpticalElements


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
    extra_params: dict[Any, Any] = {}
    optical_elements: Lco2M0ScicamMuscatOpticalElements


class Lco2M0ScicamMuscat(BaseModel):
    model_config = ConfigDict(validate_assignment=True)
    type: Literal["EXPOSE", "REPEAT_EXPOSE", "BIAS", "DARK", "STANDARD", "SCRIPT", "AUTO_FOCUS", "ENGINEERING", "SKY_FLAT"]
    instrument_type: Literal["2M0-SCICAM-MUSCAT"] = "2M0-SCICAM-MUSCAT"
    repeat_duration: NonNegativeInt | None = None
    extra_params: dict[Any, Any] = {}
    instrument_configs: list[Lco2M0ScicamMuscatConfig] = []
    acquisition_config: Lco2M0ScicamMuscatAcquisitionConfig
    guiding_config: Lco2M0ScicamMuscatGuidingConfig
    target: SiderealTarget | NonSiderealTarget
    constraints: Constraints

    config_class = Lco2M0ScicamMuscatConfig
    guiding_config_class = Lco2M0ScicamMuscatGuidingConfig
    acquisition_config_class = Lco2M0ScicamMuscatAcquisitionConfig
    optical_elements_class = Lco2M0ScicamMuscatOpticalElements


class LcoBlancoNewfirmOpticalElements(BaseModel):
    model_config = ConfigDict(validate_assignment=True)
    filter: Literal["JX", "HX", "KXs", "1187", "2096", "1644", "2124", "2168", "J1", "1066", "DARK"]


class LcoBlancoNewfirmGuidingConfig(BaseModel):
    model_config = ConfigDict(validate_assignment=True)
    mode: Literal["ON"]
    optional: bool
    """Whether the guiding is optional or not"""
    exposure_time: Annotated[int, NonNegativeInt, Le(120)] | None = None
    """Guiding exposure time"""
    extra_params: dict[Any, Any] = {}


class LcoBlancoNewfirmAcquisitionConfig(BaseModel):
    model_config = ConfigDict(validate_assignment=True)
    mode: Literal["MANUAL"]
    exposure_time: Annotated[int, NonNegativeInt, Le(60)] | None = None
    """Acquisition exposure time"""
    extra_params: dict[Any, Any] = {}


class LcoBlancoNewfirmConfig(BaseModel):
    model_config = ConfigDict(validate_assignment=True)
    exposure_count: PositiveInt
    """The number of exposures to take. This field must be set to a value greater than 0"""
    exposure_time: NonNegativeInt
    """ Exposure time in seconds"""
    mode: Literal["fowler1", "fowler8", "fowler16", "fowler2", "fowler4"]
    rois: list[Roi] | None = None
    extra_params: dict[Any, Any] = {}
    optical_elements: LcoBlancoNewfirmOpticalElements


class LcoBlancoNewfirm(BaseModel):
    model_config = ConfigDict(validate_assignment=True)
    type: Literal["EXPOSE", "SKY_FLAT", "STANDARD", "DARK"]
    instrument_type: Literal["BLANCO_NEWFIRM"] = "BLANCO_NEWFIRM"
    repeat_duration: NonNegativeInt | None = None
    extra_params: dict[Any, Any] = {}
    instrument_configs: list[LcoBlancoNewfirmConfig] = []
    acquisition_config: LcoBlancoNewfirmAcquisitionConfig
    guiding_config: LcoBlancoNewfirmGuidingConfig
    target: SiderealTarget | NonSiderealTarget
    constraints: Constraints

    config_class = LcoBlancoNewfirmConfig
    guiding_config_class = LcoBlancoNewfirmGuidingConfig
    acquisition_config_class = LcoBlancoNewfirmAcquisitionConfig
    optical_elements_class = LcoBlancoNewfirmOpticalElements


# Export a type that encompasses all instruments
LCO_INSTRUMENTS = Union[
    Lco0M4ScicamQhy600,
    Lco1M0NresScicam,
    Lco1M0ScicamSinistro,
    Lco2M0FloydsScicam,
    Lco2M0ScicamMuscat,
    LcoBlancoNewfirm,
]