from typing import Annotated, Literal

from annotated_types import Ge, Le
from pydantic import AfterValidator, BaseModel

from aeonlib.conf import settings
from aeonlib.types import Time


def valid_project_id(value: str) -> str:
    if value not in settings.lt_proposal_ids:
        raise ValueError(f"Invalid project ID: {value}")

    return value


class LTObservation(BaseModel):
    project: Annotated[str, AfterValidator(valid_project_id)]
    start: Time
    end: Time
    max_airmass: Annotated[float, Ge(1.0), Le(3.0)] = 2.0
    max_seeing: Annotated[float, Ge(1.0), Le(5.0)] = 1.2
    max_skybrightness: Annotated[float, Ge(0.0), Le(10.0)] = 1.0
    photometric: bool = False
    """True -> clear, False -> light"""


# class Filter(BaseModel):
#     name: str
#     exp_time: Annotated[float, Ge(0.0)] = 120
#     exp_count: Annotated[int, Ge(0)] = 0


"""Instruments to support:
IO:O
RISE
SPRAT
FRODOSpec
MOPTOP
LIRIC
SkyCam??
"""


class Ioo(BaseModel):
    binning: Literal["1x1", "2x2"] = "2x2"
    exp_time_U: Annotated[float, Ge(0.0)] = 120.0
    exp_count_U: Annotated[int, Ge(0)] = 0
    exp_time_R: Annotated[float, Ge(0.0)] = 120.0
    exp_count_R: Annotated[int, Ge(0)] = 0
    exp_time_G: Annotated[float, Ge(0.0)] = 120.0
    exp_count_G: Annotated[int, Ge(0)] = 0
    exp_time_I: Annotated[float, Ge(0.0)] = 120.0
    exp_count_I: Annotated[int, Ge(0)] = 0
    exp_time_Z: Annotated[float, Ge(0.0)] = 120.0
    exp_count_Z: Annotated[int, Ge(0)] = 0
    exp_time_B: Annotated[float, Ge(0.0)] = 120.0
    exp_count_B: Annotated[int, Ge(0)] = 0
    exp_time_V: Annotated[float, Ge(0.0)] = 120.0
    exp_count_V: Annotated[int, Ge(0)] = 0
    exp_time_Halpha6566: Annotated[float, Ge(0.0)] = 120.0
    exp_count_Halpha6566: Annotated[int, Ge(0)] = 0
    exp_time_Halpha6634: Annotated[float, Ge(0.0)] = 120.0
    exp_count_Halpha6634: Annotated[int, Ge(0)] = 0
    exp_time_Halpha6705: Annotated[float, Ge(0.0)] = 120.0
    exp_count_Halpha6705: Annotated[int, Ge(0)] = 0
    exp_time_Halpha6755: Annotated[float, Ge(0.0)] = 120.0
    exp_count_Halpha6755: Annotated[int, Ge(0)] = 0
    exp_time_Halpha6822: Annotated[float, Ge(0.0)] = 120.0
    exp_count_Halpha6822: Annotated[int, Ge(0)] = 0


class Sprat(BaseModel):
    exp_time: Annotated[float, Ge(0.0)] = 120.0
    exp_count: Annotated[int, Ge(1)] = 1
    grating: Literal["red", "blue"] = "red"


class Frodo(BaseModel):
    exp_time_blue: Annotated[float, Ge(0.0)] = 120.0
    exp_count_blue: Annotated[int, Ge(0)] = 1
    res_blue: Literal["high", "low"] = "low"
    exp_time_red: Annotated[float, Ge(0.0)] = 120.0
    exp_count_red: Annotated[int, Ge(0)] = 1
    res_red: Literal["high", "low"] = "low"
