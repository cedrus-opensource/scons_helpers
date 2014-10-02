

#ifndef CEDRUS_UTILITY_CODE_CASSERT_WRAPPER
#define CEDRUS_UTILITY_CODE_CASSERT_WRAPPER


// If NDEBUG is defined as a macro name at the point in the source code where <cassert> is included, then assert does nothing.

#ifdef NDEBUG
// Hard-enabling of assert() even if NDEBUG is defined
#    define NDEBUG_WAS_SET_CEDRUS_HEADER
#    undef NDEBUG
#
#    include <cassert>
#endif

#include <iostream> // for std::cerr
#include <signal.h> // for raise
#include <stdlib.h> // for getenv

#if defined(_WIN32)
#    include <Windows.h>
#endif // #if defined(_WIN32)

#if defined(__APPLE__)
#    include <CoreFoundation/CoreFoundation.h>
#endif // defined(__APPLE__)

namespace Cedrus
{
    // break into the debugger
    inline void TrapDebug()
    {
        #if defined(_WIN32)
            DebugBreak();
        #elif defined(__APPLE__)
            raise(SIGTRAP);
        #else
            // TODO
        #endif // Win/Apple
    }

    inline void OptionToContinue
    (
     const char* title,
     const char* message,
     const char* filename,
     const int line,
     const char* funcname
    )
    {
        #if defined(_WIN32)

        // suppress warnings about unused parameters on win32:
        (void) title;
        (void) message;
        (void) filename;
        (void) line;
        (void) funcname;

        #elif defined(__APPLE__)

        std::cerr << title << ":\n";
        std::cerr << funcname << "\n";
        std::cerr << filename << ":" << line << "\n";
        std::cerr << message << "\n";

        CFStringRef headerRef =  CFStringCreateWithCString( NULL, title,    kCFStringEncodingUTF8 );
        CFStringRef messageRef = CFStringCreateWithCString( NULL, message,  kCFStringEncodingUTF8 );

        CFStringRef button1 =    CFStringCreateWithCString( NULL, "Break",  kCFStringEncodingUTF8 ); // defaultButtonTitle
        CFStringRef button2 =    CFStringCreateWithCString( NULL, "Continue", kCFStringEncodingUTF8 ); // alternateButtonTitle

        CFOptionFlags response;

        CFUserNotificationDisplayAlert
            ( 0, // timeout. (apparently in seconds) The amount of time to wait for the user to dismiss
                 // the notification dialog before the dialog dismisses
                 // itself. Pass 0 to have the dialog never time out.
              kCFUserNotificationCautionAlertLevel,
              NULL, // iconURL
              NULL, // soundURL
              NULL, // localizationURL
              headerRef,
              messageRef,
              button1, // defaultButtonTitle
              button2, // alternateButtonTitle
              NULL, // otherButtonTitle
              &response);

        CFRelease(headerRef);
        CFRelease(messageRef);
        CFRelease(button1);
        CFRelease(button2);

        if ( response == kCFUserNotificationDefaultResponse )
        {
            // choice was "Break"
            TrapDebug();
        }
        else if ( response == kCFUserNotificationAlternateResponse )
        {
            // choice was "Continue"
            // do nothing
        }
        else // if you add a 3rd button, this would be kCFUserNotificationOtherResponse
        {
            // either the notification timed out by itself (no user interaction),
            // or else the user hit the ESCAPE key

            std::cerr << "ignoring opportunity to debug the FAIL (either due to inaction or ESC key)\n";
        }
        #else
            // TODO
        #endif // Win/Apple
    }

    inline void Ced_Asrt_Mac
    ( const char* message,
      const char* filename,
      const int line,
      const char* funcname )
    {
        if ( getenv("CEDRUS_SUPALL_ASRT") )
        {
            return; // BAILING OUT!!  BAILING OUT!!  BAILING OUT!!  BAILING OUT!!  BAILING OUT!!  BAILING OUT!!  BAILING OUT!!
        }

        OptionToContinue
            ( "CEDRUS_ASSERT",
              message,
              filename,
              line,
              funcname );
    }

    inline void Ced_Fail_Mac
    ( const char* message,
      const char* filename,
      const int line,
      const char* funcname )
    {
        if ( getenv("CEDRUS_SUPALL_ASRT") )
        {
            return; // BAILING OUT!!  BAILING OUT!!  BAILING OUT!!  BAILING OUT!!  BAILING OUT!!  BAILING OUT!!  BAILING OUT!!
        }

        OptionToContinue
            ( "CEDRUS_FAIL",
              message,
              filename,
              line,
              funcname );
    }

    inline void Suppress_All_Assertions()
    {
        char setting[] = "CEDRUS_SUPALL_ASRT=1";
        // should return 0 for SUCCESS:
        /*const int ret =*/ putenv( setting );
    }

    inline void UnSuppress_All_Assertions()
    {
        char negation[] = "CEDRUS_SUPALL_ASRT=";
        // should return 0 for SUCCESS:
        /*const int ret =*/ putenv( negation );
    }

}

/**
   PLEASE READ THIS INTERESTING ITEM ABOUT BAD INTERACTIONS OF IF/ELSE
   STRUCTURES AND PREPROCESSOR MACROS:

    http://stackoverflow.com/questions/154136/do-while-and-if-else-statements-in-c-c-macros
*/

/*
  If you have a Qt QString, then you need to pass it to CEDRUS_ASSERT
  by doing something like this:

       QString message;

       CEDRUS_ASSERT( 1 == 2, message.toUtf8() );

  If you are using std::string, then you will want to pass it in the following
  way:

       std::string message;

       CEDRUS_ASSERT( 1 == 2, message.c_str() );

*/
#ifdef CEDRUS_DISABLE_ASSERT

         // define it as "nothing." they will be "compiled out"
#        define CEDRUS_ASSERT(cond, msg)

#        define CEDRUS_FAIL(msg)

#        define CEDRUS_SUPPRESS_ALL_ASSERTIONS()

#        define CEDRUS_UNSUPPRESS_ALL_ASSERTIONS()


#else // the ELSE is when we _ENABLE_ our assertions

#    if defined(_WIN32)

         // when assertions are enabled on Win:
#        define CEDRUS_ASSERT(cond, msg)         \
             do { if ( ! getenv("CEDRUS_SUPALL_ASRT") ) assert( ( cond ) && ( msg ) );  } while ( 0 )

         // when assertions are enabled on Win:
#        define CEDRUS_FAIL(msg)                 \
             do { if ( ! getenv("CEDRUS_SUPALL_ASRT") ) assert( ! msg );  } while ( 0 )

#        define CEDRUS_SUPPRESS_ALL_ASSERTIONS()   Cedrus::Suppress_All_Assertions()

#        define CEDRUS_UNSUPPRESS_ALL_ASSERTIONS() Cedrus::UnSuppress_All_Assertions()

#    elif defined(__APPLE__)

         // when assertions are enabled on Mac:
#        define CEDRUS_ASSERT(cond, msg)         \
            if ( ( cond ) )                      \
            {                                    \
            }                                    \
            else                                 \
                Cedrus::Ced_Asrt_Mac( msg, __FILE__, __LINE__,  __func__ )

// when assertions are enabled on Mac:
#        define CEDRUS_FAIL(msg)                 \
            Cedrus::Ced_Fail_Mac( msg, __FILE__, __LINE__,  __func__ )

#        define CEDRUS_SUPPRESS_ALL_ASSERTIONS()   Cedrus::Suppress_All_Assertions()

#        define CEDRUS_UNSUPPRESS_ALL_ASSERTIONS() Cedrus::UnSuppress_All_Assertions()

#else
        // TODO
#endif // Win/Apple


#endif // #ifdef CEDRUS_DISABLE_ASSERT





#ifdef NDEBUG_WAS_SET_CEDRUS_HEADER
// Restoring NDEBUG if it was enabled originally
#    define NDEBUG
#endif


#endif // CEDRUS_UTILITY_CODE_CASSERT_WRAPPER

