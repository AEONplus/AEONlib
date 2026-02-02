import pathlib

import pytest
from jinja2 import FileSystemLoader

from aeonlib.salt.models.serialize.util import validate_xml, render_template


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
    loader = FileSystemLoader(pathlib.Path(__file__).parent.parent / "data")
    rendered = render_template("test.xml", loader, a=1, b=2)
    assert "<a>1</a>" in rendered
    assert "<b>2</b>" in rendered


def test_render_template_with_escaping():
    """Test that input is escaped when rendering a Jinja template."""
    loader = FileSystemLoader(pathlib.Path(__file__).parent.parent / "data")
    rendered = render_template("test.xml", loader, a="a >= 1 & a <= 5", b=2)
    assert "<a>a &gt;= 1 &amp; a &lt;= 5</a>" in rendered
