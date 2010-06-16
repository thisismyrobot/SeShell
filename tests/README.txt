=========
 SeShell
=========

This is a basic "covering all the bases" test of SeShell.

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
... <seshell>
...     <mapping>
...         <pattern>test1 (.*)</pattern>
...         <argument type="static">python</argument>
...         <argument type="static">tests/processes/printargs.py</argument>
...         <argument type="dynamic">0</argument>
...         <timeout value="1"/>
...     </mapping>
...     <mapping>
...         <pattern>test2 (.*),(.*)</pattern>
...         <argument type="static">python</argument>
...         <argument type="static">tests/processes/printargs.py</argument>
...         <argument type="dynamic">0</argument>
...         <argument type="dynamic">1</argument>
...         <argument type="static">last_argument</argument>
...         <timeout value="1"/>
...     </mapping>
...     <mapping>
...         <pattern>test3 (.*),(.*)</pattern>
...         <argument type="static">python</argument>
...         <argument type="static">tests/processes/slowprocess.py</argument>
...         <argument type="dynamic">0</argument>
...         <argument type="dynamic">1</argument>
...         <timeout value="3"/>
...     </mapping>
... </seshell>
... """

We can now load the xml and validate it

>>> import StringIO
>>> xmlfile = StringIO.StringIO(xml)
>>> xmlfile.name = "test.xml"
>>> import checkconf
>>> checkconf.validate(xmlfile)
>>> xmlfile = StringIO.StringIO(xml)
>>> xmlfile.name = "test.xml"
>>> seshell_tool.load(xmlfile)

Parsing input
-------------

And try out the two mappings. The test script prints the arguments to stdout
and the parse method returns that output as a string. We sleep after each
command as the processes are non-blocking.

>>> import time
>>> seshell_tool.parse("test1 hello")
>>> time.sleep(0.1)
arguments: ['tests/processes/printargs.py', 'hello']

>>> seshell_tool.parse("test2 6,2")
>>> time.sleep(0.1)
arguments: ['tests/processes/printargs.py', '6', '2', 'last_argument']

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

>>> time.sleep(2.1)
delayed arguments: ['tests/processes/slowprocess.py', '34', '26']

Escaped arguments
-----------------

To stop arguments breaking out of the method call, they are escaped.

>>> seshell_tool.parse("""test1 hello ; echo \"b,oo\\' "bar'""")
>>> time.sleep(0.1)
arguments: ['tests/processes/printargs.py', 'hello ; echo "b,oo\\\' "bar\'']

Timeouts
--------

If a process takes longer than the value in the <timeout> tag, it is killed
and no output is returned (partial output is discarded). The timeout for
test 4 is 0.5 seconds, the program should block for 1 second, printing out
some data immediately and some after the 1 second. 

Firstly, we add the mapping

>>> xml = """<?xml version="1.0" encoding="UTF-8"?>
... <seshell>
...     <mapping>
...         <pattern>test4 (.*)</pattern>
...         <argument type="static">python</argument>
...         <argument type="static">tests/processes/timeout.py</argument>
...         <argument type="dynamic">0</argument>
...         <timeout value="0.5"/>
...     </mapping>
... </seshell>
... """

>>> import StringIO
>>> xmlfile = StringIO.StringIO(xml)
>>> xmlfile.name = "test.xml"
>>> import checkconf
>>> checkconf.validate(xmlfile)
>>> xmlfile = StringIO.StringIO(xml)
>>> xmlfile.name = "test.xml"
>>> seshell_tool.load(xmlfile)

And check that the existing arguments have been deleted

>>> seshell_tool.parse("test1 hello")
>>> time.sleep(0.1)

Now we check the new mapping

>>> seshell_tool.parse("test4 hello how are you?")
>>> time.sleep(1.1)

And it returned nothing. If we change the timeout, we will get returned data.

>>> xml = """<?xml version="1.0" encoding="UTF-8"?>
... <seshell>
...     <mapping>
...         <pattern>test4 (.*)</pattern>
...         <argument type="static">python</argument>
...         <argument type="static">tests/processes/timeout.py</argument>
...         <argument type="dynamic">0</argument>
...         <timeout value="1.5"/>
...     </mapping>
... </seshell>
... """

>>> import StringIO
>>> xmlfile = StringIO.StringIO(xml)
>>> xmlfile.name = "test.xml"
>>> import checkconf
>>> checkconf.validate(xmlfile)
>>> xmlfile = StringIO.StringIO(xml)
>>> xmlfile.name = "test.xml"
>>> seshell_tool.load(xmlfile)
>>> seshell_tool.parse("test4 hello how are you?")
>>> time.sleep(1.1)
some output before timing outthis should have timed out before showing the following: ['tests/processes/timeout.py', 'hello how are you?']

Addressable mappings
--------------------

Some protocols are multi-drop (RS-485, RS-422 etc) where each reciever has an
address. Some addressing schemes are simple like SDI-12 which uses the numbers
0-9 as the first charater to indicate devices 1-10. Some RS-485 devices use
#n as the first characters (n = device number) for addressing. When defining
mappings the user could easily prepend all of their <pattern> elements with
the address - eg <pattern>#1 gettemp(sensor=2)</pattern> or they could use the
<address> tag to wrap a collection of mappings that all have the same start
address.

Firstly, we will create and load some xml.

>>> xml = """<?xml version="1.0" encoding="UTF-8"?>
... <seshell>
...     <address value="#1">
...         <mapping>
...             <pattern>test5 (.*)</pattern>
...             <argument type="static">python</argument>
...             <argument type="static">tests/processes/printargs.py</argument>
...             <argument type="dynamic">0</argument>
...             <timeout value="0.1"/>
...         </mapping>
...         <mapping>
...             <pattern>test6 (.*)</pattern>
...             <argument type="static">python</argument>
...             <argument type="static">tests/processes/printargs.py</argument>
...             <argument type="dynamic">0</argument>
...             <timeout value="0.1"/>
...         </mapping>
...     </address>
...     <address value="#2">
...         <mapping>
...             <pattern>test7 (.*)</pattern>
...             <argument type="static">python</argument>
...             <argument type="static">tests/processes/printargs.py</argument>
...             <argument type="dynamic">0</argument>
...             <timeout value="0.1"/>
...         </mapping>
...     </address>
... </seshell>
... """

>>> import StringIO
>>> xmlfile = StringIO.StringIO(xml)
>>> xmlfile.name = "test.xml"
>>> import checkconf
>>> checkconf.validate(xmlfile)
>>> xmlfile = StringIO.StringIO(xml)
>>> xmlfile.name = "test.xml"
>>> seshell_tool.load(xmlfile)

Now we can trigger the different patterns using their addresses.

>>> seshell_tool.parse("test5 no address means no output")
>>> time.sleep(0.1)

>>> seshell_tool.parse("#1test5 adding the address generates some output")
>>> time.sleep(0.1)
arguments: ['tests/processes/printargs.py', 'adding the address generates some output']

>>> seshell_tool.parse("#1test6 and multiple mappings can be mapped together")
>>> time.sleep(0.1)
arguments: ['tests/processes/printargs.py', 'and multiple mappings can be mapped together']

>>> seshell_tool.parse("#2test7 and we can add multiple addresses per file")
>>> time.sleep(0.1)
arguments: ['tests/processes/printargs.py', 'and we can add multiple addresses per file']
