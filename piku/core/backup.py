import os
import shutil
from time import time
from piku.core import config


def backup(src, dst):
    # backup drive contents
    os.makedirs(dst, exist_ok=True)
    timestamp = int(time() * 1000)
    backup_path = os.path.join(dst, str(timestamp))
    shutil.copytree(src, backup_path)

    # remove old backups (keep the most recent 10)
    dirs = os.listdir(dst)
    dirs.sort(key=lambda x: -int(x))
    for dir in dirs[10:]:
        shutil.rmtree(os.path.join(dst, dir))
