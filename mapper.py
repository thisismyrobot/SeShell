import re
import libxml2


class Mapper(object):
    """ Controls the mapping between serial commands and python methods.
    """
    def __init__(self):
        self.expressions = {}
        self.callable_objects = {}

    def _count_groups(self, regex):
        """ Counts the number of un-escaped '('s to determine the expected
            number of arguments.
        """
        return len(re.findall('(?<!\\\)(\\()', regex))

    def parse(self, data):
        """ Parses argument(s) and calls methods as mapped.
        """
        for expression,id in self.expressions.items():
            matched_groups = 0
            arguments = None
            matches = re.search(expression, data)
            if matches:
                arguments = matches.groups()
                matched_groups = len(arguments)
            if matched_groups == self._count_groups(expression) and id in self.callable_objects:
                try:
                    self.callable_objects[id](*arguments)
                    break
                except:
                    pass

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
