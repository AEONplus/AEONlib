from typing import Literal

from pydantic import PlainSerializer

SalticamFilter = Literal[
    "Fused silica clear",
    "fused silica clear",
    "Johnson U",
    "johnson u",
    "Johnson B",
    "johnson b",
    "Johnson V",
    "johnson v",
    "Cousins R",
    "cousins r",
    "Cousins I",
    "cousins i",
    "380nm 40nm FWHM",
    "380nm 40nm fwhm",
    "SDSS u'",
    "sdss u'",
    "SDSS g'",
    "sdss g'",
    "SDSS r'",
    "sdss r'",
    "SDSS i'",
    "sdss i'",
    "SDSS z'",
    "sdss z'",
    "H-alpha",
    "h-alpha",
    "H-beta narrow",
    "h-beta narrow",
    "H-beta wide",
    "h-beta wide",
    "Stroemgren u",
    "stroemgren u",
    "Stroemgren v",
    "stroemgren v",
    "Stroemgren b",
    "stroemgren b",
    "Stroemgren y",
    "stroemgren y",
    "SRE 1",
    "sre 1",
    "SRE 2",
    "sre 2",
    "SRE 3",
    "sre 3",
    "SRE 4",
    "sre 4",
]
"""A filter for Salticam."""


def serialize_salticam_filter(value: str) -> str:
    value = value.lower()
    translation_table = {
        "fused silica clear": "Fused silica clear",
        "johnson u": "Johnson U",
        "johnson b": "Johnson B",
        "johnson v": "Johnson V",
        "cousins r": "Cousins R",
        "cousins i": "Cousins I",
        "380nm 40nm fwhm": "380nm 40nm FWHM",
        "sdss u'": "SDSS u'",
        "sdss g'": "SDSS g'",
        "sdss r'": "SDSS r'",
        "sdss i'": "SDSS i'",
        "sdss z'": "SDSS z'",
        "h-alpha": "H-alpha",
        "h-beta narrow": "H-beta narrow",
        "h-beta wide": "H-beta wide",
        "stroemgren u": "Stroemgren u",
        "stroemgren v": "Stroemgren v",
        "stroemgren b": "Stroemgren b",
        "stroemgren y": "Stroemgren y",
        "sre 1": "SRE 1",
        "sre 2": "SRE 2",
        "sre 3": "SRE 3",
        "sre 4": "SRE 4",
    }
    serialized = translation_table.get(value)
    if serialized is None:
        raise ValueError(f"Filter name cannot be serialized: {value}")
    return serialized


SalticamFilterSerializer = PlainSerializer(serialize_salticam_filter)
