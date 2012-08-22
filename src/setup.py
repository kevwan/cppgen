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

from os import getenv
from os import path
from sys import exit
from os import makedirs
from shutil import copy

pyFilesToDeploy = [
        "cppgen.py",
        "cppheadergen.py",
        "cppheaderobserver.py",
        "cppheaderparser.py",
        "cppheaderparsertracker.py",
        "cppunitgen.py",
        "docgen.py",
        "fgconfig.py",
        "fgen.py",
        "fgutils.py",
        "filedepot.py",
        "filegenerator.py",
        "makefilegen.py",
        "templateparser.py"
    ]

configFilesToDeploy = [
        "fgen.xml",
        "makefile",
        "makefile.test",
        "template.cpp",
        "template.h",
        "template.l",
        "unittestclass.cpp",
        "unittestmain.cpp"
    ]

def getHomePath():
    home = getenv("HOME")
    if home == None:
        exit("Error: 'HOME' environment variable has NOT been set")
    return home

def deployFiles():
    home = getHomePath()
    installPath = path.join(home, "local/scripts/fgen")
    if not path.exists(installPath):
        makedirs(installPath)
    map(lambda file:copy(file, path.join(installPath, file)), pyFilesToDeploy)

    configPath = path.join(home, ".fgen")
    if not path.exists(configPath):
        makedirs(configPath)
    map(lambda file:copy(path.join("../config/.fgen", file), path.join(configPath, file)), configFilesToDeploy)

def main():
    deployFiles()
    print "Notice: the only one step for you to do manually is:\n"
    print "Add \"alias fgen <path_of_python_2.5> %s\" to your shell configuration." % \
        path.join(getHomePath(), "local/scripts/fgen/fgen.py")
    print "\nfgen has been set up successfully! Enjoy it! :)"

if __name__ == "__main__":
    try:
        main()
    except Exception, ex:
        print "Error: fgen set up failed, %s" % ex
        print "\nPlease report bugs to <wanjunfeng@gmail.com>, thanks!"