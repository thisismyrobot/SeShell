#!/usr/bin/python2.6

"""

SeShell config checker

"""

import libxml2
import sys


def error(error_detail):
    """ Prints out an error to stderr.
    """
    error_string = "CheckConf Error: %s" % (error_detail,)
    sys.stderr.write(error_string)
    sys.exit(2)


def validate():
    """ Returns None if the xml config is valid, prints a list of validation
        errors otherwise.
    """
    try:
        xml_file = file(sys.argv[1])
    except IndexError:
        error("Missing path to XML configuration file as argument.")
    except IOError:
        error("Couldn't load file '%s', check it exists and is able to be "
              "opened." % (sys.argv[1],))

    xml_data = xml_file.read()

    try:
        xml_doc = libxml2.parseMemory(xml_data, len(xml_data))
    except libxml2.parserError:
        error("Could not parse '%s', check it contains valid XML "
              "configuration." % (sys.argv[1],))
        return

    xml_context = xml_doc.xpathNewContext()
    dtd = libxml2.parseDTD(None, 'validxml.dtd')
    ret = xml_doc.validateDtd(xml_context, dtd)

    if ret == 0:
        error("XML in '%s' not valid, see error(s) above." % (sys.argv[1],))

    dtd.freeDtd()
    xml_doc.freeDoc()
    xml_context.xpathFreeContext()

    del dtd
    del xml_doc
    del xml_context
    xml_file.close()


if __name__ == '__main__':
    validate()
