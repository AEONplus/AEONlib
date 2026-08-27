from typing import Annotated, Any

from pydantic import BeforeValidator, PlainSerializer


def _unwrap_double_value(value: Any) -> Any:
    if isinstance(value, dict):
        return value.get("value")
    return value


def _wrap_double_value(value: float | None) -> dict[str, float | None]:
    return {"value": value}


DoubleValue = Annotated[
    float | None,
    BeforeValidator(_unwrap_double_value),
    PlainSerializer(_wrap_double_value, return_type=dict[str, float | None]),
]
