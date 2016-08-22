SVN-Ignore
==========

.. image:: https://img.shields.io/pypi/v/svn-ignore.svg?maxAge=2592000
   :target: https://pypi.python.org/pypi/SVN-Ignore/
.. image:: https://travis-ci.org/Sidesplitter/SVN-Ignore.svg
   :target: https://travis-ci.org/Sidesplitter/SVN-Ignore/
.. image:: https://img.shields.io/pypi/pyversions/svn-ignore.svg?maxAge=2592000
   :target: https://pypi.python.org/pypi/SVN-Ignore/

An utility that provides .svnignore functionality similar to GIT.

Lets face it, the svn:ignore property is pretty poor in comparison to
GIT, it does not update itself when you add new files, exceptions are
not possible, and it cannot be specified in a single file. That's
exactly why this utility exists

Features that this utility provides: - A .svnignore file that lets you
specify which files should be ignored - The possibility to add
exceptions(Lines starting with !) to the SVN Ignore file - Updating the
svn:ignore property every time you add new files

Installation
------------

Make sure that you have SVN installed before you run SVN-Ignore, as it
requires the ``svn`` command.

To install SVN-Ignore, simply run: ``pip install svn-ingore``. After
that you can run ``svn-ignore`` on any directory

Usage
-----

Simply calling ``svn-ignore [directory]`` will run the utility. If the
directory is left empty, it will use the working directory.

Valid arguments:

-  ``--no-recursive``: Do not apply the .svnignore file to any of the
   children of the current directory
-  ``--overwrite``: Overwrite existing svn:ignore properties.
-  ``--ignore-file <file>``: The file to look for. Default is
   ``.svnigore``
-  ``--verbose``: Display verbose information
-  ``--help``: Display this information

Hook
----

Because of the way that the ``svn:ignore`` property works, this script
only applies the contents of ``.svnigore`` to files that exist at the
time of running. To make sure that the file also applies to newly added
files, the command needs to be rerun. An easy way to do this is with a
hook.

On the Client
~~~~~~~~~~~~~

Linux (Bash alias)
^^^^^^^^^^^^^^^^^^

The correct way to do this is by using a Bash alias. Create a file
somewhere with these contents:

::

    #!/bin/bash
    if [ $1 = 'commit' ]; then
        svn-ignore
    fi

    /usr/bin/svn $@

    if [ $1 = 'add' ]; then
        svn-ignore
    fi

Make sure to call ``chmod +x FILENAME`` afterwards. After that you just
need to add the following line to ``~/.bashrc``:
``alias svn="/path/to/this/file $@"``. This hook is both for pre-commit
and post-add (A hook you normally won't find).

Windows (TortoiseSVN)
^^^^^^^^^^^^^^^^^^^^^

`TortoiseSVN offers a simple way to add pre-commit hooks client
side. <https://tortoisesvn.net/docs/release/TortoiseSVN_en/tsvn-dug-settings.html#tsvn-dug-settings-hooks>`__
Simply add ``svn-ignore`` as a Pre-Commit Hook in Tortoise-SVN.

On the Repository
~~~~~~~~~~~~~~~~~

This is currently not possible and is planned in a future version

Testing
-------

You can run the tests by calling ``python -m unittest discover`` in the
project root. Subversion 1.9 is required for running the tests.
Automatic testing is done by Travis CI. ## License

MIT License

Copyright (c) 2016 Jord Nijhuis

Permission is hereby granted, free of charge, to any person obtaining a
copy of this software and associated documentation files (the
"Software"), to deal in the Software without restriction, including
without limitation the rights to use, copy, modify, merge, publish,
distribute, sublicense, and/or sell copies of the Software, and to
permit persons to whom the Software is furnished to do so, subject to
the following conditions:

The above copyright notice and this permission notice shall be included
in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS
OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY
CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT,
TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE
SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.