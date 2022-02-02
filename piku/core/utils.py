import os
import shutil
import hashlib
import difflib
import requests


def checksum(path):
    hasher = hashlib.md5()
    with open(path,'rb') as f:
        while chunk := f.read(128 * hasher.block_size):
            hasher.update(chunk)
    return hasher.digest()

def tree(path):
    paths = []
    for root, dirs, files in os.walk(path):
        paths.extend([os.path.relpath(os.path.join(root, d), path) for d in dirs])
        paths.extend([os.path.relpath(os.path.join(root, f), path) for f in files])
    return set(paths)

def copy(src, dst):
    if os.path.isdir(src):
        os.makedirs(dst, exist_ok=True)
    else:
        shutil.copy2(src, dst)

def remove(path):
    if os.path.isdir(path):
        try:
            os.rmdir(path)
        except OSError:
            pass # raised if dir is not empty, this should only happen when a file was ignored in the folder
    else:
        os.remove(path)

def similar(value, options):
    candidates = {k for k in options if value in k}
    return candidates.union(difflib.get_close_matches(value, options, 3, .3))

def download(url, path):
    with requests.get(url, stream=True) as r:
        with open(path, 'wb') as f:
            shutil.copyfileobj(r.raw, f)
    return path
