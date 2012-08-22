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
from os import path
from os import rename
from getopt import GetoptError
from cppheaderparser import CppHeaderParser, CppHeaderObserver
from filegenerator import FileGenerator
import re 

class DocGen(FileGenerator, CppHeaderObserver):
    def __init__(self, opts, args):
        FileGenerator.__init__(self, opts, args)
        CppHeaderObserver.__init__(self)
        self.__toDocs = []
        self.__target = None
        self.__leadingWSRe = re.compile(r"(?P<spaces>^\s*)")
        self.__whiteSpaceRe = re.compile(r"\s+")

    def getOptionTuple(self):
        return ("-d", "--doc")

    def run(self):
        header = self.__getOptArg__(("-h", "--header"))[1]
        if not header:
            raise GetoptError("no header file specified")
        elif len(self.__args__) > 1:
            raise GetoptError("too many arguments")

        self.__target = header
        headerParser = CppHeaderParser(header)
        self.setParser(headerParser)
        headerParser.addObserver(self)
        headerParser.parse()
        self.__printToDocs()
        print "\t" + self.__target + "\t\t\t\t[OK]"

    def onClass(self, scopes, template, className):
        self.__toDocs.append((self.__getLineNo(), "class", className))

    def onEnum(self, scopes, enumName, enumMembers):
        self.__toDocs.append((self.__getLineNo(), "enum", enumName))

    def onFunctionDef(self, scopes, template, type, funcName, paramList, const):
        self.onFunctionDecl(scopes, template, type, funcName, paramList, const)

    def onFunctionDecl(self, scopes, template, type, funcName, paramList, const):
        self.__toDocs.append((self.__getLineNo(), "function", type, funcName, paramList))

    def onDtorDecl(self, scopes, dtorName):
        self.__toDocs.append((self.__getLineNo(), "dtor"))

    def onCtorDecl(self, scopes, ctorName, paramList):
        self.__toDocs.append((self.__getLineNo(), "ctor", paramList))

    def onDtorDef(self, scopes, dtorName):
        self.onDtorDecl(scopes, dtorName)

    def onCtorDef(self, scopes, ctorName, paramList):
        self.onCtorDecl(scopes, ctorName, paramList)

    def __getLineNo(self):
        return self.__parser__.getLineNo()

    def __printToDocs(self):
        root, name = path.split(self.__target)
        filename = path.join(root, ".%s" % name)
        with open(self.__target) as input:
            with open(filename, "w+") as output:
                toComment = True
                lineno = 0
                for line in input:
                    try:
                        lineno += 1
                        sline = line.strip()
                        if sline and sline.startswith("///") or sline.startswith("/**"):
                            toComment = False
                        else:
                            toComment = True
                        if self.__toDocs:
#                            if docCmtLine == self.__toDocs[0][0] - 1:
#                                continue
                            if toComment and self.__toDocs[0][0] == lineno:
                                toPrint = self.__toDocs.pop(0)
                                self.__printDoc(output, line, toPrint)
                    finally:
                        output.write(line)
        if not self.__verify(self.__target, filename):
            raise RuntimeError("didn't generate the right document")
        tmpname = "%s.bak" % filename
        rename(filename, tmpname)
        rename(self.__target, filename)
        rename(tmpname, self.__target)

    def __printDoc(self, output, line, toDoc):
        match = self.__leadingWSRe.search(line)
        leadingWs = ""
        if match:
            leadingWS = match.group("spaces")
        type = toDoc[1]
        print>>output, "%s/// <summary>" % leadingWS
        print>>output, "%s/// </summary>" % leadingWS

        params = None
        if type == "ctor":
            params = [x[1] for x in toDoc[2]]
        elif type == "function":
            params = [x[1] for x in toDoc[4]]

        if params:
            for param in params:
                print>>output, "%s/// <param name=\"%s\"></param>" % (leadingWS, param)

        if type == "function":
            if toDoc[2] != "void":
                print>>output, "%s/// <returns></returns>" % leadingWS

    def __showToDocs(self):
        """ this is for test purpose """
        for toDoc in self.__toDocs:
            print toDoc

    def __verify(self, src, dst):
        with open(src) as f1:
            with open(dst) as f2:
                for line1 in f1:
                    while True:
                        line2 = f2.readline()
                        if not line2:
                            return False
                        if line1.rstrip() == line2.rstrip():
                            break
        return True
