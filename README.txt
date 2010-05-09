========
 Mapper
========

Mapper allows the mapping of input strings to methods, using regular
expressions. If the regular expression matches sections in () then those
matches are passed as arguments to the method. The intended application is for
parsing of serial (RS232/422/485) commands into high-level python methods.

Run tests in Python 2.6 with "python -m doctest README.txt"

Setup
-----

Fistly we create a class that will be mapped to

>>> class Handler(object):
...     def handle(self, data):
...         """ "Handles" data (by printing it).
...         """
...         print "handled: '%s'" % data

And we set up the mapper itself

>>> import mapper
>>> mapper_tool = mapper.Mapper()

Mapping
-------

We can map input strings to call methods in the handler

>>> mapper_tool.connect("printinput (.*)", Handler().handle)

Parsing
-------

The mapper tool parses inputs and runs methods as mapped.

>>> mapper_tool.parse("printinput hello world")
handled: 'hello world'

No handler
----------

If no handler has been chosen, the mapping silently fails

>>> mapper_tool.parse("incorrectinput hello world")
