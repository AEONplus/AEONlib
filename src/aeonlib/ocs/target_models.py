from typing import Annotated, Any, ClassVar

from annotated_types import Le
from pydantic import BaseModel, ConfigDict
from pydantic.types import (
    NonNegativeFloat,
    PositiveFloat,
)


class Constraints(BaseModel):
    model_config: ClassVar[ConfigDict] = ConfigDict(validate_assignment=True)
    max_airmass: Annotated[float, PositiveFloat, Le(25.0)] = 1.6
    max_lunar_distance: Annotated[float, NonNegativeFloat, Le(180.0)] = 30.00
    max_lunar_phase: Annotated[float, PositiveFloat, Le(1.0)] = 1.0
    max_seeing: NonNegativeFloat | None = None
    """Maximum acceptable seeing"""
    min_transparency: float | None = None
    """Minimum acceptable transparency"""
    extra_params: dict[Any, Any] = {}
