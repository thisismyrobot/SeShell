import os
import libxml2
import re
import subprocess


class Argument(object):
    """ Represents an argument for a command.
    """
    def __init__(self, arg_type, arg_val):
        self.arg_type = arg_type
        self.arg_val = arg_val

    def get(self):
        return (self.arg_type, self.arg_val)


class Mapping(object):
    """ Represents a mapping between a serial command and a shell command.
    """
    def __init__(self, pattern):
        self.pattern = str(pattern)
        self._arguments = []

    def add_argument(self, arg_type, arg_val):
        self._arguments.append(Argument(arg_type, arg_val))

    @property
    def arguments(self):
        """ Returns a tuple of arguments (type, value).
        """
        return [arg.get() for arg in self._arguments]


class SeShell(object):
    """ Maps serial commands to shell commands.
    """
    def __init__(self):
        self.mappings = []

    def parse(self, data):
        """ Parses argument(s) and calls methods as mapped. The matching is
            done with re.sub that replaces a match with ''. If the input data
            exactly matches, the result is ''. The result is returned.
        """
        for mapping in self.mappings:
            pattern = mapping.pattern
            if re.sub(pattern, '', data) == '':
                matches = re.search(pattern, data)
                if matches:
                    input_args = matches.groups()
                    input_args_index = 0
                    output_args = []
                    for argument in mapping.arguments:
                        if argument[0] == 'static':
                            output_args.append(argument[1])
                        else:
                            output_args.append(input_args[input_args_index])
                            input_args_index += 1
                    proc = subprocess.Popen(output_args, stdout=subprocess.PIPE)
                    return proc.stdout.readline().rstrip()

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
                arg_type = argument.xpathEval('@type')[0].content
                arg_val = argument.content
                mapping_instance.add_argument(arg_type, arg_val)
            self.mappings.append(mapping_instance)
        xml_doc.freeDoc()
        xml_context.xpathFreeContext()
        xml_file.close()
