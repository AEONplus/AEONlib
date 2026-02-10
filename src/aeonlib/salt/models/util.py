import io
import pathlib
from typing import Any

import astropy.units as u
from astropy.coordinates import Angle
from jinja2 import Environment, PackageLoader, select_autoescape, BaseLoader
from lxml import etree
from pydantic import PlainSerializer, BeforeValidator

_schema: etree.XMLSchema | None = None


LINEAR_POLARIMETRY_PATTERN = [
    (Angle(0 * u.deg), None),
    (Angle(45 * u.deg), None),
    (Angle(22.5 * u.deg), None),
    (Angle(67.5 * u.deg), None),
]
# The half and quarter wave plate angles for the linear polarimetry pattern.


LINEAR_HI_POLARIMETRY_PATTERN = [
    (Angle(0 * u.deg), None),
    (Angle(45 * u.deg), None),
    (Angle(22.5 * u.deg), None),
    (Angle(67.5 * u.deg), None),
    (Angle(11.25 * u.deg), None),
    (Angle(56.25 * u.deg), None),
    (Angle(33.75 * u.deg), None),
    (Angle(78.75 * u.deg), None),
]
# The half and quarter wave plate angles for the linear-hi polarimetry pattern.


CIRCULAR_POLARIMETRY_PATTERN = [
    (Angle(0 * u.deg), Angle(45 * u.deg)),
    (Angle(0 * u.deg), Angle(315 * u.deg)),
]
# The half and quarter wave plate angles for the circular polarimetry pattern.


CIRCULAR_HI_POLARIMETRY_PATTRERN = [
    (Angle(0 * u.deg), Angle(45 * u.deg)),
    (Angle(0 * u.deg), Angle(315 * u.deg)),
    (Angle(22.5 * u.deg), Angle(315 * u.deg)),
    (Angle(22.5 * u.deg), Angle(45 * u.deg)),
    (Angle(45 * u.deg), Angle(45 * u.deg)),
    (Angle(45 * u.deg), Angle(315 * u.deg)),
    (Angle(67.5 * u.deg), Angle(315 * u.deg)),
    (Angle(67.5 * u.deg), Angle(45 * u.deg)),
]
# The half and quarter wave plate angles for the circular-hi polarimetry pattern.


ALL_STOKES_POLARIMETRY_PATTERN = [
    (Angle(0 * u.deg), Angle(0 * u.deg)),
    (Angle(45 * u.deg), Angle(0 * u.deg)),
    (Angle(22.5 * u.deg), Angle(0 * u.deg)),
    (Angle(67.5 * u.deg), Angle(0 * u.deg)),
    (Angle(0 * u.deg), Angle(45 * u.deg)),
    (Angle(0 * u.deg), Angle(315 * u.deg)),
]
# The half and quarter wave plate angles for the all-Stokes polarimetry pattern.


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


def _wave_plate_station(angle):
    if angle < 1e-5:
        return "0_0"
    else:
        return f"{(angle / 11.25):.0f}_{angle:.2f}"


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
    env.filters["wave_plate_station"] = _wave_plate_station
    template = env.get_template(template_path)
    return template.render(**kwargs)


def _lower(s: Any) -> Any:
    if isinstance(s, str):
        return s.lower()
    return s


LowerCaseValidator = BeforeValidator(_lower)


def _capitalize(s: str | None) -> str | None:
    if s is None:
        return None
    return s.capitalize()


CapitalizingSerializer = PlainSerializer(_capitalize)
"""
A serializer for capitalising string values.

This serializer is only intended for use in the serialization of SALT data models.
"""


def _title(s: str | None) -> str | None:
    if s is None:
        return None
    return s.title()


TitleCaseSerializer = PlainSerializer(_title)
"""
A serializer for converting string values to title case.

This serializer is only intended for use in the serialization of SALT data models.
"""


def _upper(s: str | None) -> str | None:
    if s is None:
        return None
    return s.upper()


UpperCaseSerializer = PlainSerializer(_upper)
"""
A serializer for converting string values to upper case.

This serializer is only intended for use in the serialization of SALT data models.
"""
