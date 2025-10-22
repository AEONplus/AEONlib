"""
This module defines some Pydantic validators.

The validators are
"""

from typing import Any

import astropy.coordinates
from astropy import units as u
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


def Gt(value: Any):
    """
    Return a Pydantic validator for checking a greater than relation.

    The returned validator can be used in a type annotation::

        import pydantic

        class DummyModel(pydantic.BaseModel):
            duration: Annotated[float, Gt(4)]

    Pydantic will first perform its own internal validation and then check whether
    the field value is greater than the argument passed to `Gt` (4 in the example
    above).

    It is up to the user to ensure that the field value and the argument of `Gt` can
    be compared.

    Parameters
    ----------
    value
       Value against which to compare.

    Returns
    -------
    A validator for checking a greater than relation.
    """
    return AfterValidator(lambda v: _check_gt(v, value))


def Ge(value: Any):
    """
    Return a Pydantic validator for checking a greater than or equal to relation.

    The returned validator can be used in a type annotation::

        import pydantic

        class DummyModel(pydantic.BaseModel):
            duration: Annotated[float, Ge(4)]

    Pydantic will first perform its own internal validation and then check whether
    the field value is greater than or equal to the argument passed to `Ge` (4 in the
    example above).

    It is up to the user to ensure that the field value and the argument of `Ge` can
    be compared.

    Parameters
    ----------
    value
       Value against which to compare.

    Returns
    -------
    A validator for checking a greater than or equal to relation.
    """
    return AfterValidator(lambda v: _check_ge(v, value))


def Lt(value: Any):
    """
    Return a Pydantic validator for checking a less than relation.

    The returned validator can be used in a type annotation::

        import pydantic

        class DummyModel(pydantic.BaseModel):
            height: Annotated[float, Lt(4)]

    Pydantic will first perform its own internal validation and then check whether
    the field value is less than or equal to the argument passed to `Lt` (4 in the
    example above).

    It is up to the user to ensure that the field value and the argument of `Lt` can
    be compared.

    Parameters
    ----------
    value
       Value against which to compare.

    Returns
    -------
    A validator for checking a less than relation.
    """
    return AfterValidator(lambda v: _check_lt(v, value))


def Le(value: Any):
    """
    Return a Pydantic validator for checking a less than or equal to relation.

    The returned validator can be used in a type annotation::

        import pydantic

        class DummyModel(pydantic.BaseModel):
            height: Annotated[float, Le(4)]

    Pydantic will first perform its own internal validation and then check whether
    the field value is less than or equal to the argument passed to `Le` (4 in the
    example above).

    It is up to the user to ensure that the field value and the argument of `Le` can
    be compared.

    Parameters
    ----------
    value
       Value against which to compare.

    Returns
    -------
    A validator for checking a less than or equal to relation.
    """
    return AfterValidator(lambda v: _check_le(v, value))


def check_in_visibility_range(
    dec: astropy.coordinates.Angle,
) -> astropy.coordinates.Angle:
    if dec < -76 * u.deg or dec > 11 * u.deg:
        raise ValueError("Not in SALT's visibility range (between -76 and 11 degrees).")

    return dec
