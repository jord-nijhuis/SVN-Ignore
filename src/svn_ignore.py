import os
import subprocess
import logging

class SVNIgnore:

    def __init__(self, recursive=True, directory='.', ignore_file='.svnignore', overwrite = False):
        """

        :param recursive: Apply the ignore file also to the children of the directory
        :param directory: The initial directory to start
        :param ignore_file: The name of the ignore file to look for
        :param overwrite: Overwrite the already existing values
        """
        self.logger = logging.getLogger('svn-ignore')
        self.recursive = recursive
        self.directory = directory
        self.ignore_file = ignore_file
        self.overwrite = overwrite


    def apply(self):
        """Applies the given svn ignore
        """

        if(not os.path.isdir(self.directory)):
            raise Exception('Directory {} does not exist'.format(self.directory))

        for directory, sub_directories, files in os.walk(self.directory, topdown = True):

            if '.svn' in sub_directories:
                sub_directories.remove('.svn')

            #Read existing ignores
            try:
                if(not self.overwrite):
                    existing_ignores = self.get_existing_ignores(directory)
                else:
                    existing_ignores = []
            except Exception as exception:
                self.logger.error('Could not read existing ignores from %s: %s', directory, exception.message)
                return

            #Read ignores from file
            if self.ignore_file in files:
                try:
                    ignores_from_file = self.get_ignores_from_file(directory)
                except Exception as exception:
                    self.logger.error(
                        'Could not read ignores from %s: %s',
                        os.path.join(directory, self.ignore_file),
                        exception.message
                    )

                    return
            else:
                ignores_from_file = []

            # Recursive
            # We cannot do recursive by simply passing --recursive along as it would destroy already existing properties
            if(self.recursive):
                try:
                    ignores_from_parent = self.get_existing_ignores(os.path.join(directory, '..'))
                except Exception as exception:
                    self.logger.error(
                        'Could not read ignores from parent directory of %s: %s',
                        os.path.join(directory, self.ignore_file),
                        exception.message
                    )
                    return
            else:
                ignores_from_parent = []

            # Combine ignore files
            ignores = set(ignores_from_file + existing_ignores + ignores_from_parent)

            #apply config
            try:
                self.set_ignores(directory, ignores)
            except Exception as exception:
                self.logger.error('Could not write ignores to %s: %s', directory, exception)




    def get_existing_ignores(self, directory):
        """ Get the existing ignores from a directory

        :param directory: The directory to get the existing ignores from
        :return: A list containing all the ignore rules
        """

        process =  subprocess.Popen([
            'svn',
            'propget',
            'svn:ignore',
            directory
        ],
        cwd=directory,
        stderr=subprocess.PIPE,
        stdout=subprocess.PIPE,
        ).communicate()

        existing_ignores = process[0].decode().splitlines()

        #Remove newlines
        existing_ignores = list(filter(None, existing_ignores))

        self.logger.info('Found existing ignores: {}'.format(existing_ignores))

        return existing_ignores

    def get_ignores_from_file(self, directory, removeComments = True):
        """Get the ignores from the ignore file in the directory

        :param directory:  The directory to get the ignores from
        :return: A list containing the ignores
        """
        path = os.path.join(directory, self.ignore_file)
        f = open(path, 'r')
        new_ignores = f.read().splitlines()
        f.close()

        if removeComments:
            new_ignores = list(filter(
                lambda item: not item.startswith("#"),
                new_ignores
            ))

        #Remove newlines
        new_ignores = list(filter(None, new_ignores))

        self.logger.info('Found ignores in {}: {}'.format(path, new_ignores))

        return new_ignores

    def set_ignores(self, directory, ignores):
        """ Set the ignores for a directory

        :param directory: The directory to set the ignores for
        :param ignores: A list containing the ignores
        """
        self.logger.info('Applying ignore to directory {}'.format(directory))

        process = subprocess.Popen([
            'svn',
            'propset',
            'svn:ignore',
            '\n'.join(ignores),
            '.'
        ],
            cwd=directory,
            stderr=subprocess.PIPE,
            stdout=subprocess.PIPE,
        ).communicate()

        if process[1]:
            raise Exception('Error while setting svn:ignore property: {}'.format(process[1]))

