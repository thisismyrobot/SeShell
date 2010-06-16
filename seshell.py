"""

SeShell - Daemon
================

Copyright 2010 Robert Wallhead.

SeShell is distributed under the terms of the GNU General Public License.

GNU General Public License
--------------------------

This file is part of SeShell.

SeShell is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

SeShell is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with SeShell.  If not, see <http://www.gnu.org/licenses/>.

"""
import libxml2
import re
import subprocess
import threading
import time


class Argument(object):
    """ Represents an argument.
    """
    def __init__(self, static, value):
        self._static = static
        self._value = value

    @property
    def static(self):
        """ Returns whether the argument is static
        """
        return self._static

    @property
    def value(self):
        """ Returns the argument value
        """
        return self._value


class Mapping(object):
    """ Represents a mapping between a serial command and a shell command.
    """
    def __init__(self, pattern, timeout):
        self._pattern = str(pattern)
        self._args = []
        self._timeout = float(timeout)

    @property
    def pattern(self):
        """ Returns the mapping pattern.
        """
        return self._pattern

    @property
    def arguments(self):
        """ Returns the arguments for the mapping.
        """
        return self._args

    @property
    def timeout(self):
        """ Returns the timeout.
        """
        return self._timeout

    def add_argument(self, is_static, value):
        """ Adds an argument to the existing arguments.
        """
        self._args.append(Argument(is_static, value))


class SeShell(object):
    """ Maps serial commands to shell commands.
    """
    def __init__(self):
        self.mappings = []

    @staticmethod
    def _print(data):
        """ Prints the data. Is used as a callback for methods to make them
            non-blocking. This will eventually fire data down a serial line.
        """
        print data,

    @staticmethod
    def _watchdog(proc, timeout):
        """ Kills a process if it exceedes it's maximum time.
        """
        time.sleep(timeout)
        proc.kill()

    def _run(self, args, timeout, callback):
        """ Launches a process and returns the resultant string. The creation
            of the process is non-blocking, but the readline() is blocking. To
            resolve possible hangs when a process fails to return any data,
            between the creation of the process and readline() a thread is
            started that kills the process after a timeout.
        """
        proc = subprocess.Popen(args, stdout=subprocess.PIPE)
        threading.Thread(target=self._watchdog,
                         args=(proc, timeout)).start()
        data = proc.stdout.readline().rstrip()
        callback(data)

    def parse(self, data):
        """ Parses argument(s) and calls commands as mapped. The matching is
            done with re.sub that replaces a match with ''. If the input data
            exactly matches, the result is ''. The result is returned.
        """
        for mapping in self.mappings:
            pattern = mapping.pattern
            if re.sub(pattern, '', data) == '':
                input_args = re.search(pattern, data).groups()
                input_args_index = 0
                output_args = []
                for argument in mapping.arguments:
                    if argument.static:
                        output_args.append(argument.value)
                    else:
                        output_args.append(input_args[input_args_index])
                        input_args_index += 1
                threading.Thread(target=self._run,
                                 args=(output_args,
                                       mapping.timeout,
                                       self._print)).start()

    def load(self, xml_file):
        """ Parses an xml file into memory.
        """
        self.mappings = []
        xml_data = xml_file.read()
        xml_doc = libxml2.parseMemory(xml_data, len(xml_data))
        xml_context = xml_doc.xpathNewContext()
        mappings = xml_context.xpathEval('//mappings/mapping')
        for mapping in mappings:
            pattern = mapping.xpathEval('pattern/text()')[0]
            timeout = mapping.xpathEval('timeout/@value')[0].content
            arguments = mapping.xpathEval('argument')
            mapping_instance = Mapping(pattern, timeout)
            for argument in arguments:
                static = (argument.xpathEval('@type')[0].content == 'static')
                value = argument.content
                mapping_instance.add_argument(static, value)
            self.mappings.append(mapping_instance)
        xml_doc.freeDoc()
        xml_context.xpathFreeContext()
        del xml_doc
        del xml_context
        xml_file.close()
