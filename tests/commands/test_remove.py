import os
from types import SimpleNamespace
from piku.core import locker, config
from piku.commands.add import add_command
from piku.commands.remove import remove_command
from tests.fixtures import project


def test_remove(project):
    add_command(SimpleNamespace(package='adafruit_bus_device@5.1.6'))
    add_command(SimpleNamespace(package='adafruit_magtag'))
    add_command(SimpleNamespace(package='neopixel'))
    remove_command(SimpleNamespace(package='adafruit_bus_device'))
    assert 'adafruit_bus_device' in locker.load().keys()
    assert len(os.listdir(os.path.join(project, 'project', 'lib'))) == len(locker.load().keys())
    remove_command(SimpleNamespace(package='adafruit_magtag'))
    assert 'neopixel' in locker.load().keys() and 'adafruit_pixelbuf' in locker.load().keys()
    assert len(os.listdir(os.path.join(project, 'project', 'lib'))) == len(locker.load().keys())
    remove_command(SimpleNamespace(package='neopixel'))
    assert len(locker.load().keys()) == 0
    assert len(os.listdir(os.path.join(project, 'project', 'lib'))) == len(locker.load().keys())
