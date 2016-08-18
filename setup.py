#!/usr/bin/env python
from setuptools import setup
import sys

def get_long_description():
    try:
        import pypandoc
        pypandoc.convert('README.md','rst',format='markdown', outputfile='README.rst')
        long_description = 'README.rst'

    except Exception:
        print('WARNING: Failed to convert README.md to rst, pypandoc was not present, using md')
        f = open('README.md')
        long_description = f.read()
        f.close()

    return long_description

setup(
    name='SVN-Ignore',
    py_modules=['sr', 'src.cli', 'src.svn_ignore'],
    version='1.1.1',
    description='An utility that provides .svnignore functionality similar to GIT',
    long_description=get_long_description(),
    author='Jord Nijhuis',
    author_email='jord@nijhuis.me',
    url='https://github.com/Sidesplitter/SVN-Ignore',
    license='MIT',
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Topic :: Software Development :: Version Control',
        'Development Status :: 5 - Production/Stable',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
    ],
    include_package_data=True,
    entry_points={
        'console_scripts': [
            'svn-ignore = src.cli:main'
        ],
    },
    keywords='svn cli util utils',
    setup_requires=['pytest-runner', 'pypandoc'],
    tests_require=['pytest', 'six'],
)
