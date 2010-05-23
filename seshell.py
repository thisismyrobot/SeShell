import os
import libxml2
import re
import subprocess


class Argument(object):
    """ Represents an argument.
    """
    def __init__(self, static, value):
        self.static = static
        self.value = value


class Mapping(object):
    """ Represents a mapping between a serial command and a shell command.
    """
    def __init__(self, pattern):
        self.pattern = str(pattern)
        self.arguments = []


class SeShell(object):
    """ Maps serial commands to shell commands.
    """
    def __init__(self):
        self.mappings = []

    def _run(self, args):
        """ Launches a process and returns the resultant string.
        """
        proc = subprocess.Popen(output_args, stdout=subprocess.PIPE)
        return proc.stdout.readline().rstrip()

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
                self._run(args)

    def load(self, xml_file):
        """ Parses an xml file into memory.
        """
        xml_data = xml_file.read()
        xml_doc = libxml2.parseMemory(xml_data, len(xml_data))
        xml_context = xml_doc.xpathNewContext()
        mappings = xml_context.xpathEval('//mappings/mapping')
        for mapping in mappings:
            pattern = mapping.xpathEval('pattern/text()')[0]
            arguments = mapping.xpathEval('argument')
            mapping_instance = Mapping(pattern)
            for argument in arguments:
                static = (argument.xpathEval('@type')[0].content == 'static')
                value = argument.content
                mapping_instance.arguments.append(Argument(static, value))
            self.mappings.append(mapping_instance)
        xml_doc.freeDoc()
        xml_context.xpathFreeContext()
        xml_file.close()
