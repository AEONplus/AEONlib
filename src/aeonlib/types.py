# pyright: reportUnknownVariableType=false
# pyright: reportUnknownMemberType=false
import logging
from datetime import datetime
from typing import Annotated, Any, cast

import astropy.coordinates
import astropy.time
from astropy.units import Quantity
from pydantic import GetCoreSchemaHandler, GetJsonSchemaHandler
from pydantic.json_schema import JsonSchemaValue
from pydantic_core import core_schema

logger = logging.getLogger(__name__)


class _AstropyTimeType:
    """
    Custom Pydantic type that handles astropy.time.Time serialization and parsing.
    This should enable using astropy Time objects as pydantic fields that are interoperable
    with datetime objects.
    """

    @classmethod
    def __get_pydantic_core_schema__(
        cls,
        _source_type: type[Any],
        handler: GetCoreSchemaHandler,
    ) -> core_schema.CoreSchema:
        """https://docs.pydantic.dev/latest/concepts/types/#handling-third-party-types"""

        def validate_from_datetime(datetime_value: datetime) -> astropy.time.Time:
            return astropy.time.Time(datetime_value)

        from_datetime_schema = core_schema.chain_schema(
            [
                core_schema.datetime_schema(),
                core_schema.no_info_plain_validator_function(validate_from_datetime),
            ]
        )

        def serialize_time(
            _model: Any,
            time_obj: astropy.time.Time,
            info: core_schema.SerializationInfo,
        ) -> datetime | str | float:
            """
            Determines how to serialize an astropy.time.Time object when model_dump()
            is called. This can be configured dynamically on the calling class by setting the
            `output_mapping` context. Here is an example:

            ```python
            output_mapping = {"epochofel": "mjd", "epochofperih": "mjd"}
            request_group.model_dump(
                mode="json", exclude_none=True, context={"output_mapping": output_mapping}
            )
            ```
            This would result in the epochofel and epochofperih values being output as mjd.
            """
            field_name = getattr(info, "field_name", "")
            context = getattr(info, "context", {})
            if field_name and context:
                output_mapping = context.get("output_mapping", {})
                output_type = output_mapping.get(field_name, "datetime")
                try:
                    return getattr(time_obj, output_type)
                except AttributeError:
                    logger.exception(
                        f"Invalid output type '{output_type}' for field '{field_name}'. "
                        + "Ensure output mapping is an attribute of astropy.time.Time."
                    )

            return time_obj.datetime  # pyright: ignore[reportReturnType]

        return core_schema.json_or_python_schema(
            json_schema=from_datetime_schema,
            python_schema=core_schema.union_schema(
                [
                    # Try Time directly first
                    core_schema.is_instance_schema(astropy.time.Time),
                    # Then try datetime
                    from_datetime_schema,
                ]
            ),
            serialization=core_schema.plain_serializer_function_ser_schema(
                serialize_time, is_field_serializer=True, info_arg=True
            ),
        )

    @classmethod
    def __get_pydantic_json_schema__(
        cls, _core_schema: core_schema.CoreSchema, handler: GetJsonSchemaHandler
    ) -> JsonSchemaValue:
        # Use the same schema that would be used for `datetime`
        return handler(core_schema.datetime_schema())


class _AstropyTimeMJDType:
    """
    Custom Pydantic type that handles astropy.time.Time serialization and parsing.
    Accepts floats as M/JD values and serializes output as MJD.
    """

    @classmethod
    def __get_pydantic_core_schema__(
        cls,
        _source_type: type[Any],
        handler: GetCoreSchemaHandler,
    ) -> core_schema.CoreSchema:
        """https://docs.pydantic.dev/latest/concepts/types/#handling-third-party-types"""

        def validate_from_datetime(datetime_value: datetime) -> astropy.time.Time:
            return astropy.time.Time(datetime_value, scale="tt")

        def validate_from_float(value: float) -> astropy.time.Time:
            if value - 2400000.5 > 0:
                return astropy.time.Time(value, format="jd", scale="tt")
            else:
                return astropy.time.Time(value, format="mjd", scale="tt")

        from_datetime_schema = core_schema.chain_schema(
            [
                core_schema.datetime_schema(),
                core_schema.no_info_plain_validator_function(validate_from_datetime),
            ]
        )

        from_float_schema = core_schema.chain_schema(
            [
                core_schema.float_schema(),
                core_schema.no_info_plain_validator_function(validate_from_float),
            ]
        )

        def serialize_time(time_obj: astropy.time.Time) -> float:
            return time_obj.mjd  # pyright: ignore[reportReturnType]

        return core_schema.json_or_python_schema(
            json_schema=core_schema.union_schema(
                [from_float_schema, from_datetime_schema]
            ),
            python_schema=core_schema.union_schema(
                [
                    # Try Time directly first
                    core_schema.is_instance_schema(astropy.time.Time),
                    # Then try float (MJD)
                    from_float_schema,
                    # Then try datetime
                    from_datetime_schema,
                ]
            ),
            serialization=core_schema.plain_serializer_function_ser_schema(
                serialize_time
            ),
        )

    @classmethod
    def __get_pydantic_json_schema__(
        cls, _core_schema: core_schema.CoreSchema, handler: GetJsonSchemaHandler
    ) -> JsonSchemaValue:
        return {
            "anyOf": [
                handler(core_schema.float_schema()),
                handler(core_schema.datetime_schema()),
            ]
        }


class _AstropyAngleType:
    """
    Custom pydantic type that handles Angle types. It accepts
    astropy.coordinates.Angle objects, astropy.units.Quantity objects, strings and
    floats during validation. Internally the data is stored as an angle for maximum
    precision and flexibility. During serialization, the angle is converted to a
    decimal degree representation by default.
    """

    @classmethod
    def __get_pydantic_core_schema__(
        cls,
        _source_type: type[Any],
        _handler: GetCoreSchemaHandler,
    ) -> core_schema.CoreSchema:
        """https://docs.pydantic.dev/latest/concepts/types/#handling-third-party-types"""

        def validate_from_quantity(
            angle_value: Quantity,
        ) -> astropy.coordinates.Angle:
            return astropy.coordinates.Angle(angle_value)

        def validate_from_str(angle_value: str) -> astropy.coordinates.Angle:
            return astropy.coordinates.Angle(angle_value)

        def validate_from_float(angle_value: float) -> astropy.coordinates.Angle:
            return astropy.coordinates.Angle(angle_value, unit="deg")

        quantity_schema = core_schema.chain_schema(
            [
                core_schema.is_instance_schema(Quantity),
                core_schema.no_info_plain_validator_function(validate_from_quantity),
            ]
        )

        str_schema = core_schema.chain_schema(
            [
                core_schema.str_schema(),
                core_schema.no_info_plain_validator_function(validate_from_str),
            ]
        )

        float_schema = core_schema.chain_schema(
            [
                core_schema.float_schema(),
                core_schema.no_info_plain_validator_function(validate_from_float),
            ]
        )

        def serialize_angle(angle_obj: astropy.coordinates.Angle) -> float:
            return cast(float, angle_obj.to_value(unit="deg"))

        return core_schema.json_or_python_schema(
            json_schema=core_schema.union_schema([str_schema, float_schema]),
            python_schema=core_schema.union_schema(
                [
                    core_schema.is_instance_schema(astropy.coordinates.Angle),
                    quantity_schema,
                    str_schema,
                    float_schema,
                ]
            ),
            serialization=core_schema.plain_serializer_function_ser_schema(
                serialize_angle
            ),
        )

    @classmethod
    def __get_pydantic_json_schema__(
        cls, _core_schema: core_schema.CoreSchema, handler: GetJsonSchemaHandler
    ) -> JsonSchemaValue:
        return {
            "anyOf": [
                handler(core_schema.str_schema()),
                handler(core_schema.float_schema()),
            ]
        }


Time = Annotated[astropy.time.Time | datetime, _AstropyTimeType]
TimeMJD = Annotated[astropy.time.Time | datetime | float, _AstropyTimeMJDType]
Angle = Annotated[
    astropy.coordinates.Angle | Quantity | str | float,
    _AstropyAngleType,
]
