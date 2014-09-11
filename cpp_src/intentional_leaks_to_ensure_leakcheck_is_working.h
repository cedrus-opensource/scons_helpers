
#ifndef CEDRUS_UTILITY_INTENTIONAL_LEAKS
#define CEDRUS_UTILITY_INTENTIONAL_LEAKS

#include <cstring>

namespace Cedrus
{
    struct Intentional_Leak
    {
        Intentional_Leak()
        {
            std::strcpy( leak, "Leaked on purpose" );
            leak[17]=0;
        }
        char leak[18];
    };

    /**
       There are sometimes several settings and "hoops to jump through" to get
       AUTOMATIC leak-dumps enabled on a developer computer.  Therefore, we
       like to leak one object on purpose during every debugging session, so
       that we know that if we get the auto-leak-dump of THIS LEAK, then we
       can assume the leak-dumps are up and running.
     */
    void create_one_intentional_leak()
    {
        Intentional_Leak* leaked = new Intentional_Leak;
        (void) leaked; // suppress warning about unused ('not referenced') local variable
        return;
    }

} // end namespace Cedrus

#endif // CEDRUS_UTILITY_INTENTIONAL_LEAKS
