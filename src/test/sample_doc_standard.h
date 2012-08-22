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
    /// <summary>
    /// </summary>
    struct SampleStruct
    {
        /// <summary>
        /// </summary>
        /// <param name="s"></param>
        void printStruct(const string& s) const;

    private:
        /// <summary>
        /// </summary>
        /// <returns></returns>
        unsigned int getPrivate() const;
    };

    /// <summary>
    /// </summary>
    class Sample
    {
        /// <summary>
        /// </summary>
        enum { first };

        /// <summary>
        /// </summary>
        template <typename T>
        class InnerClass
        {
        public:
            /// <summary>
            /// </summary>
            /// <returns></returns>
            int getCount() const;
        };
    public:
        /// <summary>
        /// </summary>
        Sample();
        /// <summary>
        /// </summary>
        virtual ~Sample() {}
        /// <summary>
        /// </summary>
        template <typename T>
        void print();
        /// <summary>
        /// </summary>
        /// <returns></returns>
        operator int();
        /// <summary>
        /// </summary>
        /// <returns></returns>
        ostream& operator<<();
        /// <summary>
        /// </summary>
        /// <returns></returns>
        Sample& operator++();
        /// <summary>
        /// </summary>
        /// <param name="other"></param>
        /// <returns></returns>
        bool operator==(const Sample& other) const;

        /// <summary>
        /// </summary>
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
