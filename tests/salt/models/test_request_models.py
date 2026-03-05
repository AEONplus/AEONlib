import io
import os.path
import pathlib
import zipfile
from copy import deepcopy

import pytest
from pydantic import ValidationError

from aeonlib.salt.models import Request


class TestRequest:
    def test_no_blocks(self):
        """Test that at least one block must be supplied."""
        with pytest.raises(ValidationError) as exc_info:
            Request(proposal_code="2025-1-SCI-042", semester="2026-1", blocks=[])
        assert exc_info.value.errors()[0]["loc"] == ("blocks",)
        assert exc_info.value.errors()[0]["type"] == "too_short"

    def test_no_attachments(
            self, base_request, base_block, base_rss, base_rss_longslit_spectroscopy
    ):
        """Test the case that the request includes no attachments."""
        request = base_request
        block = base_block
        rss = base_rss
        configuration = base_rss_longslit_spectroscopy
        block.acquisition.finder_charts = []
        rss.configuration = configuration
        block.instrument = rss
        request.blocks = [block]

        assert request.attachments() == set()

    def test_multiple_attachments(
            self, base_request, base_block, base_rss, base_rss_multi_object_spectroscopy
    ):
        """Test the case that the request includes multiple attachments."""
        finder_chart_1 = (
                pathlib.Path(
                    __file__).parent.parent / "data" / "dummy_finder_chart_1.pdf"
        )
        finder_chart_2 = (
                pathlib.Path(
                    __file__).parent.parent / "data" / "dummy_finder_chart_2.pdf"
        )
        mos_mask = (
                pathlib.Path(
                    __file__).parent.parent / "data" / "dummy_rss_mos_mask.rsmt"
        )
        request = base_request
        block = base_block
        rss = base_rss
        configuration = base_rss_multi_object_spectroscopy
        configuration.mask = mos_mask
        block.acquisition.finder_charts = [finder_chart_1, finder_chart_2]
        rss.configuration = configuration
        block.instrument = rss
        request.blocks = [block]

        assert request.attachments() == {
            finder_chart_1.resolve(),
            finder_chart_2.resolve(),
            mos_mask.resolve(),
        }

    def test_duplicate_attachments(
            self, base_request, base_block, base_rss, base_rss_multi_object_spectroscopy
    ):
        """Test the case that the request uses the same attachment multiple times."""
        # finder_chart_1a, finder_chart_1b and finder_chart_1c denote the sane file
        finder_chart_1a = (
                pathlib.Path(
                    __file__).parent.parent / "data" / "dummy_finder_chart_1.pdf"
        )
        finder_chart_1b = (
                pathlib.Path(__file__).parent.parent
                / "data/../data"
                / "dummy_finder_chart_1.pdf"
        )
        finder_chart_1c = (
                pathlib.Path(__file__).parent.parent
                / "data/../../salt/data"
                / "dummy_finder_chart_1.pdf"
        )
        finder_chart_2 = (
                pathlib.Path(
                    __file__).parent.parent / "data" / "dummy_finder_chart_2.pdf"
        )
        mos_mask = finder_chart_1c  # as we are testing for duplicates
        request = base_request
        block = base_block
        rss = base_rss
        configuration = base_rss_multi_object_spectroscopy
        configuration.mask = mos_mask
        rss.configuration = configuration
        block.instrument = rss

        block1 = block
        block2 = deepcopy(block1)

        block1.acquisition.finder_charts = [
            finder_chart_1a,
            finder_chart_2,
            finder_chart_1b,
        ]
        block2.acquisition.finder_charts = [
            finder_chart_1c,
            finder_chart_2,
        ]

        request.blocks = [block1, block2]

        assert request.attachments() == {
            finder_chart_1a.resolve(),
            finder_chart_2.resolve(),
        }

    def test_export(self, base_block, base_rss, base_rss_multi_object_spectroscopy):
        """Test that a correct zip file is generated."""

        # Set up the attachments.
        finder_chart_1 = (
                pathlib.Path(
                    __file__).parent.parent / "data" / "dummy_finder_chart_1.pdf"
        )
        finder_chart_2 = (
                pathlib.Path(
                    __file__).parent.parent / "data" / "dummy_finder_chart_3.png"
        )
        mos_file = (
                pathlib.Path(
                    __file__).parent.parent / "data" / "dummy_rss_mos_mask.rsmt"
        )

        # Store the attachment sizes.
        finder_chart_1_size = os.path.getsize(finder_chart_1)
        finder_chart_2_size = os.path.getsize(finder_chart_2)
        mos_file_size = os.path.getsize(mos_file)

        # Set up the first block.
        block1 = deepcopy(base_block)
        block1.acquisition.finder_charts = [finder_chart_1]
        base_rss_multi_object_spectroscopy.mask = mos_file
        base_rss.configuration = base_rss_multi_object_spectroscopy
        block1.instrument = base_rss

        # Set up the second block.
        block2 = deepcopy(base_block)
        block2.acquisition.finder_charts = [finder_chart_2]

        # Generate the zip file.
        request = Request(
            proposal_code="2026-1-SCI-042", semester="2026-1", blocks=[block1, block2]
        )
        zip_content = io.BytesIO()
        request.export(zip_content)

        # Check the content of the generated zip file.
        zip_content.seek(0)
        with zipfile.ZipFile(zip_content) as archive:
            block_submission = archive.read("BlockSubmission.xml").decode(
                encoding="utf-8"
            )
            for file in archive.namelist():
                if file != "BlockSubmission.xml":
                    assert file.startswith("Included/")
                    assert (
                            file.endswith(".pdf")
                            or file.endswith(".png")
                            or file.endswith(".rsmt")
                    )
                    assert file in block_submission

                    content = archive.read(file)
                    if file.endswith(".pdf"):
                        assert len(content) == finder_chart_1_size
                    elif file.endswith(".png"):
                        assert len(content) == finder_chart_2_size
                    elif file.endswith(".rsmt"):
                        assert len(content) == mos_file_size
