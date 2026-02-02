import io
import pathlib

from lxml import etree

_schema: etree.XMLSchema | None = None


def validate_xml(xml: str) -> None:
    """
    Validate an XML string against the SALT XML schema.

    The method raises a `ValueError` if the XML is not well-formed or does not conform
    to the schema.

    Parameters
    ----------
    xml
        XML string.

    Raises
    ------
    ValueError
        If the XML is not well-formed or does not conform to the schema.

    """
    if not _schema:
        _load_schema()

    try:
        xml_doc = etree.parse(io.StringIO(xml))
        _schema.assertValid(xml_doc)
    except (etree.DocumentInvalid, etree.XMLSyntaxError) as e:
        raise ValueError(str(e))


def _load_schema():
    with open(pathlib.Path(__file__).parent / "proposal.xsd", "r") as f:
        schema_doc = etree.parse(f)
        global _schema
        _schema = etree.XMLSchema(schema_doc)
