from cachy import CacheManager
from piku.core import config


config = {
    'default': 'file',
    'serializer': 'json',
    'stores': {
        'file': {
            'driver': 'file',
            'path': config.cache_path
        },
        'dict': {
            'driver': 'dict'
        }
    }
}

cache = CacheManager(config)
