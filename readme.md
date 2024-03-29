# marcgrep

Like [marcgrep.pl](https://pusc.it/bib/MARCgrep) but in Python and a bit different syntax.

[marcli](https://github.com/hectorcorrea/marcli) is also a similar project but will be faster yet a little less flexible.

## Installation

TODO: publish to PyPI.

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
  -i, --include TEXT  Include matching records
  -e, --exclude TEXT  Exclude matching records
```

## Development

- [x] -c count
- [x] -v version
- [ ] -l limit (number of records to process)
- [x] -i include criteria (multiple)
- [x] -e exclude criteria (multiple)
- [ ] -f fields to print
- [ ] work with MARC leader
- [ ] --progress?

```sh
poetry install # install dependencies
poetry run pytest # run tests
```

## License

[MIT](https://opensource.org/license/mit) © Eric Phetteplace 2024.
