import os
import toml


config_path = os.path.join(os.getcwd(), 'piku.toml')

def load():
    return toml.load(config_path)

def save(config):
    with open(config_path, 'w') as file:
        toml.dump(config, file)

def get(section, key, default=None):
    config = load()
    return config.get(section, {}).get(key, default)

def set(section, key, value):
    config = load()
    if section not in config:
        config[section] = {}
    return config[section].set(key, value)
