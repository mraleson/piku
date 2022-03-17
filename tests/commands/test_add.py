import os
from types import SimpleNamespace
from piku.core import locker, config
from piku.commands.add import add_command
from tests.fixtures import project


def test_add_latest(capsys, project):
    add_command(SimpleNamespace(package='adafruit_bus_device@5.1.6'))
    add_command(SimpleNamespace(package='adafruit_magtag'))
    out, _ = capsys.readouterr()
    assert 'Note' in out and 'adafruit_bus_device' in out
    lock = locker.load()
    packages = set([
        'adafruit_magtag',
        'adafruit_portalbase',
        'adafruit_bitmap_font',
        'adafruit_display_text',
        'neopixel',
        'adafruit_pixelbuf',
        'adafruit_requests',
        'adafruit_io',
        'adafruit_esp32spi',
        'adafruit_bus_device',
        'simpleio',
        'adafruit_fakerequests',
        'adafruit_miniqr',
        'neopixel',
        'adafruit_requests',
        'simpleio'])
    assert set(lock.keys()) == packages
    assert len(os.listdir(os.path.join(project, 'project', 'lib'))) == len(packages)
    deps = config.get('dependencies')
    assert 'adafruit_bus_device' in deps
    assert 'adafruit_magtag' in deps

def test_add_bad_package(capsys, project):
    add_command(SimpleNamespace(package='neo'))
    # add_command(SimpleNamespace(package='adafruit_boardtest'))
    out, _ = capsys.readouterr()
    assert 'Did you mean' in out and 'neopixel' in out

def test_add_bad_package_constraint(capsys, project):
    add_command(SimpleNamespace(package='neopixel@0.0.123'))
    # add_command(SimpleNamespace(package='adafruit_boardtest'))
    out, _ = capsys.readouterr()
    assert 'Unable to find' in out and 'neopixel' in out and '0.0.123' in out
