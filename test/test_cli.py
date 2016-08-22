import unittest
from src.cli import create_parser


class TestCLI(unittest.TestCase):

    def setUp(self):
        self.parser = create_parser()

    def test_parser_default(self):

        args = self.parser.parse_args([])
        self.assertEqual('.', args.directory)
        self.assertEqual(True, args.recursive)
        self.assertEqual(False, args.overwrite)
        self.assertEqual(False, args.verbose)

    def test_parser_directory(self):

        args = self.parser.parse_args(['directory'])
        self.assertEqual('directory', args.directory)

    def test_parser_no_recursive(self):
        args = self.parser.parse_args(['--no-recursive'])
        self.assertEqual(False, args.recursive)

    def test_parser_overwrite(self):
        args = self.parser.parse_args(['--overwrite'])
        self.assertEqual(True, args.overwrite)

    def test_parser_verbose(self):
        args = self.parser.parse_args(['--verbose'])
        self.assertEqual(True, args.verbose)
