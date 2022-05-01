import os
from piku.commands.version import get_version
from piku.core import config, utils, packages


def info_command(args):
    print(f'Piku Version: {get_version()}')
    print(f'Data directory: {config.data_path}')
    print(f'Backup directory: {config.backup_path}')

    if args.clear_cache:
        print('Clearing cache...')
        utils.remove(config.cache_path)
        os.makedirs(config.cache_path, exist_ok=True)
        print('Done')

    if args.packages:
        print('Availiable packages...')
        for package in packages.all():
            print(f' * {package}')
        print('Done')
