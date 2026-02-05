import io
import pathlib
from typing import Any

from jinja2 import Environment, PackageLoader, select_autoescape, BaseLoader
from lxml import etree
from pydantic import PlainSerializer, BeforeValidator

_schema: etree.XMLSchema | None = None


def validate_xml(xml: str) -> None:
    """
    Validate an XML string against the SALT XML schema.

    The method raises a `ValueError` if the XML is not well-formed or does not conform
    to the schema.

    This method is intended only for use in the serialization of SALT model instances.

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


def render_template(
    template_path: str, loader: BaseLoader | None = None, **kwargs
) -> str:
    """
    Render a Jinja template.

    The first argument for this method is the path of the template to render,
    as needed by the template loader. You may pass a `jinja2.BaseLoader` as the
    `loader` argument for specifying how to load the template. The default is to look
    in the `templates` folder of  the `aeonlib.salt.models.serialize` package. Any
    additional keyword arguments are passed on to Jinja's render function.

    This method is intended only for use in the serialization of SALT model instances.

    Parameters
    ----------
    template_path
        Path of the template to render.
    loader
        Jinja template loader.
    kwargs
        Additional keyword arguments passed on to the render function.

    Returns
    -------
    The rendered template.
    """
    if not loader:
        loader = PackageLoader("aeonlib.salt.models.serialize")

    env = Environment(loader=loader, autoescape=select_autoescape())
    template = env.get_template(template_path)
    return template.render(**kwargs)


def _lower(s: Any) -> Any:
    if isinstance(s, str):
        return s.lower()
    return s


LowerCaseValidator = BeforeValidator(_lower)


def _capitalize(s: str) -> str:
    return s.capitalize()


CapitalizingSerializer = PlainSerializer(_capitalize)
"""
A serializer for capitalising string values.

This serializer is only intended for use in the serialization of SALT data models.
"""


def _title(s: str) -> str:
    return s.title()


TitleCaseSerializer = PlainSerializer(_title)
"""
A serializer for converting string values to title case.

This serializer is only intended for use in the serialization of SALT data models.
"""


def _upper(s: str) -> str:
    return s.upper()


UpperCaseSerializer = PlainSerializer(_upper)
"""
A serializer for converting string values to upper case.

This serializer is only intended for use in the serialization of SALT data models.
"""
