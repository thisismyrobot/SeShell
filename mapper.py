import re
import libxml2


class Mapper(object):
    """ Controls the mapping between serial commands and python methods.
    """
    def __init__(self):
        self.mapping = {}
        self.allowed = {}

    def allow(self, name, method):
        """ Adds a method to the list of allowable methods. This puts the method
            in scope and limits the possible methods for security.
        """
        self.allowed[name] = method

    def parse(self, data):
        """ Parses argument(s) and calls methods as mapped.
        """
        for expression,method in self.mapping.items():
            arguments = re.findall(expression, data)
            if method in self.allowed:
                try:
                    self.allowed[method](*arguments)
                    break;
                except:
                     pass

    def connect(self, input, method):
        """ Connects an input string to a method to be called.
        """
        self.mapping[input] = method

    def connect_from_xml(self, xml_file):
        """ Parses mappings from an xml file and creates them.
        """
        xml_data = xml_file.read()
        xml_struct = libxml2.parseMemory(xml_data, len(xml_data))
        mappings = []
        xml_context = xml_struct.xpathNewContext()
        patterns = xml_context.xpathEval('//mappings/mapping/pattern/text()')
        handlers = xml_context.xpathEval('//mappings/mapping/handler/text()')

        for index in range(len(patterns)):
            pattern = str(patterns[index])
            handler = str(handlers[index])
            self.connect(pattern, handler)
