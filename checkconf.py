#!/usr/bin/python2.6
"""

SeShell - Config checker
========================

Copyright 2010 Robert Wallhead.

SeShell is distributed under the terms of the GNU General Public License.

GNU General Public License
--------------------------

This file is part of SeShell.

SeShell is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

SeShell is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with SeShell.  If not, see <http://www.gnu.org/licenses/>.

"""

import libxml2
import sys


def error(error_detail):
    """ Prints out an error to stderr.
    """
    error_string = "CheckConf Error: %s" % (error_detail,)
    sys.stderr.write(error_string)
    sys.exit(2)


def validate(xml_file):
    """ Returns None if the xml config is valid, prints a list of validation
        errors otherwise.
    """
    xml_data = xml_file.read()

    try:
        xml_doc = libxml2.parseMemory(xml_data, len(xml_data))
    except libxml2.parserError:
        error("Could not parse '%s', check it contains valid XML "
              "configuration." % (xml_file.name,))
        return

    xml_context = xml_doc.xpathNewContext()
    dtd = libxml2.parseDTD(None, 'validxml.dtd')
    ret = xml_doc.validateDtd(xml_context, dtd)

    if ret == 0:
        error("XML in '%s' not valid, see error(s) above." % (xml_file.name,))

    dtd.freeDtd()
    xml_doc.freeDoc()
    xml_context.xpathFreeContext()

    del dtd
    del xml_doc
    del xml_context
    xml_file.close()


if __name__ == '__main__':
    try:
        validate(file(sys.argv[1]))
    except IndexError:
        error("Missing path to XML configuration file as argument.")
    except IOError:
        error("Couldn't load file '%s', check it exists and is able to be "
              "opened." % (sys.argv[1],))
