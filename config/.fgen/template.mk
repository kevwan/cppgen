#############################################################################
# Makefile
#############################################################################

####### Compiler, tools and options
CXX      = g++
CXXFLAGS = -pipe -Wall -W -g -D_REENTRANT
INCPATH  = -I.
LIBS     = -lssl -lpthread
AR       = ar cqs
SRC      = $(wildcard *.cc)
OBJS     = $(SRC:%.cc=%.o)
TARGET   = 

compile : $(OBJS) 
	$(CXX) -o $(TARGET) $(OBJS) $(LIBS)

%.o : %.cc
	$(CXX) $(CXXFLAGS) $(INCPATH) -c -o $@ $<

clean :
	rm -rf $(OBJS) $(TARGET)
