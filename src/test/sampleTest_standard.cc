// $Id$

/**
 * @author Kevin Wan <wanjunfeng@gmail.com>
 * @date   &date
 */
#include <cppunit/extensions/HelperMacros.h>
#include "sample.h"

using namespace keggle;

class SampleStructTest : public CppUnit::TestFixture
{
    CPPUNIT_TEST_SUITE(SampleStructTest);
    CPPUNIT_TEST(testPrintStruct);
    CPPUNIT_TEST_SUITE_END();

public:
    void setUp();
    void tearDown();

    void testPrintStruct();
};

CPPUNIT_TEST_SUITE_REGISTRATION(SampleStructTest);

void SampleStructTest::setUp()
{
}

void SampleStructTest::tearDown()
{
}

void SampleStructTest::testPrintStruct()
{
    CPPUNIT_FAIL("not implemented");
}

class SampleTest : public CppUnit::TestFixture
{
    CPPUNIT_TEST_SUITE(SampleTest);
    CPPUNIT_TEST(testConstructor);
    CPPUNIT_TEST(testPrint);
    CPPUNIT_TEST(testNothingToGen);
    CPPUNIT_TEST_SUITE_END();

public:
    void setUp();
    void tearDown();

    void testConstructor();
    void testPrint();
    void testNothingToGen();
};

CPPUNIT_TEST_SUITE_REGISTRATION(SampleTest);

void SampleTest::setUp()
{
}

void SampleTest::tearDown()
{
}

void SampleTest::testConstructor()
{
    CPPUNIT_FAIL("not implemented");
}

void SampleTest::testPrint()
{
    CPPUNIT_FAIL("not implemented");
}

void SampleTest::testNothingToGen()
{
    CPPUNIT_FAIL("not implemented");
}

