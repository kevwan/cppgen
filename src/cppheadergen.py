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

class CppHeaderGen(FileGenerator):
    def __init__(self, opts, args):
        FileGenerator.__init__(self, opts, args)

    def getOptionTuple(self):
        return ("-h", "--header")

    def run(self):
        if self.__arg__ == None:
            raise GetoptError("no header specified")
        if self.__args__:
            raise GetoptError("too many arguments")
    
        dieOnExists(self.__arg__)
        FileDepot().add(self.__arg__)
        parser = TemplateParser("template.h", self.__arg__)
        parser.parse()
        print "\t" + self.__arg__ + "\t\t\t\t[OK]"
