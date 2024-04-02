# marcgrep

A CLI for searching MARC files like [MARCgrep.pl](https://pusc.it/bib/MARCgrep) but in Python and a bit different syntax.

[marcli](https://github.com/hectorcorrea/marcli) is also a similar project that's faster but a little less flexible.

## Installation

Python 3.9 or later. [Poetry](https://python-poetry.org/) is used for development.

```sh
pipx install marcgrep # install globally with pipx
pip install marcgrep # or use pip/pip3
```

## Usage

```sh
# general command format
$ marcgrep OPTIONS FILE.mrc
$ cat FILE.mrc | marcgrep OPTIONS
# full usage information
$ marcgrep -h
Usage: marcgrep [OPTIONS] [FILE]

  Find MARC records matching patterns in a file.

Options:
  -h, --help          Show this message and exit.
  -v, --version       Show marcgrep version
  -c, --count         Count matching records
  -i, --include TEXT  Include matching records (repeatable)
  -e, --exclude TEXT  Exclude matching records (repeatable)
```

The `--include` and `--exclude` flags can be used multiple times to specify multiple criteria. They accept a pattern which is a sort of comma-separated filter expression for matching MARC fields. Examples:

```sh
# records with a 780 field
$ marcgrep -i 780 FILE.mrc
# records with Ulysses in the 245 field
$ marcgrep -i '245,Ulysses' FILE.mrc
# titles _without_ "Collected Poems" in the 245 $a subfield
$ marcgrep -e '245,a,Collected Poems' FILE.mrc
# titles with second indicator = 4 that do not start with "The "
$ marcgrep -i '245,,4,,^(?!The )' FILE.mrc
```

The meaning of the pattern's components depends upon their number:

- 1: field, `910` -> 910 is in record
- 2: field and value (regular expression), `100,Lorde` -> 100 contains string "Lorde"
- 3: field, subfield, and value, `506,a,Open Access` -> 506$a contains string "Open Access"
- 4: field, subfield, first indicator, and value, `856,0,u,@lcsh\.gov` -> 856$u with 1st indicator 0 contains string "@lcsh.gov"
- 5: field, subfield, first & second indicators, and value, `245,0,4,a,The Communist Manifesto`

The intention of this syntax is to facilitate searching subfields and field values more easily than MARCgrep.pl since we care about them more often than indicators. To ignore a component but use one of lesser priority, leave the component empty. For instance, `856,s,` refers to records with an `856` field with a `$s` subfield but the trailing comma means we don't care about the subfield's value. The pattern `245,,4,,` refers to records with a `245` field with a second indicator of `4` regardless its subfields or value.

Multiple criteria are combined with logical AND. Multiple `--include` flags is narrower than one, as is an `--include` and an `--exclude`.

## Development

- [x] -c count
- [x] -v version
- [ ] -l limit (number of records to process)
- [x] -i include criteria (multiple)
- [x] -e exclude criteria (multiple)
- [ ] -f fields to print
- [ ] work with MARC leader
- [ ] regex for all components? e.g. `24.,text in any 240-249 field`
- [ ] relatedly, specify _not_ to treat value as a regex?

```sh
poetry install # install dependencies
poetry run pytest # run tests
```

## License

[MIT](https://opensource.org/license/mit) © Eric Phetteplace 2024.
