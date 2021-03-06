#!/usr/bin/python2.6

"""

SeShell testrunner

"""

import doctest


tests = ("tests/README.txt", #Basic test of the core methods in SeShell
         "tests/checkconf.txt", #Test of config checker
         "tests/pylint.txt") #PyLint verification

for test in tests:
    doctest.testfile(test,
        optionflags=doctest.ELLIPSIS | doctest.DONT_ACCEPT_BLANKLINE | doctest.REPORT_ONLY_FIRST_FAILURE)
