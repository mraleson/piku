import os
from piku.core import config, modules


def add_command(args):
    module = args.module.lower()

    # check if module already exists
    if config.get('dependencies', module):
        print(f'Module {module} already added to project. To reinstall, remove the module and add it again.')
        return

    # find module in current bundle
    bundle = config.get('general', 'circuitpython')
    source = args.source or modules.find(module, bundle).get('path')
    if not source:
        print(f'Unable to find source for requested module: {module}')
        suggestions = modules.suggest(module, bundle)
        if suggestions:
            print('Did you mean')
            for suggestion in suggestions:
                print(f' * {suggestion}')
        return

    # copy or download module
    destination = os.path.join(config.get('system', 'source', './source'), 'lib')
    path = modules.aquire(source, destination)
    if not path:
        print(f'Unable to download or copy requested module: {module} from {source}')
        return

    # save module in package.toml
    config.set('dependencies', module, modules.find(module, bundle).get('version'))
