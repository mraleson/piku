import os
import zipfile
import requests
from piku.core import config, utils, errors


# get package index
@utils.cache('dict')
@utils.cache('file', minutes=60 * 24)
def get_index():
    response = requests.get(config.index_url)
    if response.status_code != 200:
        raise errors.PikuError('Unable to download package index')
    return response.json().get('index')

# list latest circuit python version target
def latest_target():
    index = get_index()
    return sorted(list(index.keys()))[-1]

# list all packages in index
def all(target=None):
    if target is None: target = config.get('circuit-python')
    index = get_index()
    return sorted(list(index.get(target).keys()))

# suggest a package lexically similar to the one provided
def suggest(package, target=None):
    return utils.similar(package, all(target))

# find version matching package
def find(package, constraint, target=None):
    # get all packages
    if target is None: target = config.get('circuit-python')
    packages = get_index().get(target)

    # check package exists
    if package not in packages:
        raise errors.PackageNotFound(package)

    # find latest matching version
    versions = utils.sort_versions(list(packages[package].keys()), reverse=True)
    for version in versions:
        matched = utils.matches_semver(constraint, version) or version == constraint
        if matched:
            return version
    raise errors.VersionNotFound(package, constraint)

# returns a package's dependencies as specified in the bundle's package index
def dependencies(package, version, target=None):
    if target is None: target = config.get('circuit-python')
    packages = get_index().get(target)
    return packages[package][version]['dependencies']

# get package info
def info(package, version, target=None):
    if target is None: target = config.get('circuit-python')
    packages = get_index().get(target)
    return packages[package][version]

# removes a package from lib
def remove(package, lock, project_path=None):
    project_path = project_path or config.get('source')
    path = lock[package]['path']
    package_base_name = os.path.basename(os.path.normpath(path))
    library_path = os.path.join(project_path, 'lib')
    package_path = os.path.join(library_path, package_base_name)
    utils.remove(package_path)
    utils.remove(os.path.normpath(package_path) + '.mpy')

# installs a package to lib
def install(package, lock, project_path=None):
    # find bundle url
    package_info = lock[package]
    bundle_info = package_info['bundle']
    bundle_url = bundle_info['url']
    bundle_key = f'{bundle_info["name"]}-{bundle_info["build"]}-{bundle_info["target"]}'

    # download zip
    zip_path = os.path.join(config.bundle_path, f'{bundle_key}.zip')
    if not os.path.exists(zip_path):
        os.makedirs(config.bundle_path, exist_ok=True)
        utils.download(bundle_url, zip_path)

    # extract bundle zip
    extracted_path = os.path.join(config.bundle_path, f'{bundle_key}')
    if not os.path.exists(extracted_path):
        os.makedirs(extracted_path, exist_ok=True)
        with zipfile.ZipFile(zip_path, 'r') as zip:
            zip.extractall(extracted_path)
    extracted_path = os.path.join(extracted_path, os.listdir(extracted_path)[0])

    # copy package to project
    project_path = project_path or config.get('source')
    library_path = os.path.join(project_path, 'lib')
    if os.path.isdir(project_path):
        os.makedirs(library_path, exist_ok=True)
    package_path = os.path.join(extracted_path, package_info['path'])
    if not os.path.exists(package_path):
        package_path = package_path + '.mpy'

    return utils.copy(package_path, library_path)
