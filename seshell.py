import os
import libxml2
import re
import subprocess


class Argument(object):
    """ Holds an argument for a command.
    """
    def __init__(self, arg_type, arg_val):
        self.arg_type = arg_type
        self.arg_val = arg_val

    def get(self):
        return (self.arg_type, self.arg_val)

class Mapping(object):
    """ Holds a mapping between a serial command and a shell command.
    """
    def __init__(self, pattern, command):
        self.pattern = str(pattern)
        self.command = str(command)
        self._arguments = []

    def add_argument(self, arg_type, arg_val):
        self._arguments.append(Argument(arg_type, arg_val))

    @property
    def arguments(self):
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
                    input_arguments = matches.groups()
                    input_arguments_index = 0
                    command = mapping.command
                    shell_command = [command]
                    for argument in mapping.arguments:
                        if argument[0] == 'static':
                            shell_command.append(argument[1])
                        else:
                            shell_command.append(input_arguments[input_arguments_index])
                            input_arguments_index += 1
                    proc = subprocess.Popen(shell_command, stdout=subprocess.PIPE)
                    return proc.stdout.readline().rstrip()

    def load(self, xml_file):
        """ Parses an xml file into memory.
        """
        xml_data = xml_file.read()
        xml_struct = libxml2.parseMemory(xml_data, len(xml_data))
        xml_context = xml_struct.xpathNewContext()

        mappings = xml_context.xpathEval('//mappings/mapping')
        for mapping in mappings:
            pattern = mapping.xpathEval('pattern/text()')[0]
            command = mapping.xpathEval('command/text()')[0]
            mapping_instance = Mapping(pattern, command)
            arguments = mapping.xpathEval('arguments/argument')
            for argument in arguments:
                arg_type = argument.xpathEval('@type')[0].content
                arg_val = argument.content
                mapping_instance.add_argument(arg_type, arg_val)
            self.mappings.append(mapping_instance)

        xml_struct.freeDoc()
        xml_context.xpathFreeContext()
        xml_file.close()
