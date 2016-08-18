#!/bin/python
import sys
import argparse
import logging
from src.svn_ignore import SVNIgnore

def create_parser():
    parser = argparse.ArgumentParser(description='An utility that provides .svnignore functionality similar to GIT')

    # Directory argument
    parser.add_argument(
        'directory',
        nargs='?',
        type=str,
        default='.',
        help='The root directory. Default is the working directory.',
    )

    # Recursive argument
    parser.add_argument(
        '--no-recursive',
        dest='recursive',
        action='store_false',
        help='Makes the ignore file not apliable child directories.',
        required=False,
        default=True
    )

    # Overwrite argument
    parser.add_argument(
        '--overwrite',
        action='store_true',
        default=False,
        help='Overwrite the existing ignore property.',
        required=False
    )

    # Verbose argument
    parser.add_argument(
        '--verbose',
        action='store_true',
        default=False,
        help='Turn verbose mode on.',
        required=False
    )

    parser.add_argument(
        '--ignore-file',
        type=str,
        default='.svnignore',
        help='The ignore file to look for. Default is .svnignore.'
    )

    return parser


def main():
    parser = create_parser()

    args = parser.parse_args()

    if args.verbose:
        level = logging.DEBUG
    else:
        level = logging.WARNING

    logging.basicConfig(stream=sys.stdout, format='%(levelname)s: %(message)s', level=level)

    svn_ignore = SVNIgnore(
        directory=args.directory,
        recursive=args.recursive,
        overwrite=args.overwrite,
        ignore_file=args.ignore_file
    )

    svn_ignore.apply()

if __name__ == '__main__':
    main()