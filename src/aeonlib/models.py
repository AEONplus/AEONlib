"""
Models shared between facilities.
"""

from typing import Annotated, Any, Literal

from annotated_types import Ge, Le
from pydantic import BaseModel, ConfigDict
from pydantic.types import (
    NonNegativeFloat,
    StringConstraints,
)

from aeonlib.types import Angle, Time


class SiderealTarget(BaseModel):
    model_config = ConfigDict(validate_assignment=True)
    name: Annotated[str, StringConstraints(max_length=50)] = "string"
    """The name of this Target"""
    type: Literal["ICRS", "HOUR_ANGLE", "ALTAZ"]
    """The type of this Target"""
    hour_angle: Angle | None = None
    """Hour angle of this Target in decimal degrees"""
    ra: Angle
    """Right ascension in decimal degrees"""
    dec: Angle
    """Declination in decimal degrees"""
    altitude: Angle | None = None
    """Altitude of this Target in decimal degrees"""
    azimuth: Angle | None = None
    """Azimuth of this Target in decimal degrees east of North"""
    proper_motion_ra: Annotated[float, Le(20000.0)] = 0
    """Right ascension proper motion of the Target in mas/year. Defaults to 0."""
    proper_motion_dec: Annotated[float, Le(20000.0)] = 0
    """Declination proper motion of the Target in mas/year. Defaults to 0."""
    epoch: Annotated[int, Le(2100)] = 2000
    """Epoch of coordinates in Julian Years. Defaults to 2000."""
    parallax: Annotated[float, Le(2000)] = 0
    """Parallax of the Target in mas, max 2000. Defaults to 0."""


class NonSiderealTarget(BaseModel):
    model_config = ConfigDict(validate_assignment=True)
    name: Annotated[str, StringConstraints(max_length=50)] = "string"
    """The name of this Target"""
    type: Literal["ORBITAL_ELEMENTS", "SATELLITE"]
    """The type of this Target TODO: Where does HOUR_ANGLE make sense?"""
    scheme: Literal[
        "ASA_MAJOR_PLANET",
        "ASA_MINOR_PLANET",
        "ASA_COMET",
        "JPL_MAJOR_PLANET",
        "JPL_MINOR_PLANET",
        "MPC_MINOR_PLANET",
        "MPC_COMET",
    ]
    """The Target scheme to use"""
    epochofel: Annotated[float, Ge(10_000), Le(100_000)]
    """The epoch of the orbital elements (MJD)"""
    orbinc: Angle
    """Orbital inclination (angle in degrees)"""
    longascnode: Angle
    """Longitude of ascending node (angle in degrees)"""
    argofperih: Angle
    """Argument of perihelion (angle in degrees)"""
    eccentricity: NonNegativeFloat
    """Eccentricity of the orbit"""
    meandist: Annotated[float, NonNegativeFloat]
    """Semi-major axis (AU)"""  # Not Comet
    meananom: Angle
    """Mean anomaly (angle in degrees)"""
    perihdist: Annotated[float, NonNegativeFloat] | None = None
    """Perihelion distance (AU)"""  # Comet Only
    epochofperih: Annotated[float, Ge(10_000), Le(100_000)] | None = None
    """Epoch of perihelion (MJD)"""  # Comet Only
    dailymot: float | None = None
    """Daily motion (angle in degrees)"""  # Major Planet Only
    altitude: Angle | None = None
    """Altitude of this Target in decimal degrees"""  # Satellite Only
    azimuth: Angle | None = None
    """Azimuth of this Target in decimal degrees east of North"""  # Satellite Only
    diff_altitude_rate: float | None = None
    """Differential altitude rate (arcsec/s)"""  # Satellite Only
    diff_azimuth_rate: float | None = None
    """Differential azimuth rate (arcsec/s)"""  # Satellite Only
    diff_epoch: float | None = None
    """Reference time for non-sidereal motion (MJD)"""  # Satellite Only
    diff_altitude_acceleration: float | None = None
    """Differential altitude acceleration (arcsec/s^2)"""  # Satellite Only
    diff_azimuth_acceleration: float | None = None
    """Differential azimuth acceleration (arcsec/s^2)"""  # Satellite Only
    meanlong: Angle | None = None
    """Mean longitude (angle in degrees)"""  # Major Planet Only
    longofperih: Angle | None = None
    """Longitude of perihelion (angle in degrees)"""  # Major Planet Only
    extra_params: dict[Any, Any] = {}


class Window(BaseModel):
    """A general time window"""

    model_config = ConfigDict(validate_assignment=True)
    start: Time | None = None
    end: Time
