from piku.core import config
from piku.commands.add import add


def install_command(args):
    # check that we are in a piku project directory
    if not config.valid():
        print('Failed: unable to find piku project in current directory.')
        return

    # add all dependencies
    total_conflicts = set()
    dependencies = config.get('dependencies')
    for package in dependencies:
        constraint = dependencies[package]
        previous, current, conflicts = add(package, constraint)
        total_conflicts = total_conflicts.union(conflicts)

    # note conflicts
    if total_conflicts:
        print('Note, there may be multiple version requirements for following packages:')
        for c in total_conflicts:
            print(f' * {c}')
