class PikuError(Exception):
    pass

class PackageIndexNotFound(PikuError):
    def __init__(self, circuitpython_version):
        super().__init__(f'No package index found for CircuitPython version {circuitpython_version}')

class PackageNotFound(PikuError):
    pass

class VersionNotFound(PikuError):
    def __init__(self, package, version):
        super().__init__(f'{package} {version}')
