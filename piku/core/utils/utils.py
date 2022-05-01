import re
import os
import shutil
import hashlib
import difflib
import requests
from poetry.core.semver import parse_constraint, exceptions


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
    compounds = sorted([k for k in options if value in k], key=len)
    close = difflib.get_close_matches(value, options, 3, 0.3)
    temp = [c for c in close if c not in set(compounds)]
    compounds.extend(temp)
    return compounds

def download(url, path):
    with requests.get(url, stream=True) as r:
        with open(path, 'wb') as f:
            shutil.copyfileobj(r.raw, f)
    return path

def matches_semver(constraint, version):
    if version is None: return False
    return parse_semver(constraint).allows(parse_semver(version))

patch_pattern = re.compile(r'^(\d+)$')
def parse_semver(constraint):
    # fix latest key word not parsing
    if constraint.endswith('latest'):
        constraint = '*'.join(constraint.rsplit('latest', 1))

    # fix constraint not assuming @7 means @7.*
    matches = patch_pattern.findall(constraint)
    if matches:
        constraint = f'{matches[-1]}.*'.join(constraint.rsplit(matches[-1], 1))

    return parse_constraint(constraint)

# return a list of semvers sorted in order
def sort_versions(items, reverse=False):
    def key(item):
        try:
            return parse_semver(item)
        except exceptions.ParseConstraintError:
            return parse_semver('0.0.0')
    return sorted(items, key=key, reverse=reverse)

# cmp(a, b) should returns true if a is less than b else false
def bisect(a, x, cmp, lo=0, hi=None):
    if lo < 0:
        raise ValueError('lo must be non-negative')
    if hi is None:
        hi = len(a)
    while lo < hi:
        mid = (lo + hi) // 2
        if cmp(x, a[mid]):
            hi = mid
        else:
            lo = mid + 1
    return lo
