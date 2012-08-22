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
import unittest
import os
from datetime import date
from sys import exit
from os import path
from os import system
from os import remove
from shutil import copy
from fgconfig import XmlConfig
from templateparser import TemplateParser

class fgenTest(unittest.TestCase):    
    def setUp(self):
        try:
            self.__config = XmlConfig()
            self.__fgen = "fgen.py"
        except Exception, ex:
            print "Error: ", ex
            exit("exitting unit test...")

    def testCpp(self):
        header = path.join("test", "sample.h")
        cppFile = path.join("test", "sample.cc")
        cppStandard = path.join("test", "sample_standard.cc")

        self.__removeOnExists(cppFile)
        command = r"python %s -h %s -c %s" % (self.__fgen, header, cppFile)
        system(command)

        expected = self.__getFileContent(cppStandard)
        expected = expected.replace("&date", date.today().isoformat())
        actual = self.__getFileContent(cppFile)
        self.assertEquals(expected, actual)
        remove(cppFile)

    def testHeader(self):
        header = path.join("test", "headertest.h")
        headerStandard = path.join("test", "headertest_standard.h")

        self.__removeOnExists(header)
        command = r"python %s -h %s" % (self.__fgen, header)
        system(command)

        expected = self.__getFileContent(headerStandard)
        expected = expected.replace("&date", date.today().isoformat())
        actual = self.__getFileContent(header)
        self.assertEquals(expected, actual)
        remove(header)
        
    def testMakefile(self):
        makefile = path.join("test", "makefile")
        makefileStandard = path.join("test", "makefile_standard")

        self.__removeOnExists(makefile)
        command = r"python %s -m %s" % (self.__fgen, makefile)
        system(command)

        expected = self.__getFileContent(makefileStandard)
        actual = self.__getFileContent(makefile)
        self.assertEquals(expected, actual)
        remove(makefile)

    def testUnitTestClass(self):
        header = path.join("test", "sample.h")
        unitFile = path.join("test", "sampleTest.cc")
        unitStandard = path.join("test", "sampleTest_standard.cc")

        self.__removeOnExists(unitFile)
        command = r"python %s -h %s -u %s" % (self.__fgen, header, unitFile)
        system(command)

        expected = self.__getFileContent(unitStandard)
        expected = expected.replace("&date", date.today().isoformat())
        actual = self.__getFileContent(unitFile)
        self.assertEquals(expected, actual)
        remove(unitFile)
        
    def testCppHeaderDoc(self):
        oheader = path.join("test", "sample.h")
        header = path.join("test", "sample_doc.h")
        copy(oheader, header)
        docStandard = path.join("test", "sample_doc_standard.h")

        command = r"python %s -h %s -d" % (self.__fgen, header)
        system(command)

        expected = self.__getFileContent(docStandard)
        expected = expected.replace("&date", date.today().isoformat())
        actual = self.__getFileContent(header)
        self.assertEquals(expected, actual)
        remove(header)

    def testUnitTestMain(self):
        unitMain = path.join("test", "main.cc")
        unitMainStandard = path.join("test", "main_standard.cc")
        self.__removeOnExists(unitMain)
        parser = TemplateParser("unittestmain.cpp", unitMain)
        parser.parse()
        expected = self.__getFileContent(unitMainStandard)
        expected = expected.replace("&date", date.today().isoformat())
        actual = self.__getFileContent(unitMain)
        self.assertEquals(expected, actual)
        remove(unitMain)

    def testUnitMakefile(self):
        unitMakefile = path.join("test", "main.cc")
        unitMakefileStandard = path.join("test", "makefile_standard.test")
        self.__removeOnExists(unitMakefile)
        parser = TemplateParser("makefile.test", unitMakefile)
        parser.parse()
        expected = self.__getFileContent(unitMakefileStandard)
        expected = expected.replace("&date", date.today().isoformat())
        actual = self.__getFileContent(unitMakefile)
        self.assertEquals(expected, actual)
        remove(unitMakefile)

    def __getFileContent(self, filepath):
        with open(filepath) as f:
            return f.read()
        return None

    def __removeOnExists(self, filepath):
        if path.exists(filepath):
            os.remove(filepath)

if __name__ == "__main__":
    unittest.main()