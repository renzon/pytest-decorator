import os
import shlex
import shutil
import sys
from tempfile import mkdtemp

from IPython.core import magic
from pytest import main as pytest_main

TEST_MODULE_NAME = '_ipytesttmp'


class TemporaryDirectory(object):
    def __enter__(self):
        self.path = mkdtemp()
        return self.path

    def __exit__(self, exc_type, exc_val, exc_tb):
        shutil.rmtree(self.path)


def pytest(line, cell):
    with TemporaryDirectory() as root:
        oldcwd = os.getcwd()
        os.chdir(root)
        tests_module_path = '{}.py'.format(TEST_MODULE_NAME)
        try:
            with open(tests_module_path, 'w') as test_file:
                test_file.write(cell)
            # args = shlex.split(line)
            os.environ['COLUMNS'] = '80'
            pytest_main([tests_module_path])
            if TEST_MODULE_NAME in sys.modules:
                del sys.modules[TEST_MODULE_NAME]
        finally:
            os.chdir(oldcwd)


def load_ipython_extension(ipython):
    magic.register_cell_magic(pytest)
