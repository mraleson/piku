from piku.commands.version import get_version
from piku.core.config import bundle_path, backup_path, deploy_path


def info_command(args):
    print(f'Piku Version: {get_version()}')
    print(f'Bundle directory: {bundle_path}')
    print(f'Backup directory: {backup_path}')
    print(f'Deploy directory: {deploy_path}')
