import doctest


#Basic test of the core methods in SeShell
doctest.testfile("tests/README.txt")

#PyLint verification
doctest.testfile("tests/pylint.txt")
