import os
import shutil
import hashlib
import difflib
import requests


def nget(dictionary, keys, default=None):
    for key in keys[:-1]:
        dictionary = dictionary.get(key, {})
    return dictionary.get(keys[-1], default)

def nset(dictionary, keys, value):
    for key in keys[:-1]:
        dictionary = dictionary.setdefault(key, {})
    dictionary[keys[-1]] = value

def ndel(dictionary, keys):
    for key in keys[:-1]:
        dictionary = dictionary.setdefault(key, {})
    if keys[-1] in dictionary:
        value = dictionary[keys[-1]]
        del dictionary[keys[-1]]
        return value
    return None

def checksum(path):
    hasher = hashlib.md5()
    with open(path, 'rb') as f:
        while chunk := f.read(128 * hasher.block_size):
            hasher.update(chunk)
    return hasher.digest()

def tree(path):
    paths = []
    for root, dirs, files in os.walk(path):
        paths.extend([os.path.relpath(os.path.join(root, d), path) for d in dirs])
        paths.extend([os.path.relpath(os.path.join(root, f), path) for f in files])
    return set(paths)

def copy(src, dst, recursive=True, contents=False):
    if os.path.isdir(src):
        if recursive:
            if contents:
                return shutil.copytree(src, dst, dirs_exist_ok=True)
            return shutil.copytree(src, os.path.join(dst, os.path.basename(src)), dirs_exist_ok=True)
        return os.makedirs(dst, exist_ok=True)
    return shutil.copy2(src, dst)

def remove(path, recursive=True):
    if os.path.isdir(path):
        if recursive:
            shutil.rmtree(path)
        else:
            try:
                os.rmdir(path)
            except OSError:
                pass  # raised if dir is not empty, this should only happen when a file was ignored in the folder
    else:
        # This is a workaround for the fact that on macOS, removing
        # extended attribute/resource fork files (._*) will fail once
        # the file they belong to is removed.
        try:
            os.remove(path)
        except FileNotFoundError:
            pass

def similar(value, options):
    candidates = {k for k in options if value in k}
    return candidates.union(difflib.get_close_matches(value, options, 3, 0.3))

def download(url, path):
    with requests.get(url, stream=True) as r:
        with open(path, 'wb') as f:
            shutil.copyfileobj(r.raw, f)
    return path
