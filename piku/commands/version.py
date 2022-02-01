try:
    from importlib import metadata
except ImportError: # for Python<3.8
    import importlib_metadata as metadata


def get_version():
    return metadata.version('piku')

def version_command(args):
    print(get_version())
