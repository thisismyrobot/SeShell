=========
 SeShell
=========

SeShell (SErial to SHELL converter) allows the mapping of input strings to
shell commands, using regular expressions. If the regular expression matches
sections in () then those matches are passed as arguments to the shell
command.

Run tests in Python 2.6 with "python -m doctest README.txt"

Setup
-----

Firstly we create a class that will be mapped to

>>> class Handler(object):
...     @staticmethod
...     def handle(data):
...         """ "Handles" data (by printing it).
...         """
...         print "handled: '%s'" % data

And we set up the seshell itself

>>> import seshell
>>> seshell_tool = seshell.SeShell()

Mapping
-------

We can now map input strings to that the handler

>>> seshell_tool.bind(
...     "Handler.handle",
...     regex="printinput (.*)",
...     callable_object=Handler.handle)

Parsing
-------

The seshell tool parses inputs and runs methods as mapped.

>>> seshell_tool.parse("printinput hello world")
handled: 'hello world'

No handler
----------

If no mapping has been defined for an input, the mapping silently fails

>>> seshell_tool.parse("incorrectinput hello world")

Mapping from XML
----------------

We can create a number of mappings at once using an XML description.

Firstly we create a new seshell tool

>>> seshell_tool = seshell.SeShell()

And another handler

>>> class SecondHandler(object):
...     @staticmethod
...     def print_data(data):
...         """ Prints data
...         """
...         print "printing: '%s'" % data
...
...     @staticmethod
...     def multiply_data(number1, number2):
...         """ Prints the product of a dict of two numbers
...         """
...         print int(number1) * int(number2)
...
...     @staticmethod
...     def just_say_hi():
...         """ Prints 'hi'
...         """
...         print 'hi'

And some xml to parse

>>> xml = """<?xml version="1.0" encoding="UTF-8"?>
... <mappings>
...     <mapping>
...         <id>SecondHandler.print_data</id>
...         <pattern>printme (.*)</pattern>
...     </mapping>
...     <mapping>
...         <id>SecondHandler.multiply_data</id>
...         <pattern>multiply\(([0-9]*),([0-9]*)\)</pattern>
...     </mapping>
...     <mapping>
...         <id>SecondHandler.just_say_hi</id>
...         <pattern>noargs</pattern>
...     </mapping>
... </mappings>
... """

We can now load the xml

>>> import StringIO
>>> xmlfile = StringIO.StringIO(xml)
>>> seshell_tool.bind_from_xml(xmlfile)

And try out the two mappings

>>> seshell_tool.parse("printme hello")

>>> seshell_tool.parse("multiply(6,2)")

>>> seshell_tool.parse("noargs")

This returns nothing as the callable has not yet been bound - so it is not yet
in scope. XML derived mappings need explicit binding as they cannot contain
a reference to the callable object. This explicit binding also acts as a
white-list of allowable commands.

>>> seshell_tool.bind(
...     "SecondHandler.print_data",
...     callable_object=SecondHandler.print_data)

>>> seshell_tool.bind(
...     "SecondHandler.multiply_data",
...     callable_object=SecondHandler.multiply_data)

>>> seshell_tool.bind(
...     "SecondHandler.just_say_hi",
...     callable_object=SecondHandler.just_say_hi)

After allowing the methods, we can try out the two mappings again

>>> seshell_tool.parse("printme hello")
printing: 'hello'

>>> seshell_tool.parse("multiply(6,2)")
12

>>> seshell_tool.parse("noargs")
hi
