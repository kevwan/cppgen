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

class FileGenerator:
    def __init__(self, opts, args):
        self.__opts__ = opts
        self.__args__ = args
        self.__opt__ = None
        self.__arg__ = None

    def getOptionTuple(self):
        raise NotImplementedError("the subclass didn't implement this function")
    
    def init(self):
        self.__opt__, self.__arg__ = self.__getOptArg__(self.getOptionTuple())

    def run(self):
        raise NotImplementedError("the subclass didn't implement this function")

    def __getOptArg__(self, opt):
        for o, a in self.__opts__:
            if o in opt:
                return (o, a)
        return (None, None)