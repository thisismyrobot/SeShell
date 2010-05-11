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

Firstly we create a class that will be mapped to

>>> class Handler(object):
...     @staticmethod
...     def handle(data):
...         """ "Handles" data (by printing it).
...         """
...         print "handled: '%s'" % data

And we set up the mapper itself

>>> import mapper
>>> mapper_tool = mapper.Mapper()

Mapping
-------

We can now map input strings to that the handler

>>> mapper_tool.connect("printinput (.*)", "Handler.handle")

Parsing
-------

The mapper tool parses inputs and runs methods as mapped.

>>> mapper_tool.parse("printinput hello world")

This returns nothing as the method was not yet allowed. Allowing a method also
adds it into scope for the mapper.

>>> mapper_tool.allow("Handler.handle", Handler.handle)

>>> mapper_tool.parse("printinput hello world")
handled: 'hello world'

No handler
----------

If no handler has been chosen, the mapping silently fails

>>> mapper_tool.parse("incorrectinput hello world")

Mapping from XML
----------------

We can create a number of mappings at once using an XML description.

Firstly we create a new mapper

>>> mapper_tool = mapper.Mapper()

And another handler

>>> class SecondHandler(object):
...     @staticmethod
...     def print_data(data):
...         """ Prints data
...         """
...         print "printing: '%s'" % data
...
...     @staticmethod
...     def multiply_data(numbers):
...         """ Prints the product of a dict of two numbers
...         """
...         print int(numbers[0]) * int(numbers[1])

We allow the handler methods

>>> mapper_tool.allow("SecondHandler.print_data", SecondHandler.print_data)
>>> mapper_tool.allow("SecondHandler.multiply_data", SecondHandler.multiply_data)

And some xml to parse

>>> xml = """<?xml version="1.0" encoding="UTF-8"?>
... <mappings>
...     <mapping>
...         <pattern>printme (.*)</pattern>
...         <handler>SecondHandler.print_data</handler>
...     </mapping>
...     <mapping>
...         <pattern>multiply\(([0-9])*,([0-9])*\)</pattern>
...         <handler>SecondHandler.multiply_data</handler>
...     </mapping>
... </mappings>
... """

We can now load the xml

>>> import StringIO
>>> xmlfile = StringIO.StringIO(xml)
>>> mapper_tool.connect_from_xml(xmlfile)

Which is mapped into the mapper tool

And try out the two mappings

>>> mapper_tool.parse("printme hello")
printing: 'hello'

>>> mapper_tool.parse("multiply(6,2)")
12
