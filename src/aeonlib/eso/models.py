from datetime import datetime, time
from typing import Any, ClassVar, Self

from astropy.coordinates import Angle
from pydantic import BaseModel, ConfigDict, Field
from pydantic.alias_generators import to_camel

from aeonlib.models import SiderealTarget, Window


class EsoModel(BaseModel):
    model_config: ClassVar[ConfigDict] = ConfigDict(
        alias_generator=to_camel, validate_by_name=True, serialize_by_alias=True
    )


class Constraints(EsoModel):
    airmass: float
    fli: float
    moon_distance: int
    name: str
    seeing: float
    sky_transparency: str
    twilight: int
    water_vapour: float


class ObsDescription(EsoModel):
    instrument_comments: str
    name: str
    user_comments: str


class Target(EsoModel):
    dec: str
    differential_dec: float
    differential_ra: float
    epoch: float
    equinox: str
    name: str
    proper_motion_dec: float
    proper_motion_ra: float
    ra: str

    def construct_from(self, st: SiderealTarget) -> None:
        """Fills in the target fields of an observation block
        using an general Aeonlib SiderealTarget object
        """
        # Format angles the way ESO wants them.
        assert isinstance(st.ra, Angle)
        assert isinstance(st.dec, Angle)
        self.ra = st.ra.to_string(sep=":", precision=3)  # pyright: ignore[reportUnknownMemberType]
        self.dec = st.dec.to_string(sep=":", precision=3)  # pyright: ignore[reportUnknownMemberType]
        self.epoch = st.epoch
        self.name = st.name
        self.proper_motion_dec = st.proper_motion_dec
        self.proper_motion_ra = st.proper_motion_ra


class ObservationBlock(EsoModel):
    version: str
    constraints: Constraints
    obs_description: ObsDescription
    target: Target
    execution_time: int
    exposure_time: int
    instrument: str
    ip_version: float
    item_type: str
    migrate: bool
    grade: str = "?"
    name: str
    ob_id: int
    ob_status: str
    parent_container_id: int
    run_id: int
    user_priority: int


class Container(EsoModel):
    container_id: int
    item_count: int
    item_type: str
    name: str
    parent_container_id: int
    run_id: int
    version: str


class Template(EsoModel):
    template_id: int
    template_name: str
    type: str
    parameters: list[dict[str, Any]]
    """
    TODO: see if we can auto-generate these somehow
    """
    version: str


# TODO figure out how to use a general Window class for these constraints
class AbsoluteTimeConstraint(EsoModel):
    # Fields are aliased due to from being a reserved keyword in Python
    start: datetime = Field(..., serialization_alias="from", validation_alias="from")
    end: datetime = Field(..., serialization_alias="to", validation_alias="to")

    @classmethod
    def construct_from(cls, window: Window) -> Self:
        if not window.start:
            raise ValueError("ESO constraints require a valid start time")
        else:
            return cls.model_validate(window.model_dump(mode="json"))


class AbsoluteTimeConstraints(EsoModel):
    constraints: list[AbsoluteTimeConstraint]
    version: str | None = None


class SiderealTimeConstraint(EsoModel):
    # Fields are aliased due to from being a reserved keyword in Python
    start: time = Field(..., serialization_alias="from", validation_alias="from")
    end: time = Field(..., serialization_alias="to", validation_alias="to")


class SiderealTimeConstraints(EsoModel):
    constraints: list[SiderealTimeConstraint]
    version: str | None = None


class Ephemeris(EsoModel):
    text: str
    version: str | None = None
