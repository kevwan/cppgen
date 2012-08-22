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
from pyparsing import *
from cppheaderobserver import CppHeaderObserver
from cppheaderparsertracker import CppHeaderParserTracker

__doc__ = \
"""
cppheaderparser module is the module that parses cpp header file to get the definition
of classes, functions etc. You can add a CppHeaderObserver object into CppHeaderParser
object to observe the events.
"""

class Scope:
    def __init__(self, scopeType, name):
        self.__type = scopeType
        self.__name = name
        self.__access = "private" if type == "class" or type == "tclass" else None
        self.__inside = False

    def getType(self):
        return self.__type

    def getName(self):
        return self.__name

    def getAccess(self):
        return self.__access

    def setAccess(self, access):
        self.__access = access

    def setInside(self):
        self.__inside = True

    def getInside(self):
        return self.__inside

class ContextParser:
    def __init__(self, parser, transformParser, statuses=None):
        self.__parser = parser
        self.__transformParser = transformParser
        self.__status = statuses if isinstance(statuses, list) else []

    def getParser(self):
        return self.__parser

    def getTransformParser(self):
        return self.__transformParser

    def valid(self, status):
        return [s for s in self.__status if s == "all" or s == status]

class CppHeaderParser:
    """
    This class is the cpp header parser class. It uses pyparsing module to convinient the parsing.
    It's an observable class, that means you can add a CppHeaderObserver object to it. And it will
    call your overriden methods from CppHeaderObserver interface.
    """
    def __init__(self, header):
        """
        Construct the CppHeaderParser object.
        
        Parameters:
            header(string): The path of the header file.
        """
        self.__header = header
        self.__observers = [CppHeaderParserTracker()]
        self.__lineno = -1
        self.__lines = []
        self.__currentLine = None
        self.__scopes = []

        # BNF for pyparsing
        self.__ident = Regex(r"[A-Za-z_]\w*")
        self.__lparen = Literal("(").suppress()
        self.__rparen = Literal(")").suppress()
        self.__unsigned = Keyword("unsigned")
        self.__int = Keyword("int")
        self.__short = Keyword("short")
        self.__long = Keyword("long")
        self.__double = Keyword("double")
        self.__float = Keyword("float")
        self.__char = Keyword("char")
        self.__wchar_t = Keyword("wchar_t")
        self.__bool = Keyword("bool")
        self.__signed = Keyword("signed") 
        self.__void = Keyword("void") 
        self.__template = Keyword("template")
        self.__class = Keyword("class")
        self.__virtual = Keyword("virtual")
        self.__static = Keyword("static")
        self.__operator = Keyword("operator")
        self.__const = Keyword("const").setResultsName("const")
        self.__semicolon = Literal(";").setResultsName("semicolon")
        self.__typename = Keyword("typename")
        self.__typename = (self.__typename | self.__class)
        self.__pointerAndRef = ZeroOrMore(Literal("*")) + Optional(Literal("&"))
        self.__nativeType = OneOrMore((self.__unsigned ^ self.__int ^ self.__short ^ \
                        self.__long ^ self.__double ^ self.__float ^ self.__char ^ \
                        self.__wchar_t ^ self.__bool ^ self.__signed ^ self.__void)) \
                        + self.__pointerAndRef
        self.__userDefType = delimitedList(self.__ident, "::", combine=True)
        self.__simpleType = self.__userDefType + Optional("<" + delimitedList(self.__ident) \
                        + self.__pointerAndRef + ">") + self.__pointerAndRef
        self.__intermediateType = self.__userDefType + Optional("<" \
                        + delimitedList(Group(self.__simpleType)) + ">") \
                        + self.__pointerAndRef
        self.__complexType = self.__userDefType + Optional("<" \
                        + delimitedList(Group(self.__intermediateType)) + ">") \
                        + self.__pointerAndRef
        self.__type = Group(Optional(self.__const) + (self.__nativeType | self.__complexType))
        self.__returnType = self.__type.setResultsName("returnType")
        self.__templateParamList = Group(delimitedList(self.__typename.suppress() \
                + self.__ident + Optional("=" + self.__type).suppress())) \
                .setResultsName("templateParamList")
        self.__param = Optional(self.__ident) + Optional("=" + SkipTo(")")).suppress()
        self.__paramList = Optional(delimitedList(Group(self.__type + self.__param))) \
                .setResultsName("paramList")
        self.__templateDecl = Optional(self.__template.suppress() \
                + Literal("<").suppress() + self.__templateParamList \
                + Literal(">").suppress())
        #end BNF

        self.__hasMoreLines = lambda:self.__lines
        self.__getLastScope = lambda:self.__scopes[-1] if self.__scopes else None
        self.__eraseLastScope = lambda:self.__scopes.pop()
        self.__inFuncBody = lambda:[scope for scope in self.__scopes \
                    if scope.getType() == "function" and scope.getInside()]
        self.__enumParser = self.__getEnumParser()
        self.__parsers = [
             self.__getMacroParser(),
             self.__getSharpParser(),
             self.__getAccessModifierParser(),
             self.__getNamespaceParser(),
             self.__getClassParser(),
             self.__getEnumDeclParser(),
             self.__getOperatorParenParser(),
             self.__getOperatorParser(),
             self.__getFunctionParser(),
             self.__getDtorParser(),
             self.__getCtorParser(),
             self.__getStartBraceParser(),
             self.__getEndBraceParser(),
             self.__getStatementParser()
        ]

    def addObserver(self, observer):
        """
        Add an observer object into the parser.
        
        Parameters:
            observer(CppHeaderObserver): the observer object, the parser object will call
            its methods automatically when events happen.
        """
        self.__observers.append(observer)

    def removeObserver(self, observer):
        """
        Remove the observer object from the parser.
        
        observer(CppHeaderObserver): the observer object to remove.
        """
        self.__observers.remove(observer)

    def getLineNo(self):
        """
        Get current line number.
        """
        return self.__lineno

    def isPartOfTemplateClass(self):
        """
        Return if the current element is part of a template class.
        """
        return [x for x in self.__scopes if x.getType() == "tclass"]

    def parse(self):
        """
        Parse the header file. During the parsing, the observers might be called
        due to the events that might happen.
        """
        map(lambda ob:ob.onPreParse(self.__scopes), self.__observers)

        self.__parseFile()
        while self.__hasMoreLines():
            self.__lineno, ln = self.__nextLine()
            map(lambda ob:ob.onPreLine(self.__scopes, ln), self.__observers)
            if ln:
                matched = False
                for contextParser in self.__parsers:
                    status = self.__getStatus()
                    if not contextParser.valid(status):
                        continue
                    parser = contextParser.getParser()
                    transformParser = contextParser.getTransformParser()
                    try:
                        results = parser.parseString(ln)
                        if transformParser:
                            transformParser.setParseAction(replaceWith(""))
                            remaining = transformParser.transformString(ln)
                            remaining = remaining.strip()
                            if remaining:
                                self.__lines.insert(0, (self.__lineno, remaining))
                        matched = True
                        break
                    except ParseException:
                        continue
                if not matched:
                    self.__concatWithNextLine(ln)
            map(lambda ob:ob.onPostLine(self.__scopes, ln), self.__observers)

        map(lambda ob:ob.onPostParse(self.__scopes), self.__observers)

    def assemblyTemplate(self, seq):
        out = "template <"
        sep = ""
        for item in seq:
            out = sep.join((out, "typename %s" % item))
            sep = ", "
        out += ">"
        return out

    def assemblyType(self, seq):
        out = ""
        for item in seq:
            if isinstance(item, ParseResults):
                sep = ", "
                if out and out[-1] == "<":
                    sep = ""
                out = sep.join((out, self.assemblyType(item)))
            else:
                sep = ""
                if out and item:
                    ch1 = out[-1]
                    ch2 = item[0]
                    if ch1 == "," or (ch1.isalnum() and ch2.isalnum()) or (ch1 == ">" and ch2 == ">"):
                        sep = " "
                out = sep.join((out, item))
        return out

    def assemblyParamList(self, seq):
        out = ""
        sep = ""
        for item in seq:
            typeParam = " ".join((self.assemblyType(item[0]), item[1]))
            out = sep.join((out, typeParam))
            sep = ", "
        return out

    def __getMacroParser(self):
        _var = Word(alphanums + "_").setResultsName("macroName")
        _value = Optional(Regex(r".*")).setResultsName("value")
        _macroDef = "#" + "define" + _var + _value
        _macroDef.setName("macroDef")
        _tparser = _macroDef.copy()
        _macroDef.setParseAction(self.__processMacro)
        _tparser.setParseAction(replaceWith(""))
        return ContextParser(_macroDef, _tparser, ["all"])

    def __getSharpParser(self):
        _lineStartWithSharp = "#" + Regex(r".*")
        _lineStartWithSharp.setName("lineStartWithSharp")
        _tparser = _lineStartWithSharp.copy()
        _tparser.setParseAction(replaceWith(""))
        return ContextParser(_lineStartWithSharp, _tparser, ["all"])

    def __getAccessModifierParser(self):
        _modifier = oneOf("public protected private").setResultsName("modifier")
        _modifierDef = _modifier + ":"
        _modifierDef.setName("modifierDef")
        _tparser = _modifierDef.copy()
        _modifierDef.setParseAction(self.__processAccessModifier)
        _tparser.setParseAction(replaceWith(""))
        return ContextParser(_modifierDef, _tparser, ["class"])

    def __getNamespaceParser(self):
        _namespace = Keyword("namespace")
        _namespaceName = self.__ident.setResultsName("namespaceName")
        _namespaceDef = _namespace + Optional(_namespaceName)
        _namespaceDef.setName("namespaceDef")
        _tparser = _namespaceDef.copy()
        _namespaceDef.setParseAction(self.__processNamespace)
        _tparser.setParseAction(replaceWith(""))
        return ContextParser(_namespaceDef, _tparser, ["namespace"])

    def __getClassParser(self):
        _class = (Keyword("class") | Keyword("struct")).setResultsName("classOrStruct")
        _className = self.__ident.setResultsName("className")
        _classDef = self.__templateDecl + _class + _className
        _classDef.setName("classDef")
        _tparser = _classDef.copy()
        _classDef.setParseAction(self.__processClass)
        _tparser.setParseAction(replaceWith(""))
        return ContextParser(_classDef, _tparser, ["namespace", "class"])

    def __getEnumDeclParser(self):
        _enumDecl = Keyword("enum").suppress() + \
                    Optional(self.__ident).setResultsName("enumName")
        _enumDecl.setName("enumDecl")
        _enumDecl.setParseAction(self.__processEnumDecl)
        return ContextParser(_enumDecl, None, ["namespace", "class"])

    def __getOperatorParenParser(self):
        _operatorParenDef = self.__templateDecl \
                + Optional(self.__static).setResultsName("static") \
                + Optional(self.__virtual).setResultsName("virtual") \
                + self.__returnType \
                + Combine(self.__operator + "(" + ")").setResultsName("funcName") \
                + self.__lparen + self.__paramList + self.__rparen \
                + Optional(self.__const).setResultsName("const") \
                + Optional(Literal("=") + Literal("0")).setResultsName("pureVirtual") \
                + Optional(self.__semicolon)
        _operatorParenDef.setName("operatorParenDef")
        _tparser = _operatorParenDef.copy()
        _operatorParenDef.setParseAction(self.__processFunction)
        _tparser.setParseAction(replaceWith(""))
        return ContextParser(_operatorParenDef, _tparser, ["namespace", "class"])

    def __getOperatorParser(self):
        _operatorDef = self.__templateDecl \
                + Optional(self.__static).setResultsName("static") \
                + Optional(self.__virtual).setResultsName("virtual") \
                + Optional(self.__returnType + FollowedBy(self.__operator)) \
                + Combine(self.__operator + SkipTo("(")).setResultsName("funcName") \
                + self.__lparen + self.__paramList + self.__rparen \
                + Optional(self.__const).setResultsName("const") \
                + Optional(Literal("=") + Literal("0")).setResultsName("pureVirtual") \
                + Optional(self.__semicolon)
        _operatorDef.setName("operatorDef")
        _tparser = _operatorDef.copy()
        _operatorDef.setParseAction(self.__processFunction)
        _tparser.setParseAction(replaceWith(""))
        return ContextParser(_operatorDef, _tparser, ["namespace", "class"])

    def __getFunctionParser(self):
        _functionDef =  self.__templateDecl \
                + Optional(self.__static).setResultsName("static") \
                + Optional(self.__virtual).setResultsName("virtual") \
                + self.__returnType \
                + self.__ident.setResultsName("funcName") \
                + self.__lparen + self.__paramList + self.__rparen \
                + Optional(self.__const).setResultsName("const") \
                + Optional(Literal("=") + Literal("0")).setResultsName("pureVirtual") \
                + Optional(self.__semicolon)
        _functionDef.setName("functionDef")
        _tparser = _functionDef.copy()
        _functionDef.setParseAction(self.__processFunction)
        _tparser.setParseAction(replaceWith(""))
        return ContextParser(_functionDef, _tparser, ["namespace", "class"])

    def __getDtorParser(self):
        _dtorDef = Optional(self.__virtual) + Combine("~" + self.__ident).setResultsName("funcName") \
                + "(" + ")" + Optional(self.__semicolon)
        _dtorDef.setName("dtorDef")
        _tparser = _dtorDef.copy()
        _dtorDef.setParseAction(self.__processDestructor)
        _tparser.setParseAction(replaceWith(""))
        return ContextParser(_dtorDef, _tparser, ["class"])

    def __getCtorParser(self):
        _ctorDef = self.__ident.setResultsName("funcName") + self.__lparen \
                + self.__paramList + self.__rparen + Optional(self.__semicolon)
        _ctorDef.setName("ctorDef")
        _tparser = _ctorDef.copy()
        _ctorDef.setParseAction(self.__processConstructor)
        _tparser.setParseAction(replaceWith(""))
        return ContextParser(_ctorDef, _tparser, ["class"])

    def __getStartBraceParser(self):
        _startBrace = Optional(SkipTo("{")).setResultsName("skipped") + "{"
        _startBrace.setName("startBrace")
        _tparser = _startBrace.copy()
        _startBrace.setParseAction(self.__processStartBrace)
        _tparser.setParseAction(replaceWith(""))
        return ContextParser(_startBrace, _tparser, ["all"])

    def __getEndBraceParser(self):
        _endBrace = Optional(SkipTo("}")).suppress() + "}" + ZeroOrMore(";")
        _endBrace.setName("endBrace")
        _tparser = _endBrace.copy()
        _endBrace.setParseAction(self.__processEndBrace)
        _tparser.setParseAction(replaceWith(""))
        return ContextParser(_endBrace, _tparser, ["all"])

    def __getStatementParser(self):
        _statement = Optional(SkipTo(";")).suppress() + ";" # ignore the statements
        _statement.setName("statement")
        _tparser = _statement.copy()
        _tparser.setParseAction(replaceWith(""))
        return ContextParser(_statement, _tparser, ["all"])

    def __getEnumParser(self):
        _varDef = self.__ident + Optional(Literal("=") + Regex(r"[^,}]*")).suppress()
        _varList = delimitedList(_varDef)
        _enumDef = Keyword("enum").suppress() + \
                    Optional(self.__ident).setResultsName("enumName") + \
                    Literal("{").suppress() + \
                    Group(_varList).setResultsName("enumVarList") + Optional(",") + \
                    Literal("}").suppress() + \
                    Literal(";").suppress()
        _enumDef.setName("enumDef")
        _enumDef.setParseAction(self.__processEnumDef)
        return _enumDef

    def __parseFile(self):
        lnno = 0
        inComment = False
        for ln in open(self.__header):
            lnno += 1

            if inComment:
                try:
                    pos = ln.index(r"*/")
                    ln = ln[pos+2:]
                    inComment = False
                except ValueError:
                    continue

            try:
                pos = ln.index(r"//")
                ln = ln[0:pos]
            except ValueError:
                pass

            try:
                pos = ln.index(r"/*")
                try:
                    epos = ln.index(r"*/", pos + 2)
                    ln = " ".join((ln[:pos], ln[epos+2:]))
                except ValueError:
                    ln = ln[:pos]
                    inComment = True
                    continue
            except ValueError:
                pass

            ln = ln.strip()
            if ln:
                self.__lines.append((lnno, ln))

    def __getStatus(self):
        status = None
        if not self.__scopes:
            status = "namespace"
        else:
            status = self.__scopes[-1].getType()
            if status == "tclass":
                status = "class"
        return status

    def __processMacro(self, results):
        macro = results.macroName
        value = results.value
        if value and value[-1] == "\\":
            while self.__hasMoreLines():
                value = value[0:-1] + self.__nextLine()[1].rstrip()
                if value[-1] != "\\":
                    break
        map(lambda ob:ob.onMacro(self.__scopes, macro), self.__observers)

    def __processAccessModifier(self, results):
        modifier = results.modifier
        scope = self.__getLastScope()
        if scope.getType() == "class" or scope.getType() == "tclass":
            scope.setAccess(modifier)

    def __processNamespace(self, results):
        nsName = results.namespaceName
        map(lambda ob:ob.onNamespace(self.__scopes, nsName), self.__observers)
        self.__scopes.append(Scope("namespace", nsName))

    def __processClass(self, results):
        template = results.templateParamList
        clsName = results.className
        map(lambda ob:ob.onClass(self.__scopes, template, clsName), self.__observers)

        scope = None
        if template:
            scope = Scope("tclass", clsName)
        else:
            scope = Scope("class", clsName)

        if results.classOrStruct == "struct":
            scope.setAccess("public")
        self.__scopes.append(scope)

    def __processEnumDecl(self, results):
        lnno, content = self.__currentLine
        try:
            self.__enumParser.parseString(content)
        except ParseException:
            self.__concatWithNextLine(content)
            while self.__hasMoreLines():
                lnno, content = self.__nextLine()
                try:
                    self.__enumParser.parseString(content)
                    break
                except ParseException:
                    self.__concatWithNextLine(content)

    def __processEnumDef(self, results):
        enumName = results.enumName
        enumMembers = results.enumVarList
        map(lambda ob:ob.onEnum(self.__scopes, enumName, enumMembers), self.__observers)        

    def __processFunction(self, results):
        if not results.semicolon:
            self.__processFunctionDef(results)
            self.__scopes.append(Scope("function", results.funcName))
        else:
            template = results.templateParamList
            returnType = self.assemblyType(results.returnType)
            funcName = results.funcName
            paramList = results.paramList
            const = results.const
            map(lambda ob:ob.onFunctionDecl(self.__scopes, template, returnType, \
                    funcName, paramList, const), self.__observers)

    def __processFunctionDef(self, results):
        template = results.templateParamList
        returnType = self.assemblyType(results.returnType)
        funcName = results.funcName
        paramList = results.paramList        
        const = results.const
        map(lambda ob:ob.onFunctionDef(self.__scopes, template, returnType, \
               funcName, paramList, const), self.__observers)

    def __processStartBrace(self, results):
        scope = self.__getLastScope()
        if scope:
            scopeType = scope.getType()

            if scope.getInside():
                self.__scopes.append(Scope("skip", "unknown"))

            if scopeType == "namespace":
                if not scope.getInside():
                    scope.setInside()
                    map(lambda ob:ob.onNamespaceStart(self.__scopes, scope.getName()), self.__observers)
            elif scopeType == "class":
                if not scope.getInside():
                    scope.setInside()
                    map(lambda ob:ob.onClassStart(self.__scopes, scope.getName()), self.__observers)
            elif scopeType == "function":
                if not scope.getInside():
                    scope.setInside()

    def __processEndBrace(self, results):
        scope = self.__getLastScope()
        if scope:
            type = scope.getType()
            if type == "namespace":
                map(lambda ob:ob.onNamespaceEnd(self.__scopes, scope.getName()), self.__observers)
            elif type == "class":
                map(lambda ob:ob.onClassEnd(self.__scopes, scope.getName()), self.__observers)

            self.__eraseLastScope()

    def __processConstructor(self, results):
        if not results.semicolon:
            self.__processCtorDef(results)
        else:
            map(lambda ob:ob.onCtorDecl(self.__scopes, results.funcName, results.paramList), self.__observers)

    def __processCtorDef(self, results):
        ctorName = results.funcName
        paramList = results.paramList
        map(lambda ob:ob.onCtorDef(self.__scopes, ctorName, paramList), self.__observers)
        self.__scopes.append(Scope("function", ctorName))

    def __processDestructor(self, results):
        if not results.semicolon:
            self.__processDtorDef(results)
        else:
            map(lambda ob:ob.onDtorDecl(self.__scopes, results.funcName), self.__observers)

    def __processDtorDef(self, results):
        dtorName = results.funcName
        map(lambda ob:ob.onDtorDef(self.__scopes, dtorName), self.__observers)
        self.__scopes.append(Scope("function", dtorName))

    def __nextLine(self):
        self.__currentLine = self.__lines.pop(0)
        return self.__currentLine

    def __concatWithNextLine(self, s):
        if self.__hasMoreLines():
            if s:
                nextLine = self.__nextLine()[1]
                ln = " ".join((s, nextLine)).strip()
                self.__lines.insert(0, (self.__lineno, ln))
