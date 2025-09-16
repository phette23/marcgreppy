import pytest

from marcgrep.filter import Filter, FilterFormatError, parse_pattern


@pytest.mark.parametrize(
    ["input", "expected"],
    [
        ("245", ("245", None, None, None, None)),
        ("245,cat in the hat", ("245", None, None, None, "cat in the hat")),
        ("245,4,0,a,cat in the hat", ("245", "4", "0", "a", "cat in the hat")),
        ("856,,,u,http://example.com", ("856", None, None, "u", "http://example.com")),
        (
            "505,,,,long string, with, commas",
            ("505", None, None, None, "long string, with, commas"),
        ),
    ],
)
def test_parse_pattern(input, expected):
    assert parse_pattern(input) == expected


@pytest.mark.parametrize(
    "input",
    [
        "",
        "1,field too short",
        "1000,field too long",
        "111,az,>1 char subfield",
        "111,10,a,>9 indicator",
        "111,z,a,letter indicator",
        "abc,letter field",
        "a12,another letter field",
    ],
)
def test_filter_validation_errors(input):
    with pytest.raises(FilterFormatError):
        Filter(input)
