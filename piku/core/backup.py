import os
import shutil
from time import time
from piku.core import config


def backup(device):
    # backup drive contents
    os.makedirs(config.backup_path, exist_ok=True)
    timestamp = int(time() * 1000)
    backup_path = os.path.join(config.backup_path, str(timestamp))
    shutil.copytree(device, backup_path)

    # remove old backups (keep the most recent 10)
    dirs = os.listdir(config.backup_path)
    dirs.sort(key=lambda x: -int(x))
    for dir in dirs[10:]:
        shutil.rmtree(os.path.join(config.backup_path, dir))
