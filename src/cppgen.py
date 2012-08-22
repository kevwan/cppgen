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
from sys import stdout
from os import path
from getopt import GetoptError
from cppheaderparser import CppHeaderObserver
from cppheaderparser import CppHeaderParser
from fgutils import dieOnExists
from templateparser import TemplateParser
from filedepot import FileDepot
from filegenerator import FileGenerator
from fgconfig import XmlConfig

class CppGenImpl(CppHeaderObserver):
    def __init__(self, header, output):
        CppHeaderObserver.__init__(self)
        self.__header = header
        self.__output = output
        
    def onPreParse(self, scopes):
        head, tail = path.split(self.__header)
        self.__output.write("#include \"%s\"\n\n" % tail)

    def onNamespace(self, scopes, namespace):
        self.__output.write("namespace %s\n" % namespace)

    def onNamespaceStart(self, scopes, namespace):
        self.__output.write("{\n\n")

    def onNamespaceEnd(self, scopes, namespace):
        self.__output.write("}\n")

    def onFunctionDecl(self, scopes, template, returnType, funcName, paramList, const):
        if self.__parser__.isPartOfTemplateClass():
            return

        if template:
            self.__output.write("%s\n" % self.__parser__.assemblyTemplate(template))
        if returnType:
            self.__output.write("%s " % returnType)
        self.__printScopes(scopes, self.__output)
        self.__output.write(funcName)
        self.__output.write("(%s)" % self.__parser__.assemblyParamList(paramList))
        if const:
            self.__output.write(" const")
        self.__output.write("\n{\n}\n\n")

    def onDtorDecl(self, scopes, dtorName):
        if self.__parser__.isPartOfTemplateClass():
            return

        self.__printScopes(scopes, self.__output)
        self.__output.write(dtorName)
        self.__output.write("()\n{\n}\n\n")

    def onCtorDecl(self, scopes, ctorName, paramList):
        if self.__parser__.isPartOfTemplateClass():
            return

        self.__printScopes(scopes, self.__output)
        self.__output.write(ctorName)
        self.__output.write("(%s)\n{\n}\n\n" % self.__parser__.assemblyParamList(paramList))

    def __printScopes(self, scopes, file = stdout):
        scopesToPrint = [scope for scope in scopes if scope.getType() == "class"]
        map(lambda scope:file.write(scope.getName() + "::"), scopesToPrint)

    def __showScopes(self, scopes, output = stdout):
        """this function is for test"""
        map(lambda scope:output.write("(" + scope.getType() + ", " + scope.getName() + ")=>"), scopes)
        output.write("\n")

class CppGen(FileGenerator):
    def __init__(self, opts, args):
        FileGenerator.__init__(self, opts, args)

    def getOptionTuple(self):
        return ("-c", "--cpp")

    def run(self):
        if len(self.__args__) > 1:
            raise GetoptError("too many arguments")

        hopt, header = self.__getOptArg__(("-h", "--header"))

        cppFile = None
        if len(self.__args__) == 1:
            cppFile = self.__args__[0]
        elif not self.__args__ and header:
            name, ext = path.splitext(header)
            suffix = XmlConfig().getCppSuffix()
            cppFile = name + suffix
        else:
            raise GetoptError("no cpp file to generate")
    
        dieOnExists(cppFile)
        FileDepot().add(cppFile)
        parser = TemplateParser("template.cpp", cppFile)
        parser.parse()
        if header != None:
            self.__generateCppContentFromHeader(cppFile, header)
        print "\t" + cppFile + "\t\t\t\t[OK]"

    def __generateCppContentFromHeader(self, cppFile, header):
        with open(cppFile, "a+") as output:
            headerParser = CppHeaderParser(header)
            cppGenImpl = CppGenImpl(header, output)
            cppGenImpl.setParser(headerParser)
            headerParser.addObserver(cppGenImpl)
            headerParser.parse()
