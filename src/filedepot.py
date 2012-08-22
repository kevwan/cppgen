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

from os import remove
from os import path
from shutil import rmtree

class FileDepot:
    __files = None

    def __init__(self):
        if not self.__files:
            self.__files = []

    def add(self, filepath):
        self.__files.append(filepath)

    def remove(self, filepath):
        self.__files.remove(filepath)

    def clean(self):
        del self.__files[:]

    def removeAllFromDisk(self):
        if not self.__files:
            print "Rolling back..."

        for filepath in self.__files:
            if path.exists(file):
                rmtree(filepath) if path.isdir(filepath) else remove(filepath)
        self.clean()
