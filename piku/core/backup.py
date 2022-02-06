import os
import shutil
from time import time
import platform
from shutil import ignore_patterns


def backup(src, dst):
    # backup drive contents
    os.makedirs(dst, exist_ok=True)
    timestamp = int(time() * 1000)
    backup_path = os.path.join(dst, str(timestamp))

    if platform.system() == 'Darwin':
        shutil.copytree(
            src,
            backup_path,
            ignore=ignore_patterns(
                '.Trashes',
                '.Trashes/*',
                'System Volume Information',
                'System Volume Information/*',
                '.metadata_never_index',
                '.fseventsd',
                '*/._*',
            ),
        )
    else:
        shutil.copytree(src, backup_path)

    # remove old backups (keep the most recent 10)
    dirs = os.listdir(dst)
    dirs.sort(key=lambda x: -int(x))
    for dir in dirs[10:]:
        if platform.system() == "Darwin":
            shutil.rmtree(os.path.join(dst, dir), onerror=None, ignore_errors=True)
        else:
            shutil.rmtree(os.path.join(dst, dir))
