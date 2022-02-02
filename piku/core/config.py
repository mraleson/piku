import os
import toml
from appdirs import user_data_dir


config_path = os.path.join(os.getcwd(), 'piku.toml')
data_path = user_data_dir('piku', 'piku')
bundle_path = os.path.join(data_path, 'bundle')
backup_path = os.path.join(data_path, 'backup')
deploy_path = os.path.join(data_path, 'deploy')

def load():
    return toml.load(config_path)

def save(config):
    with open(config_path, 'w') as file:
        toml.dump(config, file)

def get(section, key=None, default=None):
    config = load()
    if key is None:
        return config.get(section, {})
    return config.get(section, {}).get(key, default)

def set(section, key, value):
    config = load()
    if section not in config:
        config[section] = {}
    config[section][key] = value
    save(config)

def remove(section, key):
    config = load()
    if section not in config:
        config[section] = {}
    if key in config[section]:
        value = config[section][key]
        del config[section][key]
        save(config)
        return value
