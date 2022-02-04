from piku.core import config, modules


def install_command(args):
    deps = config.get('tool.piku.dependencies')
    for name, version in deps.items():

        # determind module source
        if version.startswith('file:'):
            source = version
        else:
            source = f'{name}@{version}'

        # decode module
        module, type, path, version = modules.decode(source)

        # copy or download module
        print(f'Acquiring {module}...')
        if not modules.aquire(path):
            print(f'Unable to aquire requested module: {module}')
            return
