import pytest

from nudge import cli
from clize import run
from io import StringIO


@pytest.fixture
def command():
    def runner(command_string):
        out, err = StringIO(), StringIO()
        run(cli, args=tuple(command_string.split()), out=out, err=err, exit=False)
        return out.getvalue(), err.getvalue()
    return runner


def test_help(command):
    out, err = command('nudge --help')
    print out
    print err
    assert not err
    assert 'nudge' in out
