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

from xml.dom import minidom
from os import path
from os import getenv
from sys import stdout

class Option:
    def __init__(self, shortOpt, longOpt, hasArg, package, slotClass, priority, comment):
        self.__shortOpt = shortOpt
        self.__longOpt = longOpt
        self.__hasArg = hasArg
        self.__package = package
        self.__slotClass = slotClass
        self.__priority = priority
        self.__comment = comment
        
    def getShortOpt(self):
        return self.__shortOpt
    
    def getLongOpt(self):
        return self.__longOpt
    
    def getHasArg(self):
        return self.__hasArg
    
    def getPackage(self):
        return self.__package
    
    def getSlotClass(self):
        return self.__slotClass
    
    def getPriority(self):
        return self.__priority
    
    def getComment(self):
        return self.__comment
    
    def comparePriority(opt1, opt2):
        pri1 = eval(opt1.getPriority())
        pri2 = eval(opt2.getPriority())
        return 1 if pri1 > pri2 else 0 if pri1 == pri2 else -1

class XmlConfig:
    __configPath = None
    __rootElement = None
    __options = None

    def __init__(self):
        if not self.__rootElement:
            xmlFile = path.join(self.getConfigPath(), "fgen.xml")
            doc = minidom.parse(xmlFile)
            self.__rootElement = doc.documentElement

    def getConfigPath(self):
        if not self.__configPath:
            home = getenv("HOME")
            if home == None:
                exit("Error: you need to set HOME environment variable")
            self.__configPath = path.join(home, ".fgen")
        return self.__configPath

    def getAuthor(self):
        return self.__getSingleValue(self.__rootElement, "author")

    def getWrapperPrefix(self):
        return self.__getSingleValue(self.__rootElement, "wrapper_prefix")

    def getCppSuffix(self):
        suffix = self.__getSingleValue(self.__rootElement, "default_cpp_suffix")
        return ".cc" if suffix == None or suffix == "" else suffix

    def getUnitTestDir(self):
        return self.__getSingleValue(self.__rootElement, "unit_test_dir")
    
    def get(self, key):
        return self.__getSingleValue(self.__rootElement, key)

    def getOptions(self):
        if not self.__options:
            self.__options = []
            nodes = self.__rootElement.getElementsByTagName("options")        
            if len(nodes) != 1:
                raise ValueError("Error: there are less or more than 1 node for options")
            
            nodes = nodes[0].getElementsByTagName("option")
            for node in nodes:
                shortOpt = self.__getSingleValue(node, "short_option")
                longOpt = self.__getSingleValue(node, "long_option")
                hasArg = self.__getSingleValue(node, "has_argument")
                package = self.__getSingleValue(node, "package")
                slotClass = self.__getSingleValue(node, "slot_class")
                priority = self.__getSingleValue(node, "parse_order")
                comment = self.__getSingleValue(node, "comment")
                self.__options.append(Option(shortOpt, longOpt, hasArg, package,
                        slotClass, priority, comment))
            self.__options.sort(Option.comparePriority)
        return self.__options
    
    def getShortOptions(self):
        shortOptions = ""
        options = self.getOptions()
        for option in options:
            shortOpt = option.getShortOpt()
            hasArg = option.getHasArg()
            shortOptions = shortOptions + shortOpt
            if hasArg.lower() == "true":
                shortOptions = shortOptions + ':'
        return shortOptions
    
    def getLongOptions(self):
        longOptions = []
        options = self.getOptions()
        for option in options:
            longOpt = option.getLongOpt()
            hasArg = option.getHasArg()
            if hasArg.lower() == "true":
                longOpt = longOpt.strip() + '='
            longOptions.append(longOpt)
        return longOptions
    
    def printOptionUsage(self, output = stdout):
        print>>output, "Options:"
        for option in self.getOptions():
            shortOpt = option.getShortOpt()
            longOpt = option.getLongOpt()
            hasArg = option.getHasArg()
            comment = option.getComment()
            if hasArg.lower() == "true":
                print>>output, "  -%s %s, --%s=%s" % (shortOpt, longOpt.upper(),
                        longOpt, longOpt.upper())
            else:
                print>>output, "  -%s, --%s" % (shortOpt, longOpt)
            print>>output, "      %s" % comment

    def __getValueList(self, element, name):
        values = []
        nodes = element.getElementsByTagName(name)
        for node in nodes:
            if node.nodeType == node.ELEMENT_NODE:
                for nd in node.childNodes:
                    if nd.nodeType == node.TEXT_NODE or nd.nodeType == node.CDATA_SECTION_NODE:
                        values.append(nd.data)
        return values

    def __getSingleValue(self, element, name):
        nodes = element.getElementsByTagName(name)
        if len(nodes) != 1:
            raise ValueError("Error: there are less or more than 1 node for %" % name)

        if nodes[0].nodeType == nodes[0].ELEMENT_NODE:
            for node in nodes[0].childNodes:
                if node.nodeType == node.TEXT_NODE or node.nodeType == node.CDATA_SECTION_NODE:
                    return node.data
        return ""
