"""This module contains Pydantic models for SALT blocks."""

from __future__ import annotations

from typing import Annotated, Literal, Self

import astropy.units as u
from annotated_types import Ge, Le
from pydantic import (
    BaseModel,
    NonNegativeInt,
    NonNegativeFloat,
    PositiveInt,
    PositiveFloat,
    model_validator,
)

from aeonlib.models import Angle, Window
from aeonlib.salt.models import SaltSiderealTarget
from aeonlib.salt.validators import GreaterEqual, LessEqual

Transparency = Literal["clear", "thin cloud", "thick cloud", "any"]


class Block(BaseModel):
    """
    A block for SALT.

    Blocks are the smallest schedulable unit for an observation; i.e. block is either
    observed in total or not ar all. Every block has a unique `identifier`, which should
    only be set if you are resubmitting an existing block.

    Observing time for SALT is allocated for different priorities, and you must specify
    which is the priority for your block. You also have to rank the block relative to
    the other blocks in the proposal.

    The number of visits defines how often the block shall be observed in the
    semester for which the submission is made. If you request more than one visit,
    you can give a minimum of nights to wait between the observations. For example,
    if a block is observed during the night starting on 1 September and this wait
    period is 2, the next observation will only take place during the night starting
    on 3 September.

    If a block spans multiple semesters, you can provide a maximum number of
    observations for all semesters combined. This number must at least be equal to the
    number of visits.

    Several blocks can be grouped in a pool. You can specify the pool's name if the
    block shall belong to a pool. This pool must exist in the proposal already.

    Other details to specify for the block are the observation constraints, the target
    to observe, the acquisition details and the instrument configuration. For time
    restricted observation you also may define observing windows.

    By default, observers are notified of new data after the data reduction pipeline has
    run for the night of observation. If instead you want to be notified once the data
    is transferred to Cape Town (before the pipeline runs), you can set the data
    notification accordingly.

    Attributes
    ----------
    name
        Human-friendly name for the block. This must be unique within a proposal.
    identifier
        Unique identifier for the block. Only set this if you are resubmitting an
        existing block.
    comments
        Optional comments for the observer.
    priority
        Priority for the block.
    ranking
        Ranking (importance) of this block relative to the other blocks in the proposal.
    num_visits
        Number of visits, i.e. how often the block shall be observed in the semester
        for which the submission is made.
    max_num_visits
        Maximum number of visits, i.e. the maximum number of times the block shall be
        observed for all semesters combined.
    min_nights_between_visits
        Minimum number of nights to wait between subsequent observations of the block.
    constraints
        Observation constraints.
    windows
        List of time intervals during which the block shall be observed.
    target
        Target to observe.
    acquisition
        Acquisition details.
    instrument
        Instrument configuration.
    pool
        Name of the pool to which the block shall belong. The pool must exist in the
        proposal already.
    data_notification
        When you want to be notified about new data for the block.
    """

    name: str
    identifier: str | None = None
    comments: str | None = None
    priority: Annotated[int, Ge(0), Le(4)]
    ranking: Literal["high", "medium", "low"]
    num_visits: PositiveInt
    max_num_visits: PositiveInt | None = None
    min_nights_between_visits: NonNegativeInt = 0
    constraints: None
    windows: list[Window] | None = None
    target: SaltSiderealTarget
    acquisition: None
    instrument: None
    pool: str | None = None
    data_notification: Literal["normal", "fast"] = "normal"

    @model_validator(mode="after")
    def check_max_num_visits_is_at_least_num_visits(self) -> Self:
        if self.max_num_visits:
            if self.max_num_visits < self.num_visits:
                raise ValueError(
                    "max_num_visits must be greater than or equal to num_visits."
                )

        return self


class Constraints(BaseModel):
    """
    Observing constraints.

    An observation can be constrained by the sky transparency, the Moon phase, the lunar
    distance and the seeing.

    The lunar phase is specified in terms of what percentage p of the lunar disk is
    illuminated. For New Moon p is 0, for Full Moon it is 100. In general, p and the
    lunar elongation e (i.e., the angle between Sun, observer on Earth and Moon) are
    related by p = 100% * (1 - cos(e)) / 2.

    The lunar distance is the angle between the target to observe, Earth and Moon.

    The lunar phase and distance are only relevant if the Moon is above the horizon.

    The seeing must be given for the zenith.

    Attributes
    ----------
    transparency
        Required sky transparency.
    max_lunar_phase_percentage
        Maximum allowed Lunar phase, as a percentage. This is the percentage of the
        lunar disk which is illuminated.
    min_lunar_distance
        Minimum required lunar distance.
    max_seeing
        Maximum allowed seeing.
    """

    transparency: Transparency
    max_lunar_phase_percentage: Annotated[NonNegativeFloat, LessEqual(100)]
    min_lunar_distance: Annotated[
        Angle, GreaterEqual(0 * u.deg), LessEqual(180 * u.deg)
    ]
    max_seeing: PositiveFloat
