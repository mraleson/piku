from piku.core import config
from piku.commands.add import add


def upgrade_command(args):
    # check that we are in a piku project directory
    if not config.valid():
        print('Failed: unable to find piku project in current directory.')
        return

    dependencies = config.get('dependencies')
    for package in dependencies:
        add(package, 'latest')
