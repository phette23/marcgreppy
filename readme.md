# marcgrep ![PyPI](https://img.shields.io/pypi/v/marcgrep)

A CLI for searching MARC files like [MARCgrep.pl](https://pusc.it/bib/MARCgrep) but in Python and a bit different syntax.

[marcli](https://github.com/hectorcorrea/marcli) is also a similar project that's faster but a little less flexible.

## Installation

Python 3.9 or later.

```sh
pipx install marcgrep # install globally with pipx
pip install marcgrep # or use pip/pip3
```

## Usage

```sh
# general command format - pass one or more files or pipe stdin
marcgrep OPTIONS FILE1.mrc FILE2.mrc
cat FILE.mrc | marcgrep OPTIONS
# full usage information
Usage: marcgrep [OPTIONS] [FILES]...

  Find MARC records matching patterns in a file.

Options:
  -h, --help           Show this message and exit.
  -c, --count          Count matching records
  -i, --include TEXT   Include matching records (repeatable)
  -e, --exclude TEXT   Exclude matching records (repeatable)
  -f, --fields TEXT    Comma-separated list of fields to print
  -l, --limit INTEGER  Limit number of records to process
  --color              Colorize mnemonic MARC output
  --invert             Invert color scheme (for light terminal backgrounds)
  --version            Show the version and exit.
```

The `--include` and `--exclude` flags can be used multiple times to specify multiple criteria. They accept a pattern which is a sort of comma-separated filter expression for matching MARC fields. Examples:

```sh
# records with a 780 field
marcgrep -i 780 FILE.mrc
# records with Ulysses in the 245 field
marcgrep -i '245,Ulysses' FILE.mrc
# titles _without_ "Collected Poems" in the 245 ‡a subfield
marcgrep -e '245,a,Collected Poems' FILE.mrc
# titles with second indicator = 4 that do not start with "The "
marcgrep -i '245,,4,,^(?!The )' FILE.mrc
```

The meaning of the filter expression's components depends upon their number:

- 1: field, `910` -> 910 is in record
- 2: field and value (regular expression), `100,Lorde` -> 100 contains string "Lorde"
- 3: field, subfield, and value, `506,a,Open Access` -> 506‡a contains string "Open Access"
- 4: field, subfield, first indicator, and value, `856,0,u,@lcsh\.gov` -> 856‡u with 1st indicator 0 contains string "@lcsh.gov"
- 5: field, subfield, first & second indicators, and value, `245,0,4,a,The Communist Manifesto`

The intention of this syntax is to facilitate searching subfields and field values more easily than MARCgrep.pl since we care about them more often than indicators. To ignore a component but use one of lesser priority, leave the component empty. For instance, `856,s,` refers to records with an `856` field with an `s` subfield but the trailing comma means we don't care about the subfield's value. The pattern `245,,4,,` refers to records with a `245` field with a second indicator of `4` regardless its subfields or value.

To use a literal comma in a value pattern, include all the other components. For instance, to search for "Morrison, Toni" anywhere in a `100` field, use `100,,,,Morrison, Toni`.

Multiple criteria are combined with logical AND. Multiple `--include` flags is narrower than one, as is an `--include` and an `--exclude`.

## Color & Formatting

The `--color` flag lets you pick colors for various parts of a MARC record using environment variables. You can pick from [the available termcolor colors](https://github.com/termcolor/termcolor?tab=readme-ov-file#text-properties). The defaults are:

| Component | Color | Var |
|---|----|---|
| Tag | cyan | MARC_TAG_COLOR |
| Indicator | light_yellow | MARC_INDICATOR_COLOR |
| Subfield code | green | MARC_SUBFIELD_COLOR |
| Data | white | MARC_DATA_COLOR |

There is an inverted color scheme available with the `--invert` flag for use with light (e.g. white) terminal backgrounds.

You can also configure the subfield delimiter character and the symbol for an empty indicator. Those defaults are:

| Symbol | Var |
|---|---|
| ‡ | MARC_SUBFIELD_DELIMITER |
| _ | MARC_EMPTY_INDICATOR |

## Development

[Poetry](https://python-poetry.org/) is used for development.

```sh
poetry install # install dependencies
poetry run pytest # run tests
poetry build # build package, used in CI
```

Any tag triggers a release to [Test PyPI](https://test.pypi.org/project/marcgrep/). Any tag beginning with the letter `v` requires manual approval to be released to [PyPI](https://pypi.org/project/marcgrep/) and [GitHub](https://github.com/phette23/marcgreppy/releases). There are protection rules on the `pypi` and `testpypi` [environments](https://github.com/phette23/marcgreppy/settings/environments) to this effect, too.

## License

[MIT](https://opensource.org/license/mit) © Eric Phetteplace 2024.
