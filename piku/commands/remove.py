from piku.core import config, packages, utils, locker


def remove_command(args):
    package = args.package.lower()

    # check that we are in a piku project directory
    if not config.valid():
        print('Failed: unable to find piku project in current directory.')
        return

    # remove package from pyproject.toml
    if not config.remove(f'tool.piku.dependencies.{package}'):
        print(f'Unable to find matching package {package} in pyproject.toml')
        suggestions = utils.similar(package, config.get('tool.piku.dependencies').keys())
        if suggestions:
            print('Did you mean')
            for suggestion in suggestions:
                print(f' * {suggestion}')
        return

    # remove package to project toml file
    config.remove(f'dependencies.{package}')

    # update lock file
    existing_lock = locker.load()
    updated_lock, conflicts = locker.lock(existing_lock, removals=[package])
    locker.save(updated_lock)

    # remove all packages no longer in lock file
    removed = set(existing_lock.keys()) - set(updated_lock.keys())
    for package in removed:
        packages.remove(package, existing_lock)
