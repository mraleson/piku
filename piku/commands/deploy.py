import shutil
import platform
from subprocess import check_output
from piku.core import config
from piku.core.sync import sync
from piku.core.backup import backup



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


def deploy_command(args):
    # get device
    source = config.get('tool.piku.source')
    device = args.device or find_device_path()

    # check that we have a device found or specified
    if not device:
        print('Unable find a device and deploy, please specify a device to deploy to.')
        return

    # check that device size and name are as expected to reduce chances of loading onto wrong device
    if not has_correct_size(device):
        print('Refusing to deploy, specified CircuitPython drive is larger than expected (~2MB).')
        return
    if not has_correct_label(device):
        print('Refusing to deploy, expected device to have "circuitpy" in path.')
        return

    # confirm deploy
    if not args.yes:
        print(f'Are you sure you want to deploy to device: {device}?')
        print('WARNING THIS WILL REMOVE ALL OTHER FILES FROM THE DEVICE! PLEASE BE CAREFUL!')
        response = input('Are you sure? [y/n] ').lower()
        if response not in ['y', 'yes']:
            print('Exiting')
            return

    # backup device files before deploy
    backup_path = config.backup_path
    print(f'Backing up device files from {device} to {backup_path}...')
    backup(device, backup_path)

    # synchronize files to device
    print(f'Deploying project to device {device}...')
    sync(source, device, exclude=['boot_out.txt', '.*'], verbosity=1)

    print('Done')
