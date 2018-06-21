Declic
======

Declic (DEcorator-oriented CLI Creator) is a tiny Python 3 package for
creating command line interfaces using decorators. It was inspired by
the `click`_ package and is based on `argparse`_.

Installation
------------

From PyPI:

::

   pip install declic

or from Github:

::

   pip install git+https://github.com/Septaris/declic.git

Usage
-----

Here is an example of Declic usage:

.. literalinclude:: example.py

Running the cli:

::

   $ python my_file.py --help

   usage: bar [-h] [--foo FOO] [--version] {sub_group,foo} ...

   my description

   positional arguments:
     {sub_group,foo}

   optional arguments:
     -h, --help       show this help message and exit
     --foo FOO
     --version        show program's version number and exit

.. _click: http://click.pocoo.org/6/
.. _argparse: https://docs.python.org/3/library/argparse.html