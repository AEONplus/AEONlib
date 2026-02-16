import pathlib
import re

import pytest
from jinja2 import FileSystemLoader

from aeonlib.salt.models.util import (
    validate_xml,
    render_template,
    replace_attachment_paths,
)


def test_validate_non_well_formed_xml():
    """Test that an error is raised when you validate XML which is not well-formed."""
    xml = "<foo></bar>"
    with pytest.raises(ValueError):
        validate_xml(xml)


def test_validate_invalid_xml():
    """
    Test that an error is raised when you validate XNL which does not conform to the
    schema.
    """
    xml = """
    <AngularSpeed>
        <Value>A</Value>
        <Units>arcseconds/year</Units>
    </AngularSpeed>
    """
    with pytest.raises(ValueError):
        validate_xml(xml)


def test_validate_valid_xml():
    """Test that valid XML passes validation."""
    xml = """
    <AngularSpeed>
        <Value>4.56</Value>
        <Units>arcseconds/year</Units>
    </AngularSpeed>
    """
    validate_xml(xml)
    assert True


def test_render_template():
    """Test rendering a Jinja template."""
    loader = FileSystemLoader(pathlib.Path(__file__).parent.parent.parent / "data")
    rendered = render_template("test.xml", loader, a=1, b=2)
    assert "<a>1</a>" in rendered
    assert "<b>2</b>" in rendered


def test_render_template_with_escaping():
    """Test that input is escaped when rendering a Jinja template."""
    loader = FileSystemLoader(pathlib.Path(__file__).parent.parent.parent / "data")
    rendered = render_template("test.xml", loader, a="a >= 1 & a <= 5", b=2)
    assert "<a>a &gt;= 1 &amp; a &lt;= 5</a>" in rendered


def test_replace_attachment_paths(
        base_request, base_block, base_rss, base_rss_multi_object_spectroscopy
):
    """Test replacing attachment paths."""
    # finder_chart deliberately includes ".." to test resolution.
    finder_chart = (
            pathlib.Path(__file__).parent.parent.parent
            / "data/../data"
            / "dummy_finder_chart_1.pdf"
    )
    mos_mask = (
            pathlib.Path(
                __file__).parent.parent.parent / "data" / "dummy_rss_mos_mask.rsim"
    )
    request = base_request
    block = base_block
    rss = base_rss
    configuration = base_rss_multi_object_spectroscopy
    configuration.mask = mos_mask
    block.acquisition.finder_charts = [finder_chart]
    rss.configuration = configuration
    block.instrument = rss
    request.blocks = [block]

    xml = render_template("blocks.xml", blocks=request.model_dump()["blocks"])

    replacements = {
        finder_chart.resolve(): "Included/FinderChart.pdf",
        mos_mask.resolve(): "Included/MOS.rsmt",
    }

    updated_xml = replace_attachment_paths(xml, replacements)

    assert re.search(r"<Path>\s*Included/FinderChart.pdf\s*</Path>", updated_xml)
    assert re.search(r"<Path>\s*Included/MOS.rsmt\s*</Path>", updated_xml)


def test_missing_replacement(base_request, base_block):
    """Test that an error is raised if an attachment path replacement is missing."""
    finder_chart = (
            pathlib.Path(
                __file__).parent.parent.parent / "data" / "dummy_finder_chart_1.pdf"
    )
    request = base_request
    block = base_block
    block.acquisition.finder_charts = [finder_chart]
    request.blocks = [block]

    xml = render_template("blocks.xml", blocks=request.model_dump()["blocks"])
    with pytest.raises(ValueError, match="Path missing"):
        replace_attachment_paths(xml, {})


def test_duplicate_replacement_key(base_request):
    """
    Test that an error is raised if there is a duplicate key in the dictionary of
    replacements.
    """
    # file_1a and file_1b are the same file
    file_1a = (
            pathlib.Path(
                __file__).parent.parent.parent / "data" / "dummy_finder_chart_1.pdf"
    )
    file_1b = (
            pathlib.Path(__file__).parent.parent.parent
            / "data/../data"
            / "dummy_finder_chart_1.pdf"
    )

    request = base_request

    xml = render_template("blocks.xml", blocks=request.model_dump()["blocks"])

    replacements = {file_1a: "Included/File_1a.pdf", file_1b: "Included/File_1b.pdf"}

    with pytest.raises(ValueError, match="same path"):
        replace_attachment_paths(xml, replacements)


def test_duplicate_replacement_value(base_request):
    """
    Test that an error is raised if there is a duplicate value in the dictionary of
    replacements.
    """
    file_1 = (
            pathlib.Path(
                __file__).parent.parent.parent / "data" / "dummy_finder_chart_1.pdf"
    )
    file_2 = (
            pathlib.Path(__file__).parent.parent.parent
            / "data"
            / "dummy_finder_chart_2.pdf"
    )

    request = base_request

    xml = render_template("blocks.xml", blocks=request.model_dump()["blocks"])

    replacements = {file_1: "Included/File.pdf", file_2: "Included/File.pdf"}

    with pytest.raises(ValueError, match="duplicate value"):
        replace_attachment_paths(xml, replacements)
