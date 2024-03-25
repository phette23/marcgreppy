from importlib import metadata
from typing import BinaryIO

import click
from pymarc import MARCReader

from .utils import count_records


@click.command(help="Find MARC records matching patterns in a file.")
@click.help_option("-h", "--help")
@click.argument("file", type=click.File("rb"), default="-")
@click.option("--version", "-v", help="Show marcgrep version", is_flag=True)
@click.option("--count", "-c", help="Count matching records", is_flag=True)
def main(file: BinaryIO, count: bool, version: bool):
    if version:
        print(metadata.version("marcgrep"))

    reader = MARCReader(file)

    if count:
        num_records = count_records(reader)
        print(num_records)
        # non-zero exit if no records found
        exit(0 if num_records else 1)


if __name__ == "__main__":
    main()
