# pylint:disable=line-too-long

import shutil
import platform
import os                                   # pylint:disable=unused-import
from subprocess import check_output         # pylint:disable=unused-import
from piku.core import config, device, utils # pylint:disable=unused-import
from piku.core.sync import sync             # pylint:disable=unused-import
from piku.core.backup import backup         # pylint:disable=unused-import


DEFAULT_BOARD_CAPACITY = 3E6

DEFAULT_VOLUME_LABEL = "circuitpy"

def _display_board_type_warning(path: str) -> None:
    print('WARNING: "{}" does not appear to be a CircuitPython/MicroPython board'.format(path))
    print('')
    print('- Download Circuit Python from circuitpython.org')
    print('- Download MicroPython from micropython.org')
    print('')

    
def warning_prompt(message: str) -> bool:
    print(message)
    print('WARNING THIS WILL REMOVE ALL OTHER FILES FROM THE DEVICE! PLEASE BE CAREFUL!')
    response = input('Are you sure? [y/n] ').lower().strip()
    return response in ['y', 'yes']

  
def has_correct_size(path, default_board_capacity=DEFAULT_BOARD_CAPACITY):
    total, _, _ = shutil.disk_usage(path)
    return 0 < total < default_board_capacity


def has_correct_label(path, expected_label=DEFAULT_VOLUME_LABEL):
    if platform.system() == 'Windows':
        drive = path.split(':')[0]
        output = check_output(f'cmd /c vol {drive}:'.split()).decode()
        label = output.split('\r\n')[0].split(' ').pop()
        return expected_label in label.lower()
    return expected_label in path.lower()


def find_device_path(expected_label=DEFAULT_VOLUME_LABEL):
    if platform.system() == 'Windows':
        output = check_output('wmic logicaldisk where drivetype=2 get DeviceId , VolumeName'.split()).decode()
        drives = [
            line.split(' ')[0]
            for line in output.split('\r\n')
            if expected_label in line.lower()
        ]
        return drives[0] if drives else None
    if platform.system() == 'Linux':
        output = check_output('lsblk -l -o mountpoint,label,rm'.split()).decode()
        lines = [line.split() for line in output.split('\n')]
        drives = [
            line[0]
            for line in lines
            if len(line) == 3 and expected_label in line[1].lower() and line[2] == '1'
        ]
        return drives[0] if drives else None
    if platform.system() == 'Darwin':
        output = check_output('mount'.split()).decode()
        lines = [line.split() for line in output.split('\n')]
        drives = [
            line[2]
            for line in lines
            if len(line) > 4 and expected_label in line[2].lower()
        ]
        return drives[0] if drives else None
    return None

  def deploy(drive):
    print(f'Deploying project to device {drive}...')
    device.deploy(drive)
    print('Done')


def deploy_command(args):
  # check that we are in a piku project directory
    if not config.valid():
        print('Refusing to deploy, unable to find piku project in current directory.')
        return

  # get device
    source = config.get('tool.piku.source')
    expected_label = DEFAULT_VOLUME_LABEL
    device = args.device or find_device_path(expected_label)
    user_confirmed = False

    drive = args.device or device.find_device_path()

    # check that we have a device found or specified
    if not drive:
        print('Unable find a device and deploy, please specify a device to deploy to.')
        return

    # check that device size and name are as expected to reduce chances of loading onto wrong device
    if not has_correct_size(device):
        print('Specified CircuitPython drive is larger than expected (~{:0d}MB).'.format(int(DEFAULT_BOARD_CAPACITY // 1E6)))
        if not warning_prompt(f'Are you sure you want to deploy to {device}?'):
            return
        user_confirmed = True
    if not has_correct_label(device, expected_label):
        print(f'Expected device to have {expected_label} in path.')
        if not warning_prompt(f'Are you sure you want to deploy to {device}?'):
            return
        user_confirmed = True

    # confirm deploy
    if not args.yes and not user_confirmed:
        if not warning_prompt(f'Are you sure you want to deploy to {device}?'):
            print('Exiting')
            return

    # backup device files before deploy
    print(f'Backing up device files from {drive} to {config.backup_path}...')
    device.backup(drive, config.backup_path)


    # synchronize files to device
    if not args.watch:
        deploy(drive)
        return

    # watch files and auto deploy
    utils.watch(config.get('source'), lambda: deploy(drive))
