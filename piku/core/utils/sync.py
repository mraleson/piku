import os
import fnmatch
from piku.core.utils import checksum, tree, copy, remove

# helpers
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


# fsync all files to prevent a late OS flush to device triggering a reload
def fsync_dir(dir_path):
    print(f'fsync {dir_path}')
    # sync dir meta data
    try:
        dir_fd = os.open(dir_path, os.O_RDONLY)
        os.fsync(dir_fd)
    finally:
        os.close(dir_fd)

    # sync dir
    for root, dirs, files in os.walk(dir_path, onerror=None):

        # sync files
        for file in files:
            path = os.path.join(root, file)
            with open(path, 'rb') as f:
                os.fsync(f.fileno())

        # sync dirs
        for dir in dirs:
            path = os.path.join(root, dir)
            fsync_dir(path)

# synchronize
def sync(src_dir, dst_dir, exclude=None, verbosity=1):
    src_tree = tree(src_dir)
    dst_tree = tree(dst_dir)
    to_rm = dst_tree - src_tree
    to_ignore = {os.path.join(dst_dir, i) for i in (exclude or [])}
    changes_detected = False

    # create any missing dir and copy over missing files (sorted so dirs are created files)
    for path in sorted(src_tree):
        src = os.path.join(src_dir, path)
        dst = os.path.join(dst_dir, path)
        if ignored(dst, to_ignore):
            if verbosity > 1:
                print(f'* Ignoring copy {dst}')
        elif different(src, dst):
            if verbosity > 0:
                print(f'* Copying {src} to {dst}')
            copy(src, dst, recursive=False)
            changes_detected = True
        else:
            if verbosity > 1:
                print(f'* Files {src} {dst} are the same')

    # remove files that are in destination but not in source (reverse sorted so files rm before dirs)
    for path in reversed(sorted(to_rm)):
        full_path = os.path.join(dst_dir, path)
        if ignored(full_path, to_ignore):
            if verbosity > 1:
                print(f'* Ignoring remove {full_path}')
        else:
            if verbosity > 0:
                print(f'* Removing {full_path}')
            remove(full_path, recursive=False)
            changes_detected = True

    # sync file information to prevent delayed soft reboot on circuit python device
    fsync_dir(dst_dir)

    if verbosity > 0 and not changes_detected:
        print('Nothing to deploy, no source differences were detected.')
