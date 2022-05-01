import os
import shutil
import filecmp
import tempfile
import pytest
from piku import __version__
from piku.core.utils import sync


# helpers
temp_dir = tempfile.gettempdir()

def make_dir(base, dir=''):
    os.makedirs(os.path.join(base, dir), exist_ok=True)

def make_file(base, path, contents):
    full_path = os.path.join(base, path)
    dir = os.path.dirname(full_path)
    if dir: make_dir(dir)
    with open(full_path, 'w', encoding='utf-8') as f:
        f.write(contents)

def assert_match(a_base, a, b_base, b):
    assert filecmp.cmp(os.path.join(a_base, a), os.path.join(b_base, b), shallow=True), \
        f'Expected files or dirs {a} and {b} to match.'

def assert_contents(base, path, contents):
    p = os.path.join(base, path)
    with open(p, 'r', encoding='utf-8') as f:
        assert f.read() == contents

def assert_exists(base, path):
    p = os.path.join(base, path)
    assert os.path.isfile(p) or os.path.isdir(p), \
        f'Expected file or dir {p} to exist.'

def assert_missing(base, path):
    p = os.path.join(base, path)
    assert not os.path.isfile(p) and not os.path.isdir(p), \
        f'Expected file or dir {p} to exist.'


# fixtures
@pytest.fixture
def example_files():

    # make source dir
    src = os.path.join(temp_dir, 'piku/src')
    make_dir(src)
    make_file(src, 'a.txt', 'a')
    make_file(src, 'b/b.txt', 'b')
    make_file(src, 'c.txt', 'c')
    make_file(src, 'd.txt', 'd')
    make_file(src, 'i.txt', 'i')
    make_dir(src, 'empty')

    # make destination dir
    dst = os.path.join(temp_dir, 'piku/dst')
    make_dir(dst)
    make_file(dst, 'a.txt', 'a')
    make_file(dst, 'b/b.txt', 'b')
    make_file(dst, 'd.txt', 'bogus')
    make_file(dst, 'i.txt', 'dont copy over me')
    make_file(dst, 'keep/keep.txt', 'dont remove me')
    make_file(dst, '.ignore_me', 'dont remove me')
    make_dir(dst, 'empty_to_remove')

    yield (src, dst)

    # clean up
    shutil.rmtree(os.path.join(temp_dir, 'piku'))


# tests
def test_sync(example_files):
    src, dst = example_files
    sync(src, dst, exclude=['i.txt', 'keep/keep.txt', '.*'])
    assert_match(src, 'a.txt', dst, 'a.txt')
    assert_match(src, 'b/b.txt', dst, 'a.txt')
    assert_match(src, 'c.txt', dst, 'c.txt')
    assert_match(src, 'd.txt', dst, 'd.txt')
    assert_exists(dst, 'empty')
    assert_missing(dst, 'z.txt')
    assert_missing(dst, 'empty_to_remove')

    assert_exists(dst, 'i.txt')
    assert_contents(dst, 'i.txt', 'dont copy over me')
    assert_exists(dst, 'keep/keep.txt')
    assert_exists(dst, '.ignore_me')
    assert_contents(dst, 'keep/keep.txt', 'dont remove me')
