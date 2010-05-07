class CleverClass(object):
    def do_stuff(self):
        """ Does "stuff" with data".
        """
        print "doing clever stuff"


class Mapper(object):
    """ Controls the mapping between serial commands and python methods.
    """
    def __init__(self):
        self.mapping = {}

    def parse(self, data):
        """ Parses argument(s) and calls methods as mapped.
        """
        self.mapping[data]()

    def connect(self, input, method):
        """ Connects an input string to a method to be called.
        """
        self.mapping[input] = method


mapper = Mapper()
mapper.connect("beclever", CleverClass().do_stuff)
mapper.parse("beclever")
