from io import StringIO

import pytest
from clize import run

from nudge import cli


@pytest.fixture
def command():
    def runner(command_string):
        out, err = StringIO(), StringIO()
        run(
            cli,
            args=tuple(command_string.split()),
            out=out,
            err=err,
            exit=False,
        )
        return out.getvalue(), err.getvalue()

    return runner


def test_help(command):
    out, err = command("nudge --help")
    assert not err
    assert "nudge" in out
