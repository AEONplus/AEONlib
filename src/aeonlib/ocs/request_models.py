from datetime import datetime
from typing import Annotated, Any, Literal, Union

from annotated_types import Ge, Le
from pydantic import BaseModel, ConfigDict, Field
from pydantic.types import (
    NonNegativeFloat,
    NonNegativeInt,
    PositiveInt,
    StringConstraints,
)

from aeonlib.models import Window
from aeonlib.ocs.lco.instruments import LCO_INSTRUMENTS
from aeonlib.ocs.soar.instruments import SOAR_INSTRUMENTS


class Location(BaseModel):
    """
    Location constraints for this request.
    TODO: Seems the OpenAPI spec does not specify values.
    """

    model_config = ConfigDict(validate_assignment=True)
    site: str | None = None
    enclosure: str | None = None
    telescope: str | None = None
    telescope_class: str


class Cadence(BaseModel):
    """Request level cadence configuration"""

    model_config = ConfigDict(validate_assignment=True)
    start: datetime
    end: datetime
    period: Annotated[float, Ge(0.02)]
    jitter: Annotated[float, Ge(0.02)]


# Informs Pydantic which instrument configuration type should be used during parsing
Configuration = Annotated[
    Union[LCO_INSTRUMENTS, SOAR_INSTRUMENTS], Field(discriminator="instrument_type")
]


class Request(BaseModel):
    """A request for a single, discrete observation. One group can contain multiple
    requests"""

    model_config = ConfigDict(validate_assignment=True)
    acceptability_threshold: Annotated[int, NonNegativeInt, Le(100)] = 90
    """
    The percentage of the observation that must be completed to mark the request as
    complete and avert rescheduling. The percentage should be set to the lowest value
    for which the amount of data is acceptable to meet the science goal of the request.
    """
    configuration_repeats: PositiveInt = 1
    """
    The number of times this Request's set of Configurations should be repeated.
    This is useful for nodding back and forth between a set of Targets that are too
    far apart to use Dithering.
    """
    optimization_type: Literal["TIME", "AIRMASS"] = "TIME"
    """
    Optimization to use when scheduling. TIME favors placing requests earlier in their
    window. AIRMASS favors placing requests at lower airmass (higher altitude).
    """
    observation_note: Annotated[str, StringConstraints(max_length=255)] | None = None
    """Text describing this Request"""
    extra_params: dict[Any, Any] = {}
    configurations: list[Configuration]
    cadence: Cadence | None = None
    windows: list[Window]
    location: Location


class RequestGroup(BaseModel):
    """
    An Observation request for any observatory that supports an OCS API.
    """

    model_config = ConfigDict(validate_assignment=True)
    name: Annotated[str, StringConstraints(max_length=50)]
    """
    Descriptive name for this RequestGroup. This string will be placed in the
    FITS header as the GROUPID keyword value for all FITS frames originating from this
    RequestGroup.
    """
    proposal: str
    """The proposal ID awarded time"""
    ipp_value: NonNegativeFloat
    """A multiplier to the base priority of the Proposal for this RequestGroup
    and all child Requests. A value > 1.0 will raise the priority and debit the Proposal
    ipp_time_available upon submission. If a Request does not complete, the time debited
    for that Request is returned. A value < 1.0 will lower the priority and credit the
    ipp_time_available of the Proposal up to the ipp_limit on the successful completion
    of a Request. The value is generally set to 1.05.
    """
    operator: Literal["SINGLE", "MANY"]
    """Operator that describes how child Requests are scheduled.
    Use SINGLE if you have only one Request and MANY if you have more than one.
    """
    observation_type: Literal["NORMAL", "RAPID_RESPONSE", "TIME_CRITICAL", "DIRECT"]
    """The type of observations under this RequestGroup. Requests submitted with
    RAPID_RESPONSE bypass normal scheduling and are executed immediately.
    Requests submitted with TIME_CRITICAL are scheduled normally but with a high priority.
    These modes are only available if the Proposal was granted special time.
    """
    requests: list[Request] = []


class SubmittedRequestGroup(RequestGroup):
    """
    Represents an request group that is saved in the OCS database
    """

    id: int
    state: Literal[
        "PENDING", "COMPLETED", "WINDOW_EXPIRED", "FAILURE_LIMIT_REACHED", "CANCELED"
    ]
    submitter: str
    created: datetime
    modified: datetime
