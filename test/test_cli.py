from pathlib import Path
import re

from click.testing import CliRunner
import pytest

from marcgrep.cli import main

OAPEN = str(Path("test") / "fixtures" / "OAPEN.mrc")
ONE_RECORD = str(Path("test") / "fixtures" / "one_record.mrc")
ONE_RECORD_LINES = 66
PLAIN_TEXT = str(Path("test") / "fixtures" / "plain.txt")


class TestCLI:
    def test_count(self):
        runner = CliRunner()
        result = runner.invoke(main, [ONE_RECORD, "--count"])
        assert result.exit_code == 0
        assert result.output == "1\n"
        result = runner.invoke(main, [PLAIN_TEXT, "-c"])
        assert result.exit_code == 1
        assert result.output == "0\n"
        result = runner.invoke(main, [OAPEN, "-c"])
        assert result.exit_code == 0
        assert result.output == "500\n"

    def test_print(self):
        runner = CliRunner()
        result = runner.invoke(main, [ONE_RECORD])
        assert result.exit_code == 0
        assert len(result.output.splitlines()) == ONE_RECORD_LINES
        assert "Kulturpolitik" in result.output

    def test_one_include_print(self):
        runner = CliRunner()
        result = runner.invoke(
            main,
            [ONE_RECORD, "--include", "245,1,,a,Kulturpolitik"],
        )
        assert result.exit_code == 0
        assert len(result.output.splitlines()) == ONE_RECORD_LINES
        assert "Kulturpolitik" in result.output
        result = runner.invoke(
            main,
            [ONE_RECORD, "--include", "653,text that isn't there"],
        )
        assert result.exit_code == 1
        assert len(result.output.splitlines()) == 0

    def test_one_include_count(self):
        runner = CliRunner()
        result = runner.invoke(
            main,
            ["test/fixtures/OAPEN.mrc", "--include", "245,Kulturpolitik", "-c"],
        )
        assert result.exit_code == 0
        assert len(result.output.splitlines()) == 1

    def test_one_exclude_print(self):
        runner = CliRunner()
        result = runner.invoke(
            main,
            [ONE_RECORD, "--exclude", "245,Kulturpolitik"],
        )
        assert result.exit_code == 1
        assert len(result.output.splitlines()) == 0
        result = runner.invoke(
            main,
            [ONE_RECORD, "--exclude", "245,text that isn't there"],
        )
        assert result.exit_code == 0
        assert len(result.output.splitlines()) == ONE_RECORD_LINES

    def test_include_and_exclude(self):
        runner = CliRunner()
        result = runner.invoke(
            main,
            [
                ONE_RECORD,
                "--include",
                "245,1,,a,Kulturpolitik",
                "--exclude",
                "777",
            ],
        )
        assert result.exit_code == 0
        assert len(result.output.splitlines()) == ONE_RECORD_LINES
        result = runner.invoke(
            main,
            [
                ONE_RECORD,
                "--include",
                "245,text that's not there",
                "--exclude",
                "245,Kulturpolitik",
            ],
        )
        assert result.exit_code == 1
        assert len(result.output.splitlines()) == 0
        # exclude takes precedence
        result = runner.invoke(
            main,
            [
                ONE_RECORD,
                "--include",
                "245,1,,a,Kulturpolitik",
                "--exclude",
                "245,1,,a,Kulturpolitik",
            ],
        )
        assert result.exit_code == 1
        assert len(result.output.splitlines()) == 0
        # multiple includes use boolean AND
        result = runner.invoke(
            main,
            [
                ONE_RECORD,
                "--include",
                "245,1,,a,Kulturpolitik",
                "--include",
                "245,text that's not there",
            ],
        )
        assert result.exit_code == 1
        assert len(result.output.splitlines()) == 0
        result = runner.invoke(
            main,
            [
                ONE_RECORD,
                "--include",
                "245,1,,a,Kulturpolitik",
                "--include",
                "653,Netzwerke",
            ],
        )
        assert result.exit_code == 0
        assert len(result.output.splitlines()) == ONE_RECORD_LINES

    @pytest.mark.parametrize(
        "input,expected", [("1", "1"), ("10", "10"), ("100", "100")]
    )
    def test_limit(self, input, expected):
        runner = CliRunner()
        # all records have a 245 so the limit = the count
        result = runner.invoke(
            main, [OAPEN, "--limit", input, "-c", "--include", "245"]
        )
        assert result.exit_code == 0
        assert result.output == f"{expected}\n"
