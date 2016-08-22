import unittest
import os
import subprocess
import shutil
import logging
import sys
import six
from src.svn_ignore import SVNIgnore


class TestSVNIgnore(unittest.TestCase):

    def setUp(self):
        """Checkout the SVN repository"""

        logging.basicConfig(stream=sys.stdout, format='%(levelname)s: %(message)s', level=logging.WARNING)
        self.repository_path = os.path.abspath(os.path.dirname(__file__) + '/resources/repository')
        self.checkout_path = os.path.abspath(os.path.dirname(__file__) + '/resources/checkout')

        # Clear the checkout
        if os.path.isdir(self.checkout_path):
            shutil.rmtree(self.checkout_path)

        # Checkout SVN
        process = subprocess.Popen(
            [
                'svn',
                'checkout',
                'file://{}'.format(self.repository_path),
                self.checkout_path,
                '--non-interactive'
            ],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        ).communicate()

        if process[1]:
            raise Exception('Error while doing checkout: {}'.format(process[1]))

        self.svn_ignore = SVNIgnore(
           directory=self.checkout_path
        )

    def tearDown(self):
        """Clear the checkout directory"""

        if os.path.isdir(self.checkout_path):
            shutil.rmtree(self.checkout_path)

    def test_get_ignores_from_file(self):
        """Check ignores from file"""

        ignores = self.svn_ignore.get_ignores_from_file(self.checkout_path)
        six.assertCountEqual(self, [
            'VALUE1'
        ], ignores)

    def test_get_ignores_from_file_with_comments(self):
        """Check retrieving ignores from file without removal of comments"""

        ignores = self.svn_ignore.get_ignores_from_file(self.checkout_path, remove_comments=False)
        six.assertCountEqual(self, [
            'VALUE1',
            '#comment'
        ], ignores)

    def test_add_exceptions(self):
        """Check if exceptions (The lines starting with !) also work"""

        path = os.path.join(self.checkout_path, 'directory_exception')

        open(os.path.join(path, 'exception.txt'), 'w+').close()

        self.svn_ignore.add_exceptions(path, [
            '*.txt',
            '!exception.txt'
        ])

        output = subprocess.check_output([
            'svn',
            'status'
        ], cwd=path)

        # Check if the file was added
        self.assertEqual('A       exception.txt\n', output.decode())

    def test_add_exceptions_recursive(self):
        """ Make sure we add the exceptions recursively as well"""

        path = os.path.join(self.checkout_path, 'directory_exception')

        # Create the child directory
        os.mkdir(os.path.join(path, 'child'))
        subprocess.check_output([
            'svn',
            'add',
            os.path.join(path, 'child')
        ])

        open(os.path.join(path, 'child', 'exception.txt'), 'w+').close()

        self.svn_ignore.add_exceptions(path, [
            '*.txt',
            '!**/exception.txt'
        ])

        output = subprocess.check_output([
            'svn',
            'status'
        ], cwd=path)

        self.assertEqual('A       child\nA       child/exception.txt\n', output.decode())

    def test_add_exception_recursive_without_parent(self):
        """ Make sure we don't add exceptions for directories that have not been added yet"""

        path = os.path.join(self.checkout_path, 'directory_exception')

        # Create the child directory
        os.mkdir(os.path.join(path, 'child'))

        open(os.path.join(path, 'child', 'exception.txt'), 'w+').close()

        self.svn_ignore.add_exceptions(path, [
            '*.txt',
            '!**/exception.txt'
        ])

        output = subprocess.check_output([
            'svn',
            'status'
        ], cwd=path)

        self.assertEqual('?       child\n', output.decode())


    def test_add_exception_on_already_added_file(self):
        """Make sure that when an exception is already added it does not raise an error"""

        path = os.path.join(self.checkout_path, 'directory_exception')

        open(os.path.join(path, 'exception.txt'), 'w+').close()

        self.svn_ignore.add_exceptions(path, [
            '*.txt',
            '!exception.txt'
        ])

        self.svn_ignore.add_exceptions(path, [
            '*.txt',
            '!exception.txt'
        ])

    def test_get_existing_ignores(self):
        """Test getting ignores from the properties"""

        ignores = self.svn_ignore.get_existing_ignores(os.path.join(self.checkout_path, 'directory_props'))
        six.assertCountEqual(self, [
            'EXISTING_VALUE'
        ], ignores)

    def test_get_existing_ignores_empty(self):
        """Test getting ignores from properties when the property is empty"""

        ignores = self.svn_ignore.get_existing_ignores(os.path.join(self.checkout_path, 'directory'))
        six.assertCountEqual(self, [], ignores)

    def test_set_ignore(self):
        """ Test setting the ignore property"""

        self.svn_ignore.set_ignores(self.checkout_path, ['VALUE1'])

        ignores = self.svn_ignore.get_existing_ignores(self.checkout_path)
        six.assertCountEqual(self, ['VALUE1'], ignores)

    def test_apply(self):
        """Test the apply with default values"""

        self.svn_ignore.apply()

        ignores = self.svn_ignore.get_existing_ignores(self.checkout_path)
        six.assertCountEqual(self, ['VALUE1'], ignores)

        ignores = self.svn_ignore.get_existing_ignores(os.path.join(self.checkout_path, 'directory'))
        six.assertCountEqual(self, ['VALUE2', 'VALUE1'], ignores)

        ignores = self.svn_ignore.get_existing_ignores(os.path.join(self.checkout_path, 'directory_props'))
        six.assertCountEqual(self, ['EXISTING_VALUE', 'VALUE1'], ignores)

    def test_apply_exception(self):
        """Check if exceptions are applied"""

        open(os.path.join(self.checkout_path, 'directory_exception', 'exception.txt'), 'w+').close()

        self.svn_ignore.apply()

        ignores = self.svn_ignore.get_existing_ignores(os.path.join(self.checkout_path, 'directory_exception'))
        six.assertCountEqual(self, ['VALUE1', '*.txt'], ignores)

        output = subprocess.check_output([
            'svn',
            'status'
        ], cwd=self.checkout_path)

        # Check if the file was added
        self.assertIn('A       directory_exception/exception.txt', output.decode().splitlines())

    def test_apply_overwrite(self):
        """Test the apply with overwrite enabled"""

        self.svn_ignore.overwrite = True
        self.svn_ignore.apply()

        ignores = self.svn_ignore.get_existing_ignores(self.checkout_path)
        six.assertCountEqual(self, ['VALUE1'], ignores)

        ignores = self.svn_ignore.get_existing_ignores(os.path.join(self.checkout_path, 'directory'))
        six.assertCountEqual(self, ['VALUE2', 'VALUE1'], ignores)

        ignores = self.svn_ignore.get_existing_ignores(os.path.join(self.checkout_path, 'directory_props'))
        six.assertCountEqual(self, ['VALUE1'], ignores)

    def test_apply_no_recursive(self):
        """Test apply with recursive disabled"""
        self.svn_ignore.recursive = False
        self.svn_ignore.apply()

        ignores = self.svn_ignore.get_existing_ignores(self.checkout_path)
        six.assertCountEqual(self, ['VALUE1'], ignores)

        ignores = self.svn_ignore.get_existing_ignores(os.path.join(self.checkout_path, 'directory'))
        six.assertCountEqual(self, ['VALUE2'], ignores)

        ignores = self.svn_ignore.get_existing_ignores(os.path.join(self.checkout_path, 'directory_props'))
        six.assertCountEqual(self, ['EXISTING_VALUE'], ignores)

if __name__ == '__main__':
    unittest.main()



