import os
import json
import shutil
import zipfile
from piku.core import config, utils


bundles = {
    '7': {
        'official': 'https://github.com/adafruit/Adafruit_CircuitPython_Bundle/releases/download/20220131/adafruit-circuitpython-bundle-7.x-mpy-20220131.zip',
        'community': 'https://github.com/adafruit/CircuitPython_Community_Bundle/releases/download/20220113/circuitpython-community-bundle-7.x-mpy-20220113.zip'
    }
}

def clear_cache():
    try:
        shutil.rmtree(config.bundle_path)
    except FileNotFoundError:
        pass

def index(bundle):
    # construct paths
    bundle_cache_path = os.path.join(config.bundle_path, bundle)
    bundle_index_path = os.path.join(bundle_cache_path, 'index.json')
    official_zip_url = bundles[bundle]['official']
    official_zip_file = official_zip_url.split('/')[-1]
    official_version = official_zip_file.replace('.zip', '')
    official_zip_path = os.path.join(bundle_cache_path, official_zip_file)
    official_bundle_path = os.path.join(bundle_cache_path, official_zip_file.replace('.zip', ''))
    official_lib_path = os.path.join(official_bundle_path, 'lib')
    community_zip_url = bundles[bundle]['community']
    community_zip_file = community_zip_url.split('/')[-1]
    community_version = community_zip_file.replace('.zip', '')
    community_zip_path = os.path.join(bundle_cache_path, community_zip_file)
    community_bundle_path = os.path.join(bundle_cache_path, community_zip_file.replace('.zip', ''))
    community_lib_path = os.path.join(community_bundle_path, 'lib')

    # load index
    try:
        with open(bundle_index_path, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        pass

    # create bundle cache dir
    os.makedirs(bundle_cache_path, exist_ok=True)

    # download bundle zip files
    if not os.path.exists(official_zip_path):
        print ('Downloading official bundle...')
        utils.download(bundles[bundle]['official'], official_zip_path)
        print('Done')
    if not os.path.exists(community_zip_path):
        print ('Downloading community bundle...')
        utils.download(bundles[bundle]['community'], community_zip_path)
        print('Done')

    # extract bundles
    with zipfile.ZipFile(official_zip_path, 'r') as zip:
        zip.extractall(bundle_cache_path)
    with zipfile.ZipFile(community_zip_path, 'r') as zip:
        zip.extractall(bundle_cache_path)

    # build index
    idx = {}
    for module in os.listdir(official_lib_path):
        name = module.replace('.mpy', '')
        idx[name] = {'version': official_version, 'path': os.path.join(official_lib_path, module)}
    for module in os.listdir(community_lib_path):
        name = module.replace('.mpy', '')
        idx[name] = {'version': community_version, 'path': os.path.join(community_lib_path, module)}
    with open(bundle_index_path, 'w') as f:
        json.dump(idx, f, indent=2)

    # return index
    return idx

# find a module
def find(module, bundle):
    if bundle not in bundles:
        return {}
    idx = index(bundle)
    return idx.get(module, {})

def suggest(module, bundle):
    if bundle not in bundles:
        return set()
    idx = index(bundle)
    return utils.similar(module, idx.keys())

def aquire(source, lib_path):
    shutil.copy2(source, lib_path)
    return lib_path

def delete(module, lib_path):
    for path in os.listdir(lib_path):
        if path in [module, f'{module}.mpy']:
            utils.remove(os.path.join(lib_path, path))
            return True
    return False
