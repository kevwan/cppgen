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
from sys import stdin
from sys import stdout
from sys import stderr
from os import path
from getopt import GetoptError
from os import makedirs
from fgconfig import XmlConfig
from filedepot import FileDepot
from cppheaderparser import CppHeaderParser
from templateparser import TemplateParser
from cppheaderparser import CppHeaderObserver
from fgutils import dieOnExists
from templateparser import TemplateParserObserver
from filegenerator import FileGenerator
import re

class CppUnitGenImpl(CppHeaderObserver):
    def __init__(self, header, output):
        CppHeaderObserver.__init__(self)
        self.__header = header
        self.__output = output
        self.__functions = []
        self.__classFunctions = []
        self.__classNames = []
        self.__testClassName = []
        self.__operatorRe = re.compile(r"\boperator\b.*")
        self.__printScopes = lambda scopes, file=stdout:map(lambda s:file.write(s.getName() + "::"), \
                            [s for s in scopes if s.getType() == "class"])
        self.__assemblyFunctionName = lambda funcName:"test%s" % "".join((funcName[0].capitalize(), funcName[1:]))
    
    def onPreParse(self, scopes):
        self.__output.write("#include <cppunit/extensions/HelperMacros.h>\n")
        head, tail = path.split(self.__header)
        self.__output.write("#include \"%s\"\n\n" % tail)

    def onNamespace(self, scopes, namespace):
        self.__output.write("using namespace %s;\n\n" % namespace)

    def onClass(self, scopes, template, clsName):
        isPublic = True
        for s in scopes:
            if (s.getType() == "class" or s.getType() == "tclass") and s.getAccess() != "public":
                isPublic = False
        if isPublic:
            self.__classNames.append(clsName)

    def onClassStart(self, scopes, clsName):
        self.__classFunctions.append([])

    def onClassEnd(self, scopes, clsName):
        if not self.__classNames or self.__classNames[-1] != clsName:
            raise RuntimeError("mismatched class names")
        testClassName = "%sTest" % clsName
        self.__output.write("class %s : public CppUnit::TestFixture\n" % testClassName)
        self.__output.write("{\n")
        self.__output.write("    CPPUNIT_TEST_SUITE(%s);\n" % testClassName)
        map(lambda func:self.__output.write("    CPPUNIT_TEST(%s);\n" % func), self.__classFunctions[-1])
        self.__output.write("    CPPUNIT_TEST_SUITE_END();\n\n")
        self.__output.write("public:\n")
        self.__output.write("    void setUp();\n")
        self.__output.write("    void tearDown();\n\n")
        map(lambda func:self.__output.write("    void %s();\n" % func), self.__classFunctions[-1])
        self.__output.write("};\n\n")
        self.__output.write("CPPUNIT_TEST_SUITE_REGISTRATION(%s);\n\n" % testClassName)

        # add functions implementation here
        self.__output.write("void %s::setUp()\n{\n}\n\n" % testClassName)
        self.__output.write("void %s::tearDown()\n{\n}\n\n" % testClassName)
        map(lambda func:self.__output.write("void %s::%s()\n{\n    CPPUNIT_FAIL(\"not implemented\");\n}\n\n" % \
               (testClassName, func)), self.__classFunctions[-1])

        self.__classNames.pop()
        self.__classFunctions.pop()

    def onCtorDecl(self, scopes, ctorName, paramList):
        self.__onFunctionImpl(scopes, "Constructor")

    def onFunctionDef(self, scopes, template, type, funcName, paramList, const):
        self.__onFunctionImpl(scopes, funcName)

    def onFunctionDecl(self, scopes, template, type, funcName, paramList, const):
        self.__onFunctionImpl(scopes, funcName)

    def __toGenerate(self, scopes):
        isPublic = True
        for s in scopes:
            if (s.getType() == "class" or s.getType() == "tclass") and s.getAccess() != "public":
                isPublic = False
        return isPublic

    def __onFunctionImpl(self, scopes, funcName):
        if self.__toGenerate(scopes):
            self.__addTestFunction(funcName)

    def __showScopes(self, scopes, output = stdout):
        """this function is for test"""
        map(lambda scope:output.write("(" + scope.getType() + ", " + scope.getName() + ")=>"), scopes)
        output.write("\n")
    
    def __addTestFunction(self, funcName):
        if self.__operatorRe.search(funcName):
            return

        testFuncName = self.__assemblyFunctionName(funcName)
        functions = self.__functions
        if self.__classFunctions:
            functions = self.__classFunctions[-1]
        try:
            functions.index(testFuncName)
        except ValueError:
            functions.append(testFuncName)

class UnitTestMakefileObserver(TemplateParserObserver):
    def __init__(self):
        self.__srcRe = re.compile(r"\ASRC\s*=.*")

    def onPostProcessLine(self, line, output):
        match = self.__srcRe.search(line)
        if match:
            stderr.write("Which file contains main function in current dir: ")
            stderr.flush()
            filename = stdin.readline().strip()
            suffix = XmlConfig().getCppSuffix()
            if filename:
                output.write("SRC     += $(filter-out ../%s, $(wildcard ../*%s))\n" % (filename, suffix))
            else:
                output.write("SRC     += $(wildcard ../*%s)\n" % suffix)

class CppUnitGen(FileGenerator):
    def __init__(self, opts, args):
        FileGenerator.__init__(self, opts, args)

    def getOptionTuple(self):
        return ("-u", "--unittest")

    def run(self):
        hopt, header = self.__getOptArg__(("-h", "--header"))
        if not header:
            raise GetoptError("no header file specified")
        elif len(self.__args__) > 1:
            raise GetoptError("too many arguments")
    
        cppUnitFile = None
        if len(self.__args__) == 1:
            cppUnitFile = self.__args__[0]
        else:
            root, filename = path.split(header)
            name, ext = path.splitext(filename)
            cppSuffix = XmlConfig().getCppSuffix()
            cppUnitFile = "%sTest%s" % (name, cppSuffix)
            cppUnitFile = path.join(XmlConfig().getUnitTestDir(), cppUnitFile)

        self.__checkAndMakeUnitTestDir()
        self.__checkAndGenerateUnitTestMakefile()
        self.__checkAndGenerateUnitTestMain()
        dieOnExists(cppUnitFile)
        FileDepot().add(cppUnitFile)
        parser = TemplateParser("template.cpp", cppUnitFile)
        parser.parse()
        with open(cppUnitFile, "a+") as output:
            headerParser = CppHeaderParser(header)
            cppUnitGenImpl = CppUnitGenImpl(header, output)
            cppUnitGenImpl.setParser(headerParser)
            headerParser.addObserver(cppUnitGenImpl)
            headerParser.parse()
        print "\t" + cppUnitFile + "\t\t\t\t[OK]"
        
    def __checkAndMakeUnitTestDir(self):
        unitDir = XmlConfig().getUnitTestDir()
        if not path.exists(unitDir):
            makedirs(unitDir)
            FileDepot().add(unitDir)
    
    def __checkAndGenerateUnitTestMain(self):
        cppSuffix = XmlConfig().getCppSuffix()
        unitDir = XmlConfig().getUnitTestDir()
        unitMain = path.join(unitDir, "main%s" % cppSuffix)
        if not path.exists(unitMain):
            FileDepot().add(unitMain)
            parser = TemplateParser("unittestmain.cpp", unitMain)
            parser.parse()
            print "\t" + unitMain + "\t\t\t\t[OK]"

    def __checkAndGenerateUnitTestMakefile(self):
        unitDir = XmlConfig().getUnitTestDir()
        makefile = path.join(unitDir, "makefile")
        if not path.exists(makefile):
            FileDepot().add(makefile)
            parser = TemplateParser("makefile.test", makefile)
            parser.addObserver(UnitTestMakefileObserver())
            parser.parse()
            print "\t" + makefile + "\t\t\t\t[OK]"
