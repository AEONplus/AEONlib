from typing import Annotated

from astropy import units as u
from astropy.units import Quantity

from aeonlib.salt.models.types.quantity import AstropyQuantityTypeAnnotation
from aeonlib.salt.validators import GreaterThan

Duration = Annotated[Quantity | float, AstropyQuantityTypeAnnotation(u.s)]

PositiveDuration = Annotated[Duration, GreaterThan(0 * u.s)]
