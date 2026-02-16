import datetime
import io
import pathlib
import uuid
import zoneinfo
from typing import Any

import astropy.units as u
from astropy.coordinates import Angle
from bs4 import BeautifulSoup
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
        xml_doc = etree.parse(io.BytesIO(xml.encode("utf-8")))
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


def _iodine_cell_position(value):
    return value if value else "OUT"


def _nirwals_articulation_station(angle):
    if angle < 1e-5:
        return "0_0"
    else:
        return f"{(2 * angle):.0f}_{angle:.1f}"


def _year_as_iso_timestamp(year):
    t = datetime.datetime(year, 1, 1, 0, 0, 0, 0, tzinfo=zoneinfo.ZoneInfo("UTC"))
    return t.isoformat()


def _sign(value):
    return "+" if value >= 0 else "-"


def _uuid() -> str:
    return str(uuid.uuid4())


def _to_angle(degrees: float) -> Angle:
    return Angle(degrees * u.deg)


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
    env.trim_blocks = True
    env.lstrip_blocks = True
    env.filters["wave_plate_station"] = _wave_plate_station
    env.filters["iodine_cell_position"] = _iodine_cell_position
    env.filters["nirwals_articulation_station"] = _nirwals_articulation_station
    env.filters["year_as_iso_timestamp"] = _year_as_iso_timestamp
    env.filters["sign"] = _sign
    env.globals["uuid"] = _uuid
    env.globals["to_angle"] = _to_angle
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


def replace_attachment_paths(xml: str, replacements: dict[pathlib.Path, str]) -> str:
    """
    Replace the attachment paths in the given XML.

    Parameters
    ----------
    xml
        XML.
    replacements
        Dictionary of attachment paths and their replacements.

    Returns
    -------
    The XML with the attachment paths updated.

    Raises
    ------
    ValueError
        If an attachment is missing in the dictionary of replacements.
    """

    # Resolve all attachment paths
    replacements_resolved = {k.resolve(): v for k, v in replacements.items()}

    # Check whether there are duplicate keys or values
    if len(set(replacements_resolved.keys())) != len(replacements):
        raise ValueError(
            "Two or more keys of the replacements dictionary resolve to the same path."
        )
    if len(set(replacements_resolved.values())) != len(replacements_resolved.values()):
        raise ValueError("There duplicate values in the replacements dictionary.")

    # Replace the attachment paths
    soup = BeautifulSoup(xml, "xml")
    for path_element in soup.find_all("Path"):
        path_text = path_element.text.strip()
        path = pathlib.Path(path_text).resolve()
        if path not in replacements_resolved:
            raise ValueError(
                f"Path missing in replacements dictionary: {path_text} (resolved: {str(path)}"
            )
        path_element.string = replacements_resolved[path]

    return soup.prettify()
