"""This module provides Pydantic models for SALT observation requests."""

from typing import Annotated

from annotated_types import MinLen
from pydantic import BaseModel


class Request(BaseModel, validate_assignment=True):
    """
    An observation request for SALT.

    Parameters
    ----------
    proposal_code
        Unique identifier of the proposal for which this request is submitted.
    blocks
        List of blocks to observe.

    """

    proposal_code: str

    blocks: Annotated[list, MinLen(1)]
