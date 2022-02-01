import os
import shutil
import hashlib
import fnmatch


# helpers
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

def different(a, b):
    if os.path.isdir(a) and os.path.isdir(b):
        return False
    if os.path.isfile(a) and os.path.isfile(b):
        return os.path.getsize(a) != os.path.getsize(b) or checksum(a) != checksum(b)
    return True

def ignored(path, patterns):
    for pattern in patterns:
        if fnmatch.filter([path], pattern):
            return True
    return False


# synchronize
def sync(src_dir, dst_dir, exclude=None, verbosity=1):
    src_tree = tree(src_dir)
    dst_tree = tree(dst_dir)
    to_rm = dst_tree - src_tree
    to_ignore = {os.path.join(dst_dir, i) for i in (exclude or [])}

    # create any missing dir and copy over missing files (sorted so dirs are created files)
    for path in sorted(src_tree):
        src = os.path.join(src_dir, path)
        dst = os.path.join(dst_dir, path)
        if ignored(dst, to_ignore):
            if verbosity > 1: print(f'* Ignoring copy {dst}')
        elif different(src, dst):
            if verbosity > 0: print(f'* Copying {src} to {dst}')
            copy(src, dst)
        else:
            if verbosity > 1: print(f'* Files {src} {dst} are the same')

    # remove files that are in destination but not in source (reverse sorted so files rm before dirs)
    for path in reversed(sorted(to_rm)):
        full_path = os.path.join(dst_dir, path)
        if ignored(full_path, to_ignore):
            if verbosity > 1: print(f'* Ignoring remove {full_path}')
        else:
            if verbosity > 0: print(f'* Removing {full_path}')
            remove(full_path)
