#!/bin/python
import subprocess
import os
import sys
import argparse
import logging

def main():
	parser = argparse.ArgumentParser(description='An utility that provides .svnignore functionality similar to GIT')

	#Directory argument
	parser.add_argument(
		'directory',
		nargs='?', 
		type=str, 
		default='.', 
		help='The root directory. Default is the working directory.',
	)

	#Recurive argument
	parser.add_argument(
		'--no-recursive', 
		dest='recursive',
		action='store_false',
		help='Makes the ignore file not apliable child directories.',
		required=False,
		default=True
	)

	#Overwrite argument
	parser.add_argument(
		'--overwrite',
		action='store_true',
		default=False,
		help='Overwrite the existing ignore property. Applies the no-recursive option.',
		required=False
	)

	#Verbose argument
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
	args = parser.parse_args()

	logging.basicConfig(stream=sys.stdout, format='%(levelname)s: %(message)s')
	logger = logging.getLogger('svnignore')

	if(args.verbose):
		logger.setLevel(logging.DEBUG)
	else:
		logger.setLevel(logging.INFO)

	recursive = ('', '--recursive')[args.recursive]

	#Walk over directories
	for directory, subDirectories, files in os.walk(args.directory):

		#Found a ignore file
		if args.ignore_file in files:

			logger.info('Found ignore file in %s', directory)

			#Get the old ignore
			if(args.overwrite):
				oldIgnore = []
			else:
				oldIgnore = str(subprocess.check_output([
					'svn',
					'propget',
					'svn:ignore',
				])).encode('utf-8').splitlines()

			logger.debug('Old Ignore:\n\t' + '\n\t'.join(oldIgnore))

			#Get the new ignore
			file = open(os.path.join(directory, args.ignore_file), 'r')
			newIgnore = file.read().splitlines()
			file.close()

			logger.debug('New Ignore:\n\t' + '\n\t'.join(newIgnore))

			#Combine ignore files
			ignore = set(oldIgnore + newIgnore)

			#Remove comments
			ignore = list(filter(
				lambda item: item.startswith("#") == False,
				ignore
			))

			#Remove empty lines
			ignore = list(filter(None, ignore))

			logger.debug('Final ignore:\n\t' + '\n\t'.join(ignore))

			process = subprocess.Popen([
					'svn', 
					'propset', 
					'svn:ignore',
					'\n'.join(ignore), 
					'.',
					recursive, 
				],
				cwd=directory,
				stderr=subprocess.PIPE,
				stdout=subprocess.PIPE,
			)

			if(process.communicate()[1]):
				logger.error(str(process.communicate()[1]).encode('utf-8'))