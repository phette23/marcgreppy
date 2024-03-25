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
marcgrep OPTIONS FILE.mrc
marcgrep -h # see full usage information
```

## Development

- [x] -c count
- [x] -v version
- [ ] -l limit (number of records to process)
- [ ] -i include criteria (multiple)
- [ ] -e exclude criteria (multiple)
- [ ] -f fields to print
- [ ] --progress?

```sh
poetry install # install dependencies
poetry run pytest # run tests
```

## License

[MIT](https://opensource.org/license/mit) © Eric Phetteplace 2024.
