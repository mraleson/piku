import os
from piku.core import config, modules, utils


def remove_command(args):
    module = args.module.lower()
    library = os.path.join(config.get('system', 'source', './project'), 'lib')

    # remove module from package.toml
    if not config.remove('dependencies', module):
        print(f'Unable to find matching module {module} in piku.toml')
        suggestions = utils.similar(module, config.get('dependencies').keys())
        if suggestions:
            print('Did you mean')
            for suggestion in suggestions:
                print(f' * {suggestion}')
        return

    # remove file from library
    if not modules.delete(module, library):
        print(f'Warning: Unable to find and delete matching file in source for module {module} in {library}')
