#!/usr/bin/env python3
import fileinput
import json
import sys
from pathlib import Path
from typing import Any

import textcase
from jinja2 import Environment, FileSystemLoader

VALID_FACILITIES = ["SOAR", "LCO", "SAAO", "BLANCO"]


def get_extra_params_fields(extra_params_validation_schema: dict) -> dict:
    """Loops over the "extra_params" section of a validation_schema dict and creates a dictionary of
    field to aeonlib field_class to place into the template
    """
    fields = {}
    for field, properties in extra_params_validation_schema.items():
        field_class = ""
        # If a set of allowed values is present, use that to make a Literal unless this is a boolean variable
        if "allowed" in properties and properties.get("type") != "boolean":
            allowed_values = [
                f'"{val}"' if properties["type"] == "string" else val
                for val in properties["allowed"]
            ]
            field_class += f"Literal[{', '.join(allowed_values)}]"
        else:
            # Otherwise form an Annotated field based on its datatype, with min/max validation if present
            field_class += "Annotated["
            match properties["type"]:
                case "string":
                    field_class += "str"
                case "integer":
                    field_class += "int"
                case "float":
                    field_class += "float"
                case "boolean":
                    field_class += "bool"
            if "min" in properties:
                field_class += f", Ge({properties['min']})"
            if "max" in properties:
                field_class += f", Le({properties['max']})"
            # Add description to Annotated field. Annotated fields must have at least 2 properties.
            field_class += f', "{properties.get("description", "")}"]'
        if not properties.get("required", False) and "default" not in properties:
            # The field is considered optional if it doesn't have a default or required is not set to True
            field_class += " | None = None"
        elif "default" in properties:
            # If a default value is present, provide it
            default = (
                f'"{properties["default"]}"'
                if properties["type"] == "string"
                else properties["default"]
            )
            field_class += f" = {default}"
        fields[field] = field_class
    return fields


def get_modes(ins: dict[str, Any], type: str) -> list[str]:
    try:
        return [m["code"] for m in ins["modes"][type]["modes"]]
    except Exception:
        return []


def generate_instrument_configs(ins_s: str, facility: str) -> str:
    """
    Generate instrument models based on the output of the OCS
    instrument data endpoint. For LCO, this endpoint resides
    at https://observe.lco.global/api/instruments/

    Args:
        ins_s (str): The input json containing instrument data.
        facility (str): Which facility to generate instruments for.

    Returns:
        str: Generated Python Pydantic models as a string.
    """

    j_env = Environment(
        loader=FileSystemLoader(Path(__file__).parent / "templates"),
        trim_blocks=True,
        lstrip_blocks=True,
    )
    template = j_env.get_template("instruments.jinja")
    ins_data = json.loads(ins_s)
    instruments: list[dict[str, Any]] = []
    if facility == "SOAR":
        # Soar instruments look like SoarGhtsBluecam, already prefixed, so no need to add a prefix.
        prefix = ""
        filtered = {k: v for k, v in ins_data.items() if "soar" in k.lower()}
    elif facility == "BLANCO":
        # Blanco instrument(s) look like BLANCO_NEWFIRM
        prefix = ""
        filtered = {k: v for k, v in ins_data.items() if "blanco" in k.lower()}
    elif facility == "LCO":
        # We add a prefix for LCO because some instruments start with a number,
        # which is not allowed in Python class names. For example: Lco0M4ScicamQhy600
        prefix = "Lco"
        filtered = {
            k: v
            for k, v in ins_data.items()
            if "soar" not in k.lower() and "blanco" not in k.lower()
        }
    elif facility == "SAAO":
        # SAAO config doesn't share any instruments with other facilities so we don't need
        # to filter it
        prefix = "SAAO"
        filtered = ins_data
    else:
        raise ValueError(f"Invalid facility. Must be one of {VALID_FACILITIES}")

    # Instruments endpoint seems inconsistent, this should keep our output consistent
    ordered = dict(sorted(filtered.items()))
    for instrument_type, ins in ordered.items():
        instruments.append(
            {
                "instrument_type": instrument_type,
                "class_name": f"{prefix}{textcase.pascal(instrument_type)}",
                "config_types": [
                    c["code"] for c in ins["configuration_types"].values()
                ],
                "readout_modes": get_modes(ins, "readout"),
                "acquisition_modes": get_modes(ins, "acquisition"),
                "guiding_modes": get_modes(ins, "guiding"),
                "rotator_modes": get_modes(ins, "rotator"),
                "optical_elements": {
                    # This gets rid of the silly trailing s on "filters" and "narrowband_g_positions"
                    k.rstrip("s"): v
                    for k, v in ins["optical_elements"].items()
                },
                "configuration_extra_params": get_extra_params_fields(
                    ins.get("validation_schema", {})
                    .get("extra_params", {})
                    .get("schema", {})
                ),
                "instrument_config_extra_params": get_extra_params_fields(
                    ins.get("validation_schema", {})
                    .get("instrument_configs", {})
                    .get("schema", {})
                    .get("schema", {})
                    .get("extra_params", {})
                    .get("schema", {})
                ),
            }
        )

    return template.render(instruments=instruments, facility=facility)


if __name__ == "__main__":
    try:
        facility = sys.argv.pop(1)
        # Accepts input from stdin or a file argument
        with fileinput.input() as f:
            ins_json = "".join(list(f))
            _ = sys.stdout.write(
                generate_instrument_configs(ins_json, facility=facility)
            )
    except IndexError:
        _ = sys.stdout.write("Usage: python generator.py <facility>")
        exit(1)
