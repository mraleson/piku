from piku.core import utils


def test_parse_semver():
    assert utils.parse_semver('1.0.0').is_strictly_lower(utils.parse_semver('~2'))
    assert not utils.parse_semver('2.0.0').is_strictly_lower(utils.parse_semver('*'))
    assert utils.parse_semver('2').allows(utils.parse_semver('2.0.0'))
    assert utils.parse_semver('~2').allows(utils.parse_semver('2.0.0'))
    assert utils.parse_semver('latest').allows(utils.parse_semver('1.0.0'))

def test_sort_semver():
    items = ['1.0.2', '1.0.0', '2.0.0', '1.0.10', '1.0.1-alpha', 'bogus', '1.0.1']
    assert utils.sort_versions(items) == ['bogus', '1.0.0', '1.0.1-alpha', '1.0.1', '1.0.2', '1.0.10', '2.0.0']

def test_binary_search():
    a = [10, 20, 30, 40, 40, 40, 50]
    cmp = lambda a, b: a < b
    assert utils.bisect(a, 40, cmp) == 6
    assert utils.bisect(a, 0, cmp) == 0

    a = ['0.0.0', '1.0.0', '1.0.0', '2.0.1', '2.0.1', '2.0.1', '3.9.1']
    cmp = lambda a, b: utils.parse_semver(a).is_strictly_lower(utils.parse_semver(b))
    assert utils.bisect(a, '0.0.0', cmp) == 1
    assert utils.bisect(a, '1.0.0', cmp) == 3
    assert utils.bisect(a, '*', cmp) == 7
    assert utils.bisect(a, '2.*', cmp) == 6
    assert utils.bisect(a, '~1', cmp) == 3
    assert utils.bisect(a, 'latest', cmp) == 7
