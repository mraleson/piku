import os
from piku.core import config, utils
from piku.core.index import index


# find a module
def find(module, bundle=None):
    bundle = bundle or config.get('tool.piku.circuitpython')
    return index(bundle).get(module)

# suggest a module from index lexically similar to the one provided
def suggest(module, bundle=None):
    bundle = bundle or config.get('tool.piku.circuitpython')
    return utils.similar(module, index(bundle).keys())

# copy a module from source to project library
def aquire(source, project_path=None):
    project_path = project_path or config.get('tool.piku.source')
    library_path = os.path.join(project_path, 'lib')
    if os.path.isdir(project_path):
        os.makedirs(library_path, exist_ok=True)
    return utils.copy(source, library_path)

# remove a module from project library
def remove(module, library_path=None):
    library_path = library_path or os.path.join(config.get('tool.piku.source'), 'lib')
    for path in os.listdir(library_path):
        if path in [module, f'{module}.mpy']:
            utils.remove(os.path.join(library_path, path))
            return True
    return False

# decode module name and source from request module path
def decode(module):

    # module from local file
    if module.startswith('file:'):
        path = module[5:]
        name = os.path.splitext(os.path.basename(path))[0]
        type = 'file'
        version = module

    # module from index via semver
    else:
        bundle = config.get('tool.piku.circuitpython')
        parts = module.split('@')
        name = parts[0].lower()
        type = 'index'
        path = find(name)
        if len(parts) > 1:
            version = parts[1]
        else:
            version = f'~{bundle}'
    return (name, type, path, version)
