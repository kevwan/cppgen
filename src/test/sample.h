#ifndef SAMPLE_H
#define SAMPLE_H

/**
 * @author kevin wan
 * @date   2006-10-25
 */

// simple comment test
/* complex comment test */

#define dummy unknownmacro

namespace keggle // another comment test
{
    struct SampleStruct
    {
        void printStruct(const string& s) const;

    private:
        unsigned int getPrivate() const;
    };

    class Sample
    {
        enum { first };

        template <typename T>
        class InnerClass
        {
        public:
            int getCount() const;
        };
    public:
        Sample();
        virtual ~Sample() {}
        template <typename T>
        void print();
        operator int();
        ostream& operator<<();
        Sample& operator++();
        bool operator==(const Sample& other) const;

        void nothingToGen() const
        {
            // do nothing here
            if (true)
            {
                // do something here
            }
        }
    };
}

#endif // SAMPLE_H
