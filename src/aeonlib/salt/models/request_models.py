"""This module provides Pydantic models for SALT observation requests."""

import os
import pathlib
import zipfile
from typing import Annotated, BinaryIO

from annotated_types import MinLen
from pydantic import BaseModel, Field

from aeonlib.salt.models.util import (
    render_template,
    attachment_path_replacements,
    replace_attachment_paths,
)


class Request(BaseModel, validate_assignment=True):  # type: ignore
    """
    An observation request for SALT.

    A request is made up of a proposal code, which must be the proposal code of a
    proposal existing already, the semester for which the request is submitted and a
    non-empty list of blocks.

    The semester must be of the form yyyy-s with the year yyyy and its semester (1 or
    2). Semester 1 runs from 1 May to 1 November, semester 2 from November to May (in
    the following year). For example, semester 2026-1 runs from noon on 1 May 2026 to
    noon on 1 November 2026, whereas semester 2026-2 runs from noon on 1 November 2026
    to noon on 1 May 2027.

    Parameters
    ----------
    proposal_code
        Unique identifier of the proposal for which this request is submitted.
    semester
        Semester for which the submission is intended, in the form yyyy-s, where yyyy
        denotes the year and s can be 1 or 2. Examples are 2025-1 or 2026-2.
    blocks
        List of blocks to observe.

    """

    proposal_code: str

    semester: str = Field(pattern=r"\d{4}-[12]")

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

    def export(self, out: pathlib.Path | os.PathLike | str | BinaryIO) -> None:
        """
        Export this request as a zip file.

        Parameters
        ----------
        out
            Path of the zip file or a byte stream.
        """
        with zipfile.ZipFile(out, "w") as archive:
            block_submission_xml = render_template(
                "block_submission.xml", request=self.model_dump()
            )
            attachments = self.attachments()
            replacements = attachment_path_replacements(attachments)
            block_submission_xml = replace_attachment_paths(
                block_submission_xml, replacements
            )
            archive.writestr("BlockSubmission.xml", block_submission_xml)
            for path, zip_path in replacements.items():
                archive.write(path, zip_path)
