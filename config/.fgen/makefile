#############################################################################
# Makefile
#############################################################################

####### Compiler, tools and options
CXX                 = g++
CPPFLAGS            = -pipe -Wall -W -g -D_REENTRANT
INCPATH             = .
LIBS                =
EXECUTABLE          =
RM                  = rm -rf
SRCS                = $(wildcard *.cc)
OBJS                = $(patsubst %.cc,%.o,$(SRCS))
DEPS                = $(patsubst %.o,%.d,$(OBJS))
CPPFLAGS           += -MMD $(addprefix -I, $(INCPATH))
MISSING_DEPS        = $(filter-out $(wildcard $(DEPS)),$(DEPS))
MISSING_DEPS_SRCS   = $(wildcard $(patsubst %.d,%.cc,$(MISSING_DEPS)))
    
.PHONY : everything deps objs clean veryclean rebuild

everything : $(EXECUTABLE)

deps : $(DEPS)

objs : $(OBJS)

clean :
	@$(RM) $(OBJS)
	@$(RM) $(DEPS)
    
veryclean: clean
	@$(RM) $(EXECUTABLE)
    
rebuild: veryclean everything

ifneq ($(MISSING_DEPS),)
$(MISSING_DEPS):
	@$(RM) $(patsubst %.d,%.o,$@)
endif

-include $(DEPS)

$(EXECUTABLE) : $(OBJS)
	$(CXX) -o $(EXECUTABLE) $(OBJS) $(addprefix -l,$(LIBS))