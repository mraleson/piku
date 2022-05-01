import os
import pytest
from pathlib import Path
from types import SimpleNamespace
from piku.core import config
from piku.commands.info import info_command
from tests.fixtures import project


def test_info(capsys, project):
    info_command(SimpleNamespace(packages=False, clear_cache=False))
    out, _ = capsys.readouterr()
    assert 'Piku Version' in out

def test_info_packages(capsys, project):
    info_command(SimpleNamespace(packages=True, clear_cache=False))
    out, _ = capsys.readouterr()
    assert 'neopixel' in out

@pytest.mark.slow
def test_info_clear_cache(capsys):
    Path(os.path.join(config.cache_path, 'test')).touch()
    assert os.listdir(config.cache_path)
    info_command(SimpleNamespace(packages=False, clear_cache=True))
    out, _ = capsys.readouterr()
    assert 'Clearing cache' in out
    assert not os.listdir(config.cache_path)
