from piku.core import config, modules


def add_command(args):
    # decode module
    module, type, path, version = modules.decode(args.module)

    # check if module already exists
    if config.get(f'tool.piku.dependencies.{module}'):
        print(f'Module {module} already added to project. To reinstall, remove the module and add it again.')
        return

    # suggest module if we can't find it in index
    if type == 'index' and not path:
        print(f'Unable to find source for requested module: {module}')
        suggestions = modules.suggest(module)
        if suggestions:
            print('Did you mean')
        for suggestion in suggestions:
            print(f' * {suggestion}')
        return

    # copy or download module
    print(f'Acquiring {module}...')
    if not modules.aquire(path):
        print(f'Unable to aquire requested module: {module}')
        return

    # save module in pyproject.toml
    config.set(f'tool.piku.dependencies.{module}', version)
