import re


class Mapper(object):
    """ Controls the mapping between serial commands and python methods.
    """
    def __init__(self):
        self.mapping = {}

    def parse(self, data):
        """ Parses argument(s) and calls methods as mapped.
        """
        for expression,method in self.mapping.items():
            arguments = re.findall(expression, data)
            try:
                method(*arguments)
                break;
            except:
                 pass

    def connect(self, input, method):
        """ Connects an input string to a method to be called.
        """
        self.mapping[input] = method
