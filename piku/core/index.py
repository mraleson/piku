import os
import json
import zipfile
from piku.core import config, utils


bundles = {
    '7': {
        'official': 'https://github.com/adafruit/Adafruit_CircuitPython_Bundle/releases/download/20220131/adafruit-circuitpython-bundle-7.x-mpy-20220131.zip',
        'community': 'https://github.com/adafruit/CircuitPython_Community_Bundle/releases/download/20220113/circuitpython-community-bundle-7.x-mpy-20220113.zip'
    }
}

# create index of known offical and community modules
def index(bundle):
    # check that we have sources for this bundle
    if bundle not in bundles:
        return None

    # construct paths
    bundle_cache_path = os.path.join(config.bundle_path, bundle)
    bundle_index_path = os.path.join(bundle_cache_path, 'index.json')
    official_zip_url = bundles[bundle]['official']
    official_zip_file = official_zip_url.split('/')[-1]
    official_zip_path = os.path.join(bundle_cache_path, official_zip_file)
    official_bundle_path = os.path.join(bundle_cache_path, official_zip_file.replace('.zip', ''))
    official_lib_path = os.path.join(official_bundle_path, 'lib')
    community_zip_url = bundles[bundle]['community']
    community_zip_file = community_zip_url.split('/')[-1]
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
        idx[name] = os.path.join(official_lib_path, module)
    for module in os.listdir(community_lib_path):
        name = module.replace('.mpy', '')
        idx[name] = os.path.join(community_lib_path, module)
    with open(bundle_index_path, 'w') as f:
        json.dump(idx, f, indent=2)

    # return index
    return idx
