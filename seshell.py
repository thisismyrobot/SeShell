""" SeShell
"""
import libxml2
import re
import subprocess
import threading


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
    def __init__(self, pattern):
        self._pattern = str(pattern)
        self._args = []

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
        print data

    @staticmethod
    def _run(args, callback):
        """ Launches a process and returns the resultant string.
        """
        proc = subprocess.Popen(args, stdout=subprocess.PIPE)
        data = proc.stdout.readline().rstrip()
        callback(data)

    @staticmethod
    def _xml_valid(xml_doc, xml_context):
        """ Returns True if the xml_context is valid, false otherwise.
        """
        dtd = libxml2.parseDTD(None, 'validxml.dtd')
        ret = xml_doc.validateDtd(xml_context, dtd)
        dtd.freeDtd()
        del dtd
        return (ret == 1)

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
                                 args=(output_args, self._print)).start()

    def load(self, xml_file):
        """ Parses an xml file into memory.
        """
        xml_data = xml_file.read()
        xml_doc = libxml2.parseMemory(xml_data, len(xml_data))
        xml_context = xml_doc.xpathNewContext()
        self._xml_valid(xml_doc, xml_context)
        mappings = xml_context.xpathEval('//mappings/mapping')
        for mapping in mappings:
            pattern = mapping.xpathEval('pattern/text()')[0]
            arguments = mapping.xpathEval('argument')
            mapping_instance = Mapping(pattern)
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
