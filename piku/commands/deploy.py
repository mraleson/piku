import shutil
from piku.core import config
from piku.core.sync import sync
from piku.core.backup import backup


def deploy_command(args):
    # get device
    source = config.get('system', 'source', './project')
    device = config.get('system', 'device')

    # check that device size and name are as expected to reduce chances of loading onto wrong device
    total, used, free = shutil.disk_usage(device)
    assert total < 3E6, 'Specified CircuitPython drive is larger than expected (~2MB).'
    assert 'circuitpy' in device.lower(), 'Expected device to have "circuitpy" in path.'

    # backup device files before deploy
    print('Backing up device files...')
    backup(device)

    # synchronize files to device
    print('Deploying project to device...')
    sync(source, device, exclude=['boot_out.txt', '.*'], verbosity=1)

    print('Done')
