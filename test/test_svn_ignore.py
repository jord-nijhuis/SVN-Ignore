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
        self.repository_path = os.path.abspath('./test/resources/repository')
        self.checkout_path = os.path.abspath('./test/resources/checkout')

        # Clear the checkout
        if os.path.isdir(self.checkout_path):
            shutil.rmtree(self.checkout_path)

        #Checkout SVN
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

        ignores = self.svn_ignore.get_ignores_from_file(self.checkout_path, removeComments=False)
        six.assertCountEqual(self, [
            'VALUE1',
            '#comment'
        ], ignores)

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

        self.svn_ignore.apply()

        ignores = self.svn_ignore.get_existing_ignores(self.checkout_path)
        six.assertCountEqual(self, ['VALUE1'], ignores)

        ignores = self.svn_ignore.get_existing_ignores(os.path.join(self.checkout_path, 'directory'))
        six.assertCountEqual(self, ['VALUE2', 'VALUE1'], ignores)

        ignores = self.svn_ignore.get_existing_ignores(os.path.join(self.checkout_path, 'directory_props'))
        six.assertCountEqual(self, ['EXISTING_VALUE', 'VALUE1'], ignores)

    def test_apply_overwrite(self):
        self.svn_ignore.overwrite = True
        self.svn_ignore.apply()

        ignores = self.svn_ignore.get_existing_ignores(self.checkout_path)
        six.assertCountEqual(self, ['VALUE1'], ignores)

        ignores = self.svn_ignore.get_existing_ignores(os.path.join(self.checkout_path, 'directory'))
        six.assertCountEqual(self, ['VALUE2', 'VALUE1'], ignores)

        ignores = self.svn_ignore.get_existing_ignores(os.path.join(self.checkout_path, 'directory_props'))
        six.assertCountEqual(self, ['VALUE1'], ignores)

    def test_apply_no_recusrive(self):
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



