import os
import tempfile
from types import SimpleNamespace
import pytest
from piku.core import utils, config
from piku.commands.create import create_command


@pytest.fixture
def project(mocker, capsys):
    # create temp dirs
    temp_project_path = os.path.join(tempfile.gettempdir(), 'piku')
    utils.remove(temp_project_path)
    os.makedirs(temp_project_path, exist_ok=True)

    # change cwd
    cwd = os.getcwd()
    os.chdir(temp_project_path)

    # create a project
    project_name = 'bogus'
    create_command(SimpleNamespace(project=project_name))
    os.chdir(project_name)
    capsys.readouterr()

    # mock paths
    mocker.patch.object(config, 'config_path', os.path.join(os.getcwd(), 'pyproject.toml'))
    mocker.patch.object(config, 'lock_path', os.path.join(os.getcwd(), 'piku.lock'))


    yield os.getcwd()

    # clean mocks
    mocker.resetall()

    # clear up project
    utils.remove(temp_project_path)
    os.chdir(cwd)

@pytest.fixture
def tempdir():
    temp_path = os.path.join(tempfile.gettempdir(), 'piku')
    os.makedirs(temp_path)
    yield temp_path
    utils.remove(temp_path)
