from pathlib import Path

from pymarc import MARCReader
import pytest

from marcgrep.filter import Filter

with open(Path("test") / "fixtures" / "one_record.mrc", "rb") as fh:
    reader = MARCReader(fh)
    record = next(reader)


@pytest.mark.parametrize(
    "input, expected",
    [
        ("245", True),
        ("246", False),
        ("653,Netzwerke", True),
        ("653,Netz", True),
        ("653,a,Netz", True),
        ("653,Netzwerkestring that's not there", False),
        ("653,a,Netzwerkestring that's not there", False),
        # regex
        ("653,a,.*werke", True),
        ("653,a,^[0-9]+$", False),
        # match across multiple subfields
        ("506,Open Access.*Unrestricted online access", True),
        ("506,Open Access.*string that's not there", False),
        # test for subfield, empty value
        ("856,u,", True),
        ("856,y,", False),
        # indicators
        ("245,1,,,", True),
        ("245,1,0,,", True),
        ("245,2,0,,", False),
        ("245,1,2,,", False),
        ("245,1,,a,Kulturpolitik", True),
        ("245,1,0,,Kulturpolitik", True),
        ("245,2,0,,Kulturpolitik", False),
        ("245,1,2,,Kulturpolitik", False),
        # curly braces in value https://github.com/phette23/marcgreppy/issues/1
        ("653,a,curly", True),
    ],
)
def test_single_inclusive_filter_matches(input, expected):
    f = Filter(input)
    assert record is not None
    assert f.match(record) == expected


@pytest.mark.parametrize(
    "input,expected",
    [
        ("245,1,,a,Kulturpolitik", False),
        ("245,1,0,,Kulturpolitik", False),
        ("245,2,0,,Kulturpolitik", True),
        ("245,1,2,,Kulturpolitik", True),
        ("245,.*politik", False),
        ("245,.*string that's not there", True),
        ("653,a,.*werke", False),
        # indicators
        ("245,1,,,", False),
        ("245,1,0,,", False),
        ("245,2,0,,", True),
        ("245,1,2,,", True),
    ],
)
def test_single_exclusive_filter_matches(input, expected):
    f = Filter(input, inclusive=False)
    assert record is not None
    assert f.match(record) == expected
