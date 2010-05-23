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

Set up the seshell tool for use

>>> import seshell
>>> seshell_tool = seshell.SeShell()

Mapping from XML
----------------

The seshell tool builds up a mapping from xml.

And some xml to parse

>>> xml = """<?xml version="1.0" encoding="UTF-8"?>
... <mappings>
...     <mapping>
...         <pattern>test1 (.*)</pattern>
...         <command>python</command>
...         <arguments>
...             <argument type="static">test/printargs.py</argument>
...             <argument type="dynamic">0</argument>
...         </arguments>
...     </mapping>
...     <mapping>
...         <pattern>test2 (.*),(.*)</pattern>
...         <command>python</command>
...         <arguments>
...             <argument type="static">test/printargs.py</argument>
...             <argument type="dynamic">0</argument>
...             <argument type="dynamic">1</argument>
...             <argument type="static">last_argument</argument>
...         </arguments>
...     </mapping>
... </mappings>
... """

We can now load the xml

>>> import StringIO
>>> xmlfile = StringIO.StringIO(xml)
>>> seshell_tool.load(xmlfile)

And try out the two mappings. The test script prints the arguments to stdout
and the parse method returns that output as a string.

>>> seshell_tool.parse("test1 hello")
"arguments: ['test/printargs.py', 'hello']"

>>> seshell_tool.parse("test2 6,2")
"arguments: ['test/printargs.py', '6', '2', 'last_argument']"
