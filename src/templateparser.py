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
from fgconfig import XmlConfig
from os import path
from datetime import date
import re

class TemplateParserObserver:
    def onPreProcessLine(self, line, stream):
        pass
    def onPostProcessLine(self, line, stream):
        pass

class TemplateParser:
    def __init__(self, tmpfile, output):
        self.__config = XmlConfig()
        self.__template = path.join(self.__config.getConfigPath(), tmpfile)
        self.__output = output
        self.__observers = []
        self.__varRe = re.compile(r"\${(?P<var>\b\w+\b)}")

    def addObserver(self, observer):
        self.__observers.append(observer)

    def removeObserver(self, observer):
        self.__observers.remove(observer)

    def parse(self):
        with open(self.__output, "w+") as stream:
            map(lambda line:self.__processLine(line, stream), open(self.__template))

    def __processLine(self, line, stream):
        line = self.__replaceVars(line)
        stream.write(line)
        map(lambda ob:ob.onPostProcessLine(line, stream), self.__observers)

    def __replaceVars(self, s):
        match = self.__varRe.search(s)
        if match == None:
            return s

        start, end = match.span()
        var = match.group("var").lower()
        if var == "wrapper":
            s = self.__replaceWrapper(s, start, end)
        elif var == "date":
            s = "".join((s[:start], date.today().isoformat(), s[end:]))
        else:
            value = self.__config.get(var)
            if  value != None:
                start, end = match.span()
                s = self.__varRe.sub(value, s)
        return "".join((s[:end], self.__replaceVars(s[end:])))

    def __replaceWrapper(self, s, start, end):
        head, tail = path.split(self.__output)
        name, ext = path.splitext(tail)
        value = self.__config.getWrapperPrefix()
        value = value if value else ""
        wrapper = "%s%s" % (value, name.upper())
        return "".join((s[:start], wrapper, s[end:]))
