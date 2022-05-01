from types import SimpleNamespace
from piku.commands.version import version_command


def test_version(capsys):
    version_command(SimpleNamespace())
    out, _ = capsys.readouterr()
    assert '.' in out
