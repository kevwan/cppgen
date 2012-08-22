// $Id$

/**
 * @author ${author}
 * @date   ${date}
 */
#include <iostream>
#include <cppunit/BriefTestProgressListener.h>
#include <cppunit/CompilerOutputter.h>
#include <cppunit/extensions/TestFactoryRegistry.h>
#include <cppunit/TestResult.h>
#include <cppunit/TestResultCollector.h>
#include <cppunit/TestRunner.h>
using namespace CppUnit;

int main()
{
    // Create the event manager and test controller
    TestResult controller;

    // Add a listener that colllects test result
    TestResultCollector result;
    controller.addListener(&result);        

    // Add a listener that print dots as test run.
    BriefTestProgressListener progress;
    controller.addListener(&progress);      

    // Add the top suite to the test runner
    TestRunner runner;
    runner.addTest(TestFactoryRegistry::getRegistry().makeTest());
    runner.run(controller);

    // Print test in a compiler compatible format.
    CompilerOutputter outputter(&result, std::cerr);
    outputter.write(); 

    return result.wasSuccessful() ? 0 : 1;
}
