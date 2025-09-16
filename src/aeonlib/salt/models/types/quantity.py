import dataclasses
from typing import Any

from astropy.units import UnitBase, Quantity
from pydantic import GetCoreSchemaHandler, GetJsonSchemaHandler
from pydantic.json_schema import JsonSchemaValue
from pydantic_core import core_schema


@dataclasses.dataclass(frozen=True)
class AstropyQuantityTypeAnnotation:
    """
    Annotation for defining custom Pydantic types based on a `astropy.units.Quantity`.

    To define such a custom type, instantiate `AstropyQuantityTypeAnnotation` with the
    default unit `d` and pass it as a type annotation. Pydantic fields with this type can
    be instantiated wth a `float` or a `astropy.units.Quantity` with units that are
    compatible with `d`. If a `float` is used, it is assumed to be given with `d` as the
    unit. The field is stored as a `astropy.units.Quantity` with unit `d`.

    For example, you can define a ProperMotion type as follows:

    ```
    from typing import Annotated, Union
    from astropy import units as u
    from astropy.units import Quantity
    from aeonlib.salt.models.types import AstropyQuantityTypeAnnotation

    ProperMotion = Annotated[Union[Quantity, float], AstropyQuantityTypeAnnotation(u.arcsec / u.year)]
    ```

    This type can then be used in a Pydantic model:

    ```
    from pydantic import BaseModel

    class MovingObject(BaseModel):
        proper_motion: ProperMotion

    # Create the same object in three different ways.
    # Note: 1 year = 8766 hours
    object1 = MovingObject(proper_motion=8766)  # 3 arcsec per year
    object2 = MovingObject(proper_motion=8766 * u.arcsec / u.year)
    object3 = MovingObject(proper_motion=1 * u.arcsec / u.hour)
    """

    # Based on
    # https://docs.pydantic.dev/latest/concepts/types/#handling-third-party-types

    default_unit: UnitBase

    def __get_pydantic_core_schema__(
        self,
        _source_type: Any,
        _handler: GetCoreSchemaHandler,
    ) -> core_schema.CoreSchema:
        def validate_from_float(value: float) -> Quantity:
            return Quantity(value, unit=self.default_unit)

        def validate_from_quantity(value: Quantity) -> Quantity:
            return value.to(self.default_unit)

        from_float_schema = core_schema.chain_schema(
            [
                core_schema.float_schema(),
                core_schema.no_info_plain_validator_function(validate_from_float),
            ]
        )

        from_quantity_schema = core_schema.chain_schema(
            [
                core_schema.is_instance_schema(Quantity),
                core_schema.no_info_plain_validator_function(validate_from_quantity),
            ]
        )

        return core_schema.json_or_python_schema(
            json_schema=from_float_schema,
            python_schema=core_schema.union_schema(
                [from_quantity_schema, from_float_schema]
            ),
            serialization=core_schema.plain_serializer_function_ser_schema(
                lambda instance: instance.to(self.default_unit).value
            ),
        )

    def __get_pydantic_json_schema(
        self, _core_schema: core_schema.CoreSchema, handler: GetJsonSchemaHandler
    ) -> JsonSchemaValue:
        return handler(core_schema.float_schema())
