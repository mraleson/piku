import shutil
from piku.core import config
from piku.core.sync import sync
from piku.core.backup import backup


def deploy_command(args):
    # get device
    source = config.get('system', 'source', './project')
    device = config.get('system', 'device')

    # check that device has been specified
    if not device:
        print('Unable to deploy, please specify a device to deploy to in your piku.toml file.')
        return

    # check that device size and name are as expected to reduce chances of loading onto wrong device
    total, used, free = shutil.disk_usage(device)
    if total > 3E6:
        print('Refusing to deploy, specified CircuitPython drive is larger than expected (~2MB).')
        return
    if'circuitpy' not in device.lower():
        print('Refusing to deploy, expected device to have "circuitpy" in path.')
        return

    # backup device files before deploy
    print('Backing up device files...')
    backup(device)

    # synchronize files to device
    print('Deploying project to device...')
    sync(source, device, exclude=['boot_out.txt', '.*'], verbosity=1)

    print('Done')
