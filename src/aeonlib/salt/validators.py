"""This module defines some Pydantic validators."""

from typing import Any

from pydantic import AfterValidator


def _check_gt(a: Any, b: Any) -> Any:
    if a <= b:
        raise ValueError(f"{a} is not greater than to {b}.")
    return a


def _check_ge(a: Any, b: Any) -> Any:
    if a < b:
        raise ValueError(f"{a} is not greater than or equal to {b}.")
    return a


def _check_lt(a: Any, b: Any) -> None:
    if a >= b:
        raise ValueError(f"{a} is not less than to {b}.")
    return a


def _check_le(a: Any, b: Any) -> None:
    if a > b:
        raise ValueError(f"{a} is not less than or equal to {b}.")
    return a


def GreaterThan(value: Any):
    """
    Return a Pydantic validator for checking a greater than relation.

    The returned validator can be used in a type annotation::

        import pydantic

        class DummyModel(pydantic.BaseModel):
            duration: Annotated[float, GreaterThan(4)]

    Pydantic will first perform its own internal validation and then check whether
    the field value is greater than the argument passed to `GreaterThan` (4 in the
    example above).

    It is up to the user to ensure that the field value and the argument of
    `GreaterThan` can be compared.

    Parameters
    ----------
    value
       Value against which to compare.

    Returns
    -------
    A validator for checking a greater than relation.
    """
    return AfterValidator(lambda v: _check_gt(v, value))


def GreaterEqual(value: Any):
    """
    Return a Pydantic validator for checking a greater than or equal to relation.

    The returned validator can be used in a type annotation::

        import pydantic

        class DummyModel(pydantic.BaseModel):
            duration: Annotated[float, GreaterEqual(4)]

    Pydantic will first perform its own internal validation and then check whether
    the field value is greater than or equal to the argument passed to `GreaterEqual`
    (4 in the example above).

    It is up to the user to ensure that the field value and the argument of
    `GreaterEqual` can be compared.

    Parameters
    ----------
    value
       Value against which to compare.

    Returns
    -------
    A validator for checking a greater than or equal to relation.
    """
    return AfterValidator(lambda v: _check_ge(v, value))


def LessThan(value: Any):
    """
    Return a Pydantic validator for checking a less than relation.

    The returned validator can be used in a type annotation::

        import pydantic

        class DummyModel(pydantic.BaseModel):
            height: Annotated[float, LessThan(4)]

    Pydantic will first perform its own internal validation and then check whether
    the field value is less than or equal to the argument passed to `LessEqual` (4 in
    the example above).

    It is up to the user to ensure that the field value and the argument of
    `LessThan` can be compared.

    Parameters
    ----------
    value
       Value against which to compare.

    Returns
    -------
    A validator for checking a less than relation.
    """
    return AfterValidator(lambda v: _check_lt(v, value))


def LessEqual(value: Any):
    """
    Return a Pydantic validator for checking a less than or equal to relation.

    The returned validator can be used in a type annotation::

        import pydantic

        class DummyModel(pydantic.BaseModel):
            height: Annotated[float, LessEqual(4)]

    Pydantic will first perform its own internal validation and then check whether
    the field value is less than or equal to the argument passed to `LessEqual` (4 in
    the example above).

    It is up to the user to ensure that the field value and the argument of
    `LessEqual` can be compared.

    Parameters
    ----------
    value
       Value against which to compare.

    Returns
    -------
    A validator for checking a less than or equal to relation.
    """
    return AfterValidator(lambda v: _check_le(v, value))
