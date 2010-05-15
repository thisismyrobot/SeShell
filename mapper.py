import re
import libxml2


class Mapper(object):
    """ Maps string commands to Python methods
    """
    def __init__(self):
        self.expressions = {}
        self.callable_objects = {}

    def parse(self, data):
        """ Parses argument(s) and calls methods as mapped. The matching is
            done with re.sub that replaces a match with ''. If the input data
            exactly matches, the result is ''.
        """
        for expression,id in self.expressions.items():
            if re.sub(expression, '', data) == '':
                matches = re.search(expression, data)
                if matches:
                    arguments = matches.groups()
                if id in self.callable_objects:
                    self.callable_objects[id](*arguments)

    def bind(self, id, regex=None, callable_object=None):
        """ Connects method ids to regular expressions and/or the actual
            Python methods.
        """
        if regex:
            self.expressions[regex] = id
        if callable_object:
            self.callable_objects[id] = callable_object

    def bind_from_xml(self, xml_file):
        """ Parses mappings from an xml file and creates them.
        """
        xml_data = xml_file.read()
        xml_struct = libxml2.parseMemory(xml_data, len(xml_data))
        mappings = []
        xml_context = xml_struct.xpathNewContext()
        patterns = xml_context.xpathEval('//mappings/mapping/pattern/text()')
        ids = xml_context.xpathEval('//mappings/mapping/id/text()')

        for index in range(len(patterns)):
            pattern = str(patterns[index])
            id = str(ids[index])
            self.bind(id, regex=pattern)
