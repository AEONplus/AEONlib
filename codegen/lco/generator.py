#!/usr/bin/env python3
import fileinput
import json
import sys
from pathlib import Path

import textcase
from jinja2 import Environment, FileSystemLoader


def get_modes(ins: dict, type: str) -> list[str]:
    try:
        return [m["code"] for m in ins["modes"][type]["modes"]]
    except Exception:
        return []


def generate_instrument_configs(ins_s: str, soar: bool = False) -> str:
    """
    Generate instrument models based on the output of the OCS
    instrument data endpoint. For LCO, this endpoint resides
    at https://observe.lco.global/api/instruments/

    Args:
        ins_s (str): The input json containing instrument data.
        soar (bool): Whether to generate SOAR instruments.

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
    instruments = []
    if soar:
        prefix = ""
        filtered = {k: v for k, v in ins_data.items() if 'soar' in k.lower()}
    else:
        prefix = "Lco"
        filtered = {k: v for k, v in ins_data.items() if 'soar' not in k.lower()}

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
                    k[:-1]: v
                    for k, v in ins["optical_elements"].items()
                },
            }
        )

    return template.render(instruments=instruments, soar=soar)


if __name__ == "__main__":
    try:
        # soar = sys.argv[1] == 'soar'
        soar = sys.argv.pop(1) == 'soar'
    except IndexError:
        soar = False
    # Accepts input from stdin or a file argument
    with fileinput.input() as f:
        ins_json = "".join(list(f))
        sys.stdout.write(generate_instrument_configs(ins_json, soar=soar))
