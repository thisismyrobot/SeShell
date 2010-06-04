import doctest


tests = ("tests/README.txt", #Basic test of the core methods in SeShell
         "tests/pylint.txt") #PyLint verification

for test in tests:
    doctest.testfile(test,
        optionflags=doctest.ELLIPSIS | doctest.DONT_ACCEPT_BLANKLINE)
