#!/usr/bin/env python
from setuptools import setup

setup(
	name='SVN-Ignore',
	py_modules=['sr', 'src.index'],
    version='1.0.4',
    description='An utility that provides .svnignore functionality similar to GIT',
    long_description=open('README.md').read(),
    author='Jord Nijhuis',
    author_email='jord@nijhuis.me',
	url='https://github.com/Sidesplitter/SVN-Ignore',
	license='MIT',
	classifiers= [
		'License :: OSI Approved :: MIT License',
		'Topic :: Software Development :: Version Control',
		'Development Status :: 5 - Production/Stable',
		'Programming Language :: Python :: 3.5'
	],
   	include_package_data=True,
	entry_points = {
        'console_scripts': [
        	'svn-ignore = src.index:main'
        ],
    },
    keywords='svn cli util utils'
)