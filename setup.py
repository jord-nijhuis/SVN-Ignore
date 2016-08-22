#!/usr/bin/env python
from setuptools import setup

with open('README.rst') as f:
    long_description = f.read()

setup(
    name='SVN-Ignore',
    py_modules=['sr', 'src.cli', 'src.svn_igno re'],
    version='1.2.1',
    description='An utility that provides .svnignore functionality similar to GIT',
    long_description=long_description,
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
    setup_requires=['pytest-runner'],
    install_requires=['glob2'],
    tests_require=['pytest', 'six'],
)
