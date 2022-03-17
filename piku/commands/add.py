from piku.core import config, errors, packages, locker


# attempt to add a package given it name and a version constraint
def add(package_name, package_constraint):
    # find maching package version
    package_version = packages.find(package_name, package_constraint)

    # add package to project toml file
    config.set(f'dependencies.{package_name}', package_constraint)

    # update locked packages
    existing_lock = locker.load()
    updated_lock = locker.lock(existing_lock, additions=[(package_name, package_version)])
    locker.save(updated_lock)

    # remove old packages that were updated or replaced
    for package in existing_lock:
        if package not in updated_lock or updated_lock[package]['version'] != existing_lock[package]['version']:
            packages.remove(package, existing_lock)

    # install all new packages that were updated or added
    for package in updated_lock:
        if package not in existing_lock or updated_lock[package]['version'] != existing_lock[package]['version']:
            packages.install(package, updated_lock)

def add_command(args):
    # check that we are in a piku project directory
    if not config.valid():
        print('Failed: unable to find piku project in current directory.')
        return

    # parse package and constraint
    package = args.package
    constraint = 'latest'
    if '@' in args.package:
        package, constraint = args.package.split('@')

    # find a match for the required package
    try:
        add(package, constraint)
    except errors.PackageNotFound:
        print(f'Unable to resolve requested package: {package}')
        suggestions = packages.suggest(package)
        if suggestions:
            print('Did you mean')
        for suggestion in suggestions:
            print(f' * {suggestion}')
        return
    except errors.VersionNotFound:
        print(f'Unable to find {package} package matching version {constraint}')
