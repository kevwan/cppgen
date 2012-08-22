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

from getopt import GetoptError
from filedepot import FileDepot
from fgutils import dieOnExists
from templateparser import TemplateParser
from filegenerator import FileGenerator 

class MakefileGen(FileGenerator):
    def __init__(self, opts, args):
        FileGenerator.__init__(self, opts, args)

    def getOptionTuple(self):
        return ("-m", "--makefile")

    def run(self):
        if len(self.__args__) > 1:
            raise GetoptError("too many arguments")
            
        makefile = "makefile"
        if len(self.__args__) == 1:
            makefile = self.__args__[0]
    
        dieOnExists(makefile)
        FileDepot().add(makefile)
        parser = TemplateParser("makefile", makefile)
        parser.parse()
        print "\t" + makefile + "\t\t\t\t[OK]"