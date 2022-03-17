class PikuError(Exception):
    pass

class PackageNotFound(PikuError):
    pass

class VersionNotFound(PikuError):
    def __init__(self, package, version):
        super().__init__(f'{package} {version}')
