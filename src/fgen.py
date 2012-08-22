# fgen is a free command line tool that facilitates cross platform
# c++ development, including header generation, cpp file generation,
# makefile generation, unit test framework generation, etc.
#
# Copyright (C) 2006 Kevin Wan <wanjunfeng@gmail.com>
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.

from __future__ import with_statement
from getopt import getopt
from getopt import GetoptError
import sys
from StringIO import StringIO
from filedepot import FileDepot
from fgconfig import XmlConfig

__doc__ = \
"""
fgen - A command line tool to generate the skeleton of kinds of files in c++ development.

Usage: fgen [options] arguments

Options:
  -c, --cpp
      generate cpp file
  -m, --makefile
      specify filename to generate makefile, default to makefile
  -u, --unittest
      generate unit test class for the specified class. if unit test makefile and main.cc
      don't exist, will generate them
  -d, --doc
      generate the doxygen document for the header file
  -h HEADER, --header=HEADER
      specify header file to generate or to generate cpp file base on this header file
"""

__reportTo__ = "\nAny bug or suggestion, please report to <wanjunfeng@gmail.com>, thanks!"

def getUsage():
    """
    We generate usage information and return it.
    Usage information is generated base on config file.
    """
    output = StringIO()
    print>>output
    print>>output, "Usage: fgen [options] arguments\n"
    XmlConfig().printOptionUsage(output)
    output.write(__reportTo__)
    content = output.getvalue()
    output.close()
    return content

def createGenerator(pkg, className, *args):
    """
    With this function, we can add a module into fgen without changing any code but config file.
    """
    exec "import %s" % pkg
    exec "instance = %s.%s(*args)" % (pkg, className)
    return instance

def main():
    if len(sys.argv) == 1:
        sys.exit(getUsage())

    parser = XmlConfig()
    try:
        opts, args = getopt(sys.argv[1:], parser.getShortOptions(), parser.getLongOptions())
        if not opts:
            raise GetoptError("No option specified!")
        
        optlist = []
        for opt in opts:
            optlist = optlist + [x for x in opt if x]

        options = parser.getOptions()
        for option in options:
            shortOpt = "-" + option.getShortOpt()
            longOpt = "--" + option.getLongOpt()
            if shortOpt in optlist or longOpt in optlist:
                pkg = option.getPackage()
                slotClass = option.getSlotClass()
                instance = createGenerator(pkg, slotClass, opts, args)
                instance.init()
                instance.run()
                break
    except GetoptError, ex:
        print "Error: ", ex
        sys.exit(getUsage())

if __name__ == "__main__":
    # We roll back all the generated files if get errors.
    try:
        main()
    except Exception, ex:
        print "Error: ", ex
        FileDepot().removeAllFromDisk()
        print __reportTo__
