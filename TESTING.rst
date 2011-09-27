Tiger Lily
Copyright 2011 Erich Blume <blume.erich@gmail.com>
See COPYING for copyright information

Tiger Lily Testing Documentation
================================

Tiger Lily was designed with being fully testable in mind, and great care has
been taken to ensure that any end user can run the full test suite with a
minimum of fuss to ensure that her environment is correct.


Running Tiger Lily's Test Suite
-------------------------------

To run the Tiger Lily test suite, execute the following command at the project
root directory:

    $ python3 setup.py nosetests --verbose

Note that this command may take some time to run. This is because the testing
protocol requires a few special packages (``nose`` and ``coverage``) to run and
these packages might need to be downloaded.

If everything worked you should see something like the following:

    running build_ext
    Doctest: tigerlily.grc.genome.GRCGenome.download ... ok
    ... MORE TESTS HERE ...
    
    Name                                 Stmts   Miss  Cover   Missing
    ------------------------------------------------------------------
    tigerlily                                1      0   100%   
    ... MORE COVERAGE HERE ...
    ------------------------------------------------------------------
    TOTAL                                  462     83    82%   
    ----------------------------------------------------------------------
    Ran 25 tests in 0.063s
    
    OK


This indicates a succesful test run. The 'coverage report' at the end indicates
that 82% of Tiger Lily is 'covered' by a unit test. This does NOT indicate that
only 82% of tests passed - the 'OK' at the end means that ALL (100%) tests
passed.


Adding New Unit Tests to Tiger Lily
-----------------------------------

If you thought that running unit tests for Tiger Lily was easy, wait until you
see how easy it is to ADD unit tests. The developers wanted to make sure that
unit tests were written BEFORE new functionality was added, and laziness is
a programmer's best virtue.

There are two suggested methods for adding unit tests:

Method 1: `doctest`
~~~~~~~~~~~~~~~~~~~

Because every single function, method, class, and module *will* have a docstring
(right?), it makes perfect sense that you might want to document an example of
using that function. If that is the case, then Doctests are probably the right
choice for unit testing this function, too. See the
`doctest documentation <http://docs.python.org/py3k/library/doctest.html>`_
for examples on how this is done. It's dead simple though. Enjoy!

Method 2: ``unittest.TestCase``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Sometimes doctests aren't the right choice, such as when you have to write a
huge block of code just to 'set up' the example. In these cases you will want
to use the `unittest <http://docs.python.org/py3k/library/unittest.html>`_
module. 

Simply create a subclass of ``unittest.TestCase`` absolutely *anywhere*. You
could put it inside of the module that contains the function you are testing.
You could put it in another module inside of the subpackage called
<module>_test.py. You could put it inside of a new sub-subpackage called tests
inside of the subpackage inside of which all of the unit tests are stored. All
of these methods will work - the only important thing is that each unit test
gets its own subclass of ``unittest.TestCase``.

