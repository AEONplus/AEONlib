from typing import ClassVar

from pydantic import BaseModel, ConfigDict
from pydantic.types import NonNegativeInt


class Roi(BaseModel):
    """Region of Interest"""

    model_config: ClassVar[ConfigDict] = ConfigDict(validate_assignment=True)
    x1: NonNegativeInt | None = None
    x2: NonNegativeInt | None = None
    y1: NonNegativeInt | None = None
    y2: NonNegativeInt | None = None
