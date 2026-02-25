import pathlib

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
            pathlib.Path(__file__).parent.parent / "data" / "dummy_finder_chart_1.pdf"
        )
        finder_chart_2 = (
            pathlib.Path(__file__).parent.parent / "data" / "dummy_finder_chart_2.pdf"
        )
        mos_mask = (
            pathlib.Path(__file__).parent.parent / "data" / "dummy_rss_mos_mask.rsim"
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
            pathlib.Path(__file__).parent.parent / "data" / "dummy_finder_chart_1.pdf"
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
            pathlib.Path(__file__).parent.parent / "data" / "dummy_finder_chart_2.pdf"
        )
        mos_mask = finder_chart_1c  # as we are testing for duplicates
        request = base_request
        block = base_block
        rss = base_rss
        configuration = base_rss_multi_object_spectroscopy
        configuration.mask = mos_mask
        block.acquisition.finder_charts = [
            finder_chart_1a,
            finder_chart_2,
            finder_chart_1b,
        ]
        rss.configuration = configuration
        block.instrument = rss
        request.blocks = [block]

        assert request.attachments() == {
            finder_chart_1a.resolve(),
            finder_chart_2.resolve(),
        }
