#######
PyHooks
#######

.. image:: https://img.shields.io/travis/Shir0kamii/pyhooks/master.svg
.. image:: https://img.shields.io/coveralls/Shir0kamii/pyhooks/master.svg
.. image:: https://img.shields.io/codeclimate/github/Shir0kamii/pyhooks.svg

PyHooks is meant to expose method hook for classes

=======
Purpose
=======

Have you ever wanted to execute code before or after a method ? PyHooks solve
this exact problem taking inspiration from marshmallow's hook system.

============
Installation
============

Like any other published python package, you can install it via `pip` : 

.. code-block:: bash

    pip install pyhooks


============
How to use ?
============

To use it, you first need to implement a hooked method. You do this by
decorating the method with `@Hook`.

For example, suppose you have a class that at some moment save your data (such
as a database). If you want to be able to plug new behavior, your code
will look like this:

.. code-block:: python 

    from pyhooks import Hook


    class DatabaseEntry(object):
        @Hook
        def save(self):
            pass # save implementation here

Thanks to the `@Hook` line, you will now be able to add functions that execute
before and after the `save` method using the decorators `@precall_register` 
and `@postcall_register`.

For instance, if you want to increment a version variable before 
saving, you could do:

.. code-block:: python

    from pyhooks import precall_register


    class VersionnedEntry(DatabaseEntry):
        @precall_register("save")
        def increment_version(self):
            self.version += 1


The decorator directive indicates to your class that `increment_version` should
be run before the `save` method that is passed to the decorator as argument.


========
Examples
========

You can find some more examples in the `examples/` directory of this
repository.

==============
Advanced usage
==============

You can specialize a register decorator by calling it outside of a decorator
context. The last example would yield:

.. code-block:: python

    from pyhooks import precall_register

    pre_save = precall_register("save")


    class VersionnedEntry(DatabaseEntry):
        @pre_save
        def increment_version(self):
            self.version += 1
