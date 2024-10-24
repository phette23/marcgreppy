import sys
from typing import IO, BinaryIO, List, Union

import click
from pymarc import Any, MARCReader

from .color import color_field, color_record
from .filter import Filter


@click.command(help="Find MARC records matching patterns in a file.")
@click.help_option("-h", "--help")
@click.argument("files", type=click.File("rb"), nargs=-1)
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
@click.option(
    "--invert",
    help="Invert color scheme (for light terminal backgrounds)",
    is_flag=True,
)
@click.version_option(package_name="marcgrep", message="%(prog)s %(version)s")
def main(
    files: List[BinaryIO],
    color: bool,
    invert: bool,
    count: bool,
    include: list[str],
    exclude: list[str],
    fields: str,
    limit: int,
):
    # handle stdin if no files are provided
    if not files:
        files = [sys.stdin.buffer]

    if invert and not color:
        click.echo(
            "The --invert flag was passed without --color, it has no effect.", err=True
        )

    any_matches = False

    for file in files:
        counter = 0
        matched_records = 0
        reader = MARCReader(file)

        # build a list of filters, start with exclusive because they rule out records quicker
        filters: list[Filter] = [
            Filter(pattern, inclusive=False) for pattern in exclude
        ]
        filters.extend(Filter(pattern) for pattern in include)

        for record in reader:
            if record:
                counter += 1
                if all(f.match(record) for f in filters):
                    any_matches = True
                    matched_records += 1
                    if not count:
                        if fields:
                            for f in record.get_fields(*fields.split(",")):
                                if color:
                                    color_field(f, invert)
                                else:
                                    print(f)
                        else:
                            if color:
                                color_record(record, invert)
                            else:
                                print(record)
                if limit and counter >= limit:
                    break

        if count:
            print(f"{file.name}: {matched_records}")

    # non-zero exit if no records match
    return exit(0 if any_matches else 1)


if __name__ == "__main__":
    main()
