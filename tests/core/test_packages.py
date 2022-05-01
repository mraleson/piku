import os
import pytest
from tests.fixtures import tempdir
from piku.core import packages, errors, utils


def test_get_index():
    index = packages.get_index()
    assert len(index) > 0

def test_latest_target():
    assert packages.latest_target() == '7'

def test_all():
    all = packages.all('7')
    assert 'neopixel' in all and 'dynamixel' in all

def test_suggest():
    suggestions = packages.suggest('neo', '7')
    assert suggestions == ['neopixel', 'neopixel_spi', 'adafruit_neokey', 'adafruit_neotrellis', 'asyncio']

def test_find():
    assert utils.parse_semver(packages.find('neopixel', '*', target='7')) >= utils.parse_semver('6.2.4')
    assert packages.find('neopixel', '~6', target='7').startswith('6.')
    assert packages.find('neopixel', '6.0.3', target='7') == '6.0.3'
    assert packages.find('dynamixel', '*', target='7') == '0.0.0'
    assert utils.parse_semver(packages.find('adafruit_lis3mdl', 'latest', target='7')) >= utils.parse_semver('1.1.12')
    with pytest.raises(errors.PackageNotFound):
        packages.find('bogus', '*', target='7')
    with pytest.raises(errors.VersionNotFound):
        packages.find('neopixel', '~5', target='7')

def test_info():
    info = packages.info('neopixel', '6.2.4', target='7')
    assert info['package'] == 'neopixel'

def test_dependencies():
    dependencies = packages.dependencies('neopixel', '6.2.4', target='7')
    assert dependencies == {'adafruit_pixelbuf': '1.1.2'}
    dependencies = packages.dependencies('adafruit_boardtest', '1.2.9', target='7')
    assert dependencies == {'adafruit_bus_device': '5.1.2', 'adafruit_sdcard': '3.3.7'}

def test_install(tempdir):
    lock = {
        'neopixel': packages.get_index()['7']['neopixel']['6.2.4']
    }
    packages.install('neopixel', lock, project_path=tempdir)
    assert 'neopixel.mpy' in os.listdir(os.path.join(tempdir, 'lib'))
