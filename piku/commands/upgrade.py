from piku.core import config
from piku.commands.add import add


def upgrade_command(args):
    dependencies = config.get('dependencies')
    for package in dependencies:
        add(package, 'latest')
