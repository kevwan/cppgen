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

class CppHeaderObserver:
    def __init__(self):
        self.__parser__ = None

    def setParser(self, parser):
        self.__parser__ = parser

    def onPreParse(self, scopes):
        pass
    def onPostParse(self, scopes):
        pass
    def onPreLine(self, scopes, ln):
        pass
    def onPostLine(self, scopes, ln):
        pass
    def onMacro(self, scopes, macro):
        pass
    def onNamespace(self, scopes, namespace):
        pass
    def onNamespaceStart(self, scopes, namespace):
        pass
    def onNamespaceEnd(self, scopes, namespace):
        pass
    def onClass(self, scopes, template, className):
        pass
    def onClassStart(self, scopes, className):
        pass
    def onClassEnd(self, scopes, className):
        pass
    def onEnum(self, scopes, enumName, enumMembers):
        pass
    def onFunctionDef(self, scopes, template, returnType, funcName, paramList, const):
        pass
    def onFunctionDecl(self, scopes, template, returnType, funcName, paramList, const):
        pass
    def onDtorDecl(self, scopes, dtorName):
        pass
    def onDtorDef(self, scopes, dtorName):
        pass
    def onCtorDecl(self, scopes, ctorName, paramList):
        pass
    def onCtorDef(self, scopes, ctorName, paramList):
        pass
