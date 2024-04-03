import math
from typing import BinaryIO, Literal

import click
from pymarc import MARCReader

from .filter import Filter
from .utils import count_records


@click.command(help="Find MARC records matching patterns in a file.")
@click.help_option("-h", "--help")
@click.argument("file", type=click.File("rb"), default="-")
@click.option("--count", "-c", help="Count matching records", is_flag=True)
@click.option(
    "--include", "-i", help="Include matching records (repeatable)", multiple=True
)
@click.option(
    "--exclude", "-e", help="Exclude matching records (repeatable)", multiple=True
)
@click.option("--limit", "-l", help="Limit number of records to process", type=int)
@click.version_option(package_name="marcgrep", message="%(prog)s %(version)s")
def main(
    file: BinaryIO,
    count: bool,
    include: list[str],
    exclude: list[str],
    limit: int,
):
    counter = 0
    matched_records = 0
    reader = MARCReader(file)

    # build a list of filters, start with exclusive because they rule out records quicker
    filters = [Filter(pattern, inclusive=False) for pattern in exclude]
    filters.extend(Filter(pattern) for pattern in include)

    # if no filters, count or print all records
    if not len(filters):
        if count:
            matched_records = count_records(reader)
            print(matched_records)
            # non-zero exit if no records found
            return exit(0 if matched_records else 1)
        for record in reader:
            print(record)
        return exit(0)

    for record in reader:
        if record:
            counter += 1
            if all(f.match(record) for f in filters):
                matched_records += 1
                if not count:
                    print(record)
            if limit and counter >= limit:
                break

    if count:
        print(matched_records)

    # non-zero exit if no records match
    return exit(0 if matched_records else 1)


if __name__ == "__main__":
    main()
