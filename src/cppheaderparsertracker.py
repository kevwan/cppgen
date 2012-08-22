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

from cppheaderobserver import CppHeaderObserver

class CppHeaderParserTracker(CppHeaderObserver):
    def __init__(self):
        CppHeaderObserver.__init__(self)

    def onPreParse(self, scopes):
        print "Parsing started..."

    def onPostParse(self, scopes):
        print "Parsing finished..."

    def onMacro(self, scopes, macro):
        print "Parsing macro %s..." % macro

    def onNamespace(self, scopes, namespace):
        print "Parsing namespace %s..." % namespace

    def onNamespaceEnd(self, scopes, namespace):
        print "Finished parsing namespace %s..." % namespace

    def onClass(self, scopes, template, className):
        print "Parsing class %s..." % className

    def onClassEnd(self, scopes, className):
        print "Finished parsing class %s..." % className

    def onEnum(self, scopes, enumName, enumMembers):
        print "Parsing enum %s..." % enumName

    def onFunctionDef(self, scopes, template, returnType, funcName, paramList, const):
        print "Parsing function %s..." % funcName

    def onFunctionDecl(self, scopes, template, returnType, funcName, paramList, const):
        print "Parsing function %s..." % funcName

    def onDtorDecl(self, scopes, dtorName):
        print "Parsing destructor %s..." % dtorName

    def onDtorDef(self, scopes, dtorName):
        print "Parsing destructor %s..." % dtorName

    def onCtorDecl(self, scopes, ctorName, paramList):
        print "Parsing constructor %s..." % ctorName

    def onCtorDef(self, scopes, ctorName, paramList):
        print "Parsing constructor %s..." % ctorName
