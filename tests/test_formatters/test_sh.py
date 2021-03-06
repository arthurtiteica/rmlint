from nose import with_setup
from tests.utils import *

import subprocess


@with_setup(usual_setup_func, usual_teardown_func)
def test_basic():
    create_file('xxx', 'a')
    create_file('xxx', 'b')

    create_file('yyy', 'dir_a/a')
    create_file('zzz', 'dir_a/b')

    create_file('zzz', 'dir_b/a')
    create_file('yyy', 'dir_b/b')

    create_file('', 'empty')

    create_file('aaa', 'aaa')
    create_link('aaa', 'link_aaa', symlink=True)
    os.remove(os.path.join(TESTDIR_NAME, 'aaa'))

    head, *data, footer = run_rmlint('-D -S a -o sh:{t}/rmlint.sh'.format(t=TESTDIR_NAME))
    # subprocess.call('cat ' + os.path.join(TESTDIR_NAME, 'rmlint.sh'), shell=True)

    assert footer['duplicate_sets'] == 3
    assert footer['total_lint_size'] == 9
    assert footer['total_files'] == 9
    assert footer['duplicates'] == 3

    # Dry run first; check if it did not accidentally delete something.
    text = subprocess.check_output([os.path.join(TESTDIR_NAME, 'rmlint.sh'), '-dn'])
    head, *data, footer = run_rmlint('-D -S a')
    assert footer['duplicate_sets'] == 3
    assert footer['total_lint_size'] == 9
    assert footer['total_files'] == 9
    assert footer['duplicates'] == 3

    text = subprocess.check_output([os.path.join(TESTDIR_NAME, 'rmlint.sh'), '-d'])
    head, *data, footer = run_rmlint('-D -S a')

    assert footer['duplicate_sets'] == 0
    assert footer['total_lint_size'] == 0
    assert footer['total_files'] == 3
    assert footer['duplicates'] == 0

    text = text.decode('utf-8')
    assert '/dir_a' in text
    assert '/a' in text
