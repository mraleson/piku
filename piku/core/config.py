import os
import toml
from appdirs import user_data_dir


config_path = os.path.join(os.getcwd(), 'pyproject.toml')
lock_path = os.path.join(os.getcwd(), 'piku.lock')
data_path = user_data_dir('piku', 'piku')
backup_path = os.path.join(data_path, 'backup')
cache_path = os.path.join(data_path, 'cache')
bundle_path = os.path.join(cache_path, 'bundle')
index_url = 'https://raw.githubusercontent.com/mraleson/piku-index/main/data/packages.json'

defaults = {
    'tool':
    {
        'piku': {
            'project': None,
            'piku': None,
            'circuit-python': None,
            'board': None,
            'source': './project',
        }
    }
}


# nested dictionary helpers
def nget(dictionary, keys, default=None):
    for key in keys[:-1]:
        dictionary = dictionary.get(key, {})
    return dictionary.get(keys[-1], default)

def nset(dictionary, keys, value):
    for key in keys[:-1]:
        dictionary = dictionary.setdefault(key, {})
    dictionary[keys[-1]] = value

def ndel(dictionary, keys):
    for key in keys[:-1]:
        dictionary = dictionary.setdefault(key, {})
    if keys[-1] in dictionary:
        value = dictionary[keys[-1]]
        del dictionary[keys[-1]]
        return value
    return None


# load config
def load():
    return toml.load(config_path)

# save config
def save(config):
    with open(config_path, 'w') as file:
        toml.dump(config, file)

# get value from nested dictionary with dotted pack a.b.c
def get(dotpath):
    config = load()
    if not dotpath.startswith('tool.piku'):
        dotpath = 'tool.piku' + '.' + dotpath
    keys = dotpath.split('.')
    return nget(config, keys, nget(defaults, keys))

# set value from nested dictionary with dotted pack a.b.c
def set(dotpath, value):
    config = load()
    if not dotpath.startswith('tool.piku'):
        dotpath = 'tool.piku' + '.' + dotpath
    keys = dotpath.split('.')
    nset(config, keys, value)
    save(config)

# remove value from nested dictionary with dotted pack a.b.c
def remove(dotpath):
    config = load()
    if not dotpath.startswith('tool.piku'):
        dotpath = 'tool.piku' + '.' + dotpath
    keys = dotpath.split('.')
    value = ndel(config, keys)
    save(config)
    return value

# returns true if in a valid piku project
def valid():
    try:
        config = load()
        if not config.get('tool').get('piku'):
            return False
    except FileNotFoundError:
        return False
    return True
