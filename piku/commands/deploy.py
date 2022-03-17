from piku.core import config, device


def deploy_command(args):
    # get device
    drive = args.device or device.find_device_path()

    # check that we are in a piku project directory
    if not config.valid():
        print('Refusing to deploy, unable to find piku project in current directory.')
        return

    # check that we have a device found or specified
    if not drive:
        print('Unable find a device and deploy, please specify a device to deploy to.')
        return

    # check that device size and name are as expected to reduce chances of loading onto wrong device
    if not device.has_correct_size(drive):
        print('Refusing to deploy, specified CircuitPython drive is larger than expected (~2MB).')
        return
    if not device.has_correct_label(drive):
        print('Refusing to deploy, expected device to have "circuitpy" in path.')
        return

    # confirm deploy
    if not args.yes:
        print(f'Are you sure you want to deploy to device: {drive}?')
        print('WARNING THIS WILL REMOVE ALL OTHER FILES FROM THE DEVICE! PLEASE BE CAREFUL!')
        response = input('Are you sure? [y/n] ').lower()
        if response not in ['y', 'yes']:
            print('Exiting')
            return

    # backup device files before deploy
    print(f'Backing up device files from {drive} to {config.backup_path}...')
    device.backup(drive, config.backup_path)

    # synchronize files to device
    print(f'Deploying project to device {drive}...')
    device.deploy(drive)

    print('Done')
