import os
import shutil
import platform
from subprocess import check_output
from time import time
from piku.core import utils, config


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

def deploy(device):
    source = config.get('tool.piku.source')
    utils.sync(source, device, exclude=['boot_out.txt', '.*'], verbosity=1)

def has_correct_size(path):
    total, used, free = shutil.disk_usage(path)
    return 0 < total < 3E6

def has_correct_label(path):
    if platform.system() == 'Windows':
        drive = path.split(':')[0]
        output = check_output(f'cmd /c vol {drive}:'.split()).decode()
        label = output.split('\r\n')[0].split(' ').pop()
        return 'circuitpy' in label.lower()
    return 'circuitpy' in path.lower()

def find_device_path():
    if platform.system() == 'Windows':
        output = check_output('wmic logicaldisk where drivetype=2 get DeviceId , VolumeName'.split()).decode()
        drives = [
            line.split(' ')[0]
            for line in output.split('\r\n')
            if 'circuitpy' in line.lower()
        ]
        return drives[0] if drives else None
    if platform.system() == 'Linux':
        output = check_output('lsblk -l -o mountpoint,label,rm'.split()).decode()
        lines = [line.split() for line in output.split('\n')]
        drives = [
            line[0]
            for line in lines
            if len(line) == 3 and 'circuitpy' in line[1].lower() and line[2] == '1'
        ]
        return drives[0] if drives else None
    if platform.system() == 'Darwin':
        output = check_output('mount'.split()).decode()
        lines = [line.split() for line in output.split('\n')]
        drives = [
            line[2]
            for line in lines
            if len(line) > 4 and 'circuitpy' in line[2].lower()
        ]
        return drives[0] if drives else None
    return None
