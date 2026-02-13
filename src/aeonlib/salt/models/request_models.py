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

    def attachments(self) -> set[pathlib.Path]:
        """
        Return the set of attachments for this request.

        All the attachment paths are reso,lved using the `resolve` method of the
        `pathlib.Path` class.

        Returns
        -------
        The set of attachments.
        """
        _attachments: set[pathlib.Path] = set()

        for block in self.blocks:
            for finder_chart in block.acquisition.finder_charts:
                if not isinstance(finder_chart, pathlib.Path):
                    raise ValueError("The finder chart value is not a Path instance.")
                _attachments.add(finder_chart)

            if block.instrument.instrument_name == "RSS":
                if hasattr(block.instrument.configuration, "mask"):
                    mask = block.instrument.configuration.mask
                    if not isinstance(mask, pathlib.Path):
                        raise ValueError("The mask value is not a Path instance.")
                    _attachments.add(mask)

        # Remove duplicates
        return set(a.resolve() for a in _attachments)
