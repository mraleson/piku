import json
from copy import deepcopy
from piku.core import config, packages


# load lock file
def load():
    try:
        with open(config.lock_path, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        return {}

# save lock file
def save(locked):
    with open(config.lock_path, 'w') as file:
        json.dump(locked, file, indent=2)

# get lock dictionary fingerprint set for comparing lock dictionaries
def fingerprint(locked):
    return {f'{k}{v["version"]}' for k, v in locked.items()}

# lock returns an updated locked packages dictionary given an existing one and any additions or removals
# existing: an existing locked packages dictionary
# additions: a list of (package, constraint) we want to add
# removals: a list of packages we want to remove
def lock(existing, additions=None, removals=None):
    # create new locked packages dictionary
    project_dependencies = config.get('dependencies')
    locked = deepcopy(existing or {})
    additions = additions or []
    removals = removals or []

    # add any new packages to the package lock
    for (package, version) in additions:
        locked[package] = packages.info(package, version)

    # remove requested packages from lock
    for package in removals:
        del locked[package]

    # expand dependencies
    previous = None
    conflicts = set()
    while previous is None or fingerprint(locked) != fingerprint(previous):
        previous = locked.copy()
        expanded = locked.copy()
        for package in locked:
            package_info = locked[package]
            dependencies = package_info['dependencies']
            for dep in dependencies:
                dep_info = packages.info(dep, dependencies[dep])
                if dep not in project_dependencies:
                    if dep in expanded and expanded[dep]['version'] != dep_info['version']:
                        conflicts.add(dep)
                    expanded[dep] = dep_info
                else:
                    conflicts.add(dep)
        locked = expanded

    # clean orphan dependencies
    previous = None
    while previous is None or fingerprint(locked) != fingerprint(previous):
        previous = locked.copy()
        expanded = locked.copy()
        for package in locked:
            orphaned = True
            for other in locked:
                if package in locked[other]['dependencies']:
                    orphaned = False
            if package not in project_dependencies and orphaned:
                del expanded[package]
        locked = expanded

    return locked, conflicts


# from piku.core import config, packages, project
#
# {
#     packages: {
#         package_name: {
#             version: package-bundle-version-build
#             dependencies: ['depenency_name']
#         }
#         dependencies: {
#             depenency_name: {
#             version: package-bundle-version-build
#         requested: ['package_name']
#     }
# }
#
# # generate a lock file and return a list of dependencies matched versions
# def lock(dependencies):
#     locked = {}
#     matched = {}
#
#     for package, constraint in dependencies.items():
#         # find build containing requested package
#         package_match = packages.find(package, constraint)
#         (bundle, version, build) = package_match
#         package_deps = packages.dependencies(package, bundle, build)
#         locked['']
#
#
# def install(locked):
#     pass
