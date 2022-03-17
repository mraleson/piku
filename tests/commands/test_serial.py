from types import SimpleNamespace
from piku.commands.serial import serial_command


def test_serial(capsys):
    serial_command(SimpleNamespace(serial='bogus'))
    out, _ = capsys.readouterr()
    assert 'Connecting' in out
