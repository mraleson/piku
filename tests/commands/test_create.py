import os
import tempfile
from types import SimpleNamespace
from piku.core import utils
from piku.commands.create import create_command


def test_create(capsys):
    # create a temp directory
    project = 'bogus'
    test_path = os.path.join(tempfile.gettempdir(), 'piku')
    utils.remove(test_path)
    os.makedirs(test_path, exist_ok=True)
    cwd = os.getcwd()
    os.chdir(test_path)

    # create project
    create_command(SimpleNamespace(project=project, directory=None))
    out, _ = capsys.readouterr()
    assert project in out
    assert 'pyproject.toml' in os.listdir(os.path.join(test_path, project))
    utils.remove(test_path)
    os.chdir(cwd)
