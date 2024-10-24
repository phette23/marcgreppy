from os import environ
from typing import get_args

from pymarc import Field, Record
from termcolor import cprint
from termcolor._types import Color


def env_get(key: str, default: str) -> str:
    return environ.get(f"MARC_{key}") or default


COLOR_DARK_DEFAULTS: dict[str, Color] = {
    "TAG": "cyan",
    "INDICATOR": "light_yellow",
    "SUBFIELD": "green",
    "DATA": "white",
}
COLOR_LIGHT_DEFAULTS: dict[str, Color] = {
    "TAG": "blue",
    "INDICATOR": "dark_grey",
    "SUBFIELD": "magenta",
    "DATA": "black",
}
DELIMITER: str = env_get("DELIMITER", "‡")
EMPTY_INDICATOR: str = env_get("EMPTY_INDICATOR", "_")


def _set_color_env(token: str, invert: bool) -> str:
    var = f"{token}_COLOR"
    # validate that termcolor supports the color
    try:
        assert environ.get(f"MARC_{var}", "black") in get_args(Color)
    except AssertionError:
        raise ValueError(
            f'Invalid color "{environ.get(f"MARC_{var}")}" for MARC_{var}. '
            f"Valid colors are {get_args(Color)}."
        )
    if invert:
        return env_get(var, COLOR_LIGHT_DEFAULTS[token])
    return env_get(var, COLOR_DARK_DEFAULTS[token])


def _setup_colors(invert: bool):
    """Create COLORS global dict from env vars and invert flag

    Args:
        invert (bool): default to light color scheme
    """
    global COLORS
    COLORS = {}
    for token in ["TAG", "INDICATOR", "SUBFIELD", "DATA"]:
        COLORS[token] = _set_color_env(token, invert)


def color_field(field: Field, invert: bool) -> None:
    # create COLORS global if we have not already
    if not globals().get("COLOR"):
        _setup_colors(invert)

    # control fields have neither indicators nor subfields
    if field.is_control_field():
        cprint(f"{field.tag}", COLORS["TAG"], end=" ")
        cprint(f"{field.value()}", COLORS["DATA"], end="")
    else:
        cprint(f"{field.tag}", COLORS["TAG"], end=" ")
        cprint(
            f"{field.indicator1 if field.indicator1 != ' ' else EMPTY_INDICATOR}{field.indicator2 if field.indicator2 != ' ' else EMPTY_INDICATOR}",
            COLORS["INDICATOR"],
            end=" ",
        )
        for subfield in field.subfields:
            cprint(f"{DELIMITER}{subfield.code}", COLORS["SUBFIELD"], end="")
            cprint(f"{subfield.value}", COLORS["DATA"], end="")
    print()


def color_record(record: Record, invert: bool) -> None:
    for field in record:
        color_field(field, invert)
    print()
