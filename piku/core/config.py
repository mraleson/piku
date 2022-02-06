import os
import toml
from appdirs import user_data_dir
from piku.core.utils import nset, nget, ndel


defaults = {
    'tool':
    {
        'piku': {
        'source': './project'
        }
    }
}

config_path = os.path.join(os.getcwd(), 'pyproject.toml')
data_path = user_data_dir('piku', 'piku')
bundle_path = os.path.join(data_path, 'bundle')
backup_path = os.path.join(data_path, 'backup')
deploy_path = os.path.join(data_path, 'deploy')


def load():
    return toml.load(config_path)

def save(config):
    with open(config_path, 'w') as file:
        toml.dump(config, file)

def get(dotpath):
    config = load()
    assert dotpath.startswith('tool.piku')
    keys = dotpath.split('.')
    return nget(config, keys, nget(defaults, keys))

def set(dotpath, value):
    config = load()
    assert dotpath.startswith('tool.piku')
    keys = dotpath.split('.')
    nset(config, keys, value)
    save(config)

def remove(dotpath):
    config = load()
    assert dotpath.startswith('tool.piku')
    keys = dotpath.split('.')
    value = ndel(config, keys)
    save(config)
    return value
