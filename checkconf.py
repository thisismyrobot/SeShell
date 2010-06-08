#!/usr/bin/python2.6

"""

SeShell config checker

"""

import libxml2
import sys


def validate():
    """ Returns None if the xml config is valid, prints a list of validation
        errors otherwise.
    """
    xml_file = file(sys.argv[1])
    xml_data = xml_file.read()
    xml_doc = libxml2.parseMemory(xml_data, len(xml_data))
    xml_context = xml_doc.xpathNewContext()
    dtd = libxml2.parseDTD(None, 'validxml.dtd')
    xml_doc.validateDtd(xml_context, dtd)

    dtd.freeDtd()
    xml_doc.freeDoc()
    xml_context.xpathFreeContext()

    del dtd
    del xml_doc
    del xml_context
    xml_file.close()


if __name__ == '__main__':
    validate()
