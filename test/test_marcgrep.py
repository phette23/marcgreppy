from io import BufferedReader
from pathlib import Path

from pymarc import MARCReader
import pytest

from marcgrep.utils import count_records


# helper method since our functions expect a MARCReader
def reader_from_fixture(file: str) -> tuple[MARCReader, BufferedReader]:
    fh = open(Path("test") / "fixtures" / file, "rb")
    return MARCReader(fh), fh


@pytest.mark.parametrize(
    "input, expected",
    [
        ("plain.txt", 0),
        ("OAPEN.mrc", 500),
    ],
)
def test_count(input, expected):
    reader, fh = reader_from_fixture(input)
    assert count_records(reader) == expected
    fh.close()
