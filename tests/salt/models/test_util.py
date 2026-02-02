import pytest

from aeonlib.salt.models.serialize.util import validate_xml


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
