import os
import shutil
import platform
from time import time
from piku.core import utils


# perhaps im the future this is configurable along with the sync ignore/exclude patterns
backup_ignore_patterns = shutil.ignore_patterns(
    '.Trashes',
    '.Trashes/*',
    'System Volume Information',
    'System Volume Information/*',
    '.metadata_never_index',
    '.fseventsd',
    '*/._*'
)

def backup(src, dst):
    # backup drive contents
    os.makedirs(dst, exist_ok=True)
    timestamp = int(time() * 1000)
    backup_path = os.path.join(dst, str(timestamp))

    shutil.copytree(src, backup_path, ignore=backup_ignore_patterns)

    # remove old backups (keep the most recent 10)
    dirs = os.listdir(dst)
    dirs.sort(key=lambda x: -int(x))
    for dir in dirs[10:]:
        utils.remove(os.path.join(dst, dir))
