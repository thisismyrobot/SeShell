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
...         <argument type="static">python</argument>
...         <argument type="static">test/printargs.py</argument>
...         <argument type="dynamic">0</argument>
...     </mapping>
...     <mapping>
...         <pattern>test2 (.*),(.*)</pattern>
...         <argument type="static">python</argument>
...         <argument type="static">test/printargs.py</argument>
...         <argument type="dynamic">0</argument>
...         <argument type="dynamic">1</argument>
...         <argument type="static">last_argument</argument>
...     </mapping>
...     <mapping>
...         <pattern>test3 (.*),(.*)</pattern>
...         <argument type="static">python</argument>
...         <argument type="static">test/slowprocess.py</argument>
...         <argument type="dynamic">0</argument>
...         <argument type="dynamic">1</argument>
...     </mapping>
... </mappings>
... """

We can now load the xml

>>> import StringIO
>>> xmlfile = StringIO.StringIO(xml)
>>> seshell_tool.load(xmlfile)

Parsing input
-------------

And try out the two mappings. The test script prints the arguments to stdout
and the parse method returns that output as a string. We sleep after each
command as the processes are non-blocking.

>>> import time
>>> seshell_tool.parse("test1 hello")
>>> time.sleep(0.1)
arguments: ['test/printargs.py', 'hello']

>>> seshell_tool.parse("test2 6,2")
>>> time.sleep(0.1)
arguments: ['test/printargs.py', '6', '2', 'last_argument']

Incorrect input
---------------

Incorrect (non-mapped) input is ignored

>>> seshell_tool.parse("input is nonexistent")

Blocking processes
------------------

Processes do not block (this process will take 2 seconds to complete) so the
call returns in a very short period of time, but the results take longer. The
3 seconds is to give the process time to launch. This may need tweaking on
really slow embedded systems.

>>> now = time.time()
>>> seshell_tool.parse("test3 34,26")
>>> after = time.time()
>>> int(after - now)
0

>>> time.sleep(3)
delayed arguments: ['test/slowprocess.py', '34', '26']

Escaped arguments
-----------------

To stop arguments breaking out of the method call, they are escaped.

>>> seshell_tool.parse("""test1 hello ; echo \"b,oo\\' "bar'""")
>>> time.sleep(0.1)
arguments: ['test/printargs.py', 'hello ; echo "b,oo\\\' "bar\'']
