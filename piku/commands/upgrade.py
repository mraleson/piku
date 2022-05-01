from piku.core import config
from piku.commands.add import add


def upgrade_command(args):
    # check that we are in a piku project directory
    if not config.valid():
        print('Failed: unable to find piku project in current directory.')
        return

    # re-add all packages as latest
    total_conflicts = set()
    dependencies = config.get('dependencies')
    for package in dependencies:
        previous, current, conflicts = add(package, 'latest')
        total_conflicts = total_conflicts.union(conflicts)

    # note conflicts
    if total_conflicts:
        print('Note, there may be multiple version requirements for following packages:')
        for c in total_conflicts:
            print(f' * {c}')
