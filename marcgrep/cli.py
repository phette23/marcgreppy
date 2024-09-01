from typing import BinaryIO

import click
from pymarc import MARCReader

from .color import color_field, color_record
from .filter import Filter


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
@click.option("--fields", "-f", help="Comma-separated list of fields to print")
@click.option("--limit", "-l", help="Limit number of records to process", type=int)
@click.option("--color", help="Colorize mnemonic MARC output", is_flag=True)
@click.version_option(package_name="marcgrep", message="%(prog)s %(version)s")
def main(
    file: BinaryIO,
    color: bool,
    count: bool,
    include: list[str],
    exclude: list[str],
    fields: str,
    limit: int,
):
    counter = 0
    matched_records = 0
    reader = MARCReader(file)

    # build a list of filters, start with exclusive because they rule out records quicker
    filters: list[Filter] = [Filter(pattern, inclusive=False) for pattern in exclude]
    filters.extend(Filter(pattern) for pattern in include)

    for record in reader:
        if record:
            counter += 1
            if all(f.match(record) for f in filters):
                matched_records += 1
                if not count:
                    if fields:
                        for f in record.get_fields(*fields.split(",")):
                            if color:
                                color_field(f)
                            else:
                                print(f)
                    else:
                        if color:
                            color_record(record)
                        else:
                            print(record)
            if limit and counter >= limit:
                break

    if count:
        print(matched_records)

    # non-zero exit if no records match
    return exit(0 if matched_records else 1)


if __name__ == "__main__":
    main()
