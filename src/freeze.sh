#!/bin/tcsh

rm -rf dist
python freeze.py -o dist fgen.py cppgen.py cppheadergen.py cppheaderobserver.py cppheaderparser.py cppheaderparsertracker.py cppunitgen.py docgen.py fgconfig.py fgutils.py filedepot.py filegenerator.py makefilegen.py pyparsing.py templateparser.py
cd dist
make
strip fgen
cp -f fgen ..
cd ..
rm -rf dist
