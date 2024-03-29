from importlib import metadata
from typing import BinaryIO

import click
from pymarc import MARCReader

from .filter import Filter
from .utils import count_records


@click.command(help="Find MARC records matching patterns in a file.")
@click.help_option("-h", "--help")
@click.argument("file", type=click.File("rb"), default="-")
@click.option("--version", "-v", help="Show marcgrep version", is_flag=True)
@click.option("--count", "-c", help="Count matching records", is_flag=True)
@click.option("--include", "-i", help="Include matching records", multiple=True)
@click.option("--exclude", "-e", help="Exclude matching records", multiple=True)
def main(
    file: BinaryIO,
    count: bool,
    version: bool,
    include: list[str],
    exclude: list[str],
):
    if version:
        print(metadata.version("marcgrep"))
        return exit(0)

    num_records = 0
    reader = MARCReader(file)

    # build a list of filters, start with exclusive because they rule out records quicker
    filters = [Filter(pattern, inclusive=False) for pattern in exclude]
    filters.extend(Filter(pattern) for pattern in include)

    # if no filters, count or print all records
    if not len(filters):
        if count:
            num_records = count_records(reader)
            print(num_records)
            # non-zero exit if no records found
            return exit(0 if num_records else 1)
        for record in reader:
            print(record)
        return exit(0)

    for record in reader:
        if record:
            if all(f.match(record) for f in filters):
                num_records += 1
                if not count:
                    print(record)

    if count:
        print(num_records)

    # non-zero exit if no records match
    return exit(0 if num_records else 1)


if __name__ == "__main__":
    main()
