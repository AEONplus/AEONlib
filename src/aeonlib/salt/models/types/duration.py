from typing import Annotated, Union

from astropy import units as u
from astropy.units import Quantity

from aeonlib.salt.models.types import AstropyQuantityTypeAnnotation
from aeonlib.salt.validators import GreaterThan

Duration = Annotated[Union[Quantity, float], AstropyQuantityTypeAnnotation(u.s)]

PositiveDuration = Annotated[Duration, GreaterThan(0 * u.s)]
