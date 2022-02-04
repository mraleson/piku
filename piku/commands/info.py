from piku.commands.version import get_version
from piku.core import modules, config, utils


def info_command(args):
    print(f'Piku Version: {get_version()}')
    print(f'Bundle directory: {config.bundle_path}')
    print(f'Backup directory: {config.backup_path}')
    print(f'Deploy directory: {config.deploy_path}')

    if args.clear_cache:
        print('Clearing module cache...')
        try:
            utils.remove(config.bundle_path)
        except FileNotFoundError:
            pass
        print('Done')

    if args.modules:
        index = modules.index(config.get('tool.piku.circuitpython'))
        print('Availiable modules...')
        for module in index.keys():
            print(f' * {module}')
        print('Done')
