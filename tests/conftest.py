import pytest


def pytest_addoption(parser):
    parser.addoption(
        '--all', action='store_true', default=False, help='run all tests, including those marked as slow'
    )

def pytest_configure(config):
    config.addinivalue_line('markers', 'slow: mark test as slow to run')

def pytest_collection_modifyitems(config, items):
    if config.getoption('--all'):
        return
    skip_slow = pytest.mark.skip(reason='skipping slow tests, use --slow option to run')
    for item in items:
        if 'slow' in item.keywords:
            item.add_marker(skip_slow)
