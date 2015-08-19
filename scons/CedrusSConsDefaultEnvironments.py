#!/usr/bin/env python

from SCons.Script import *
import CedrusSConsHelperFunctions
import MacSettings
import LinuxSettings
import WindowsSettings
import platform

"""
This file is EVEN MORE GENERAL than a top-level SConstruct file.

This file is meant to establish settings that ALL CEDRUS 'SConstruct'
FILES WILL USE... no matter whether it is the SuperLab-4 SConstruct,
or the Licenser SConstruct, or some future thing like a SuperLab-8
SConstruct.

These are like 'company-wide' build flags. They should not assume too
much, because they are general for all projects.
"""

def _get_mac_global_defaults( env ):

    mac = MacSettings.MacSettings( env['WX_VERSION'] )
    env['CXX'] = 'g++-4.0'
    env['CC'] = 'gcc-4.0'

    env['RPATHPREFIX'] = ''
    env['_RPATH'] = ''

    # Note: at one point I changed this to 'AppendUnique', and for some reason
    # that caused the string to appear in the build command-line with DOUBLE-QUOTES AROUND
    # the WHOLE thing!!  Like this:  " -install_name @executable_path/libCedrusThreads.dylib "
    #
    # Then that caused gcc to think that whole string was an input
    # file, and we got the error "No such file or directory"
    env.Append( SHLINKFLAGS = ' -install_name @executable_path/${TARGET.file} ' )

    # believe it or not, we need flags for 'plain old C' code!  it's for sqlite (written in C), in DataViewer
    plain_old_c_flags = [ '-isysroot/Developer/SDKs/MacOSX10.4u.sdk', '-mmacosx-version-min=10.4' ]

    if env['WX_VERSION'] == '2.9':
        plain_old_c_flags = [ '-isysroot/Developer/SDKs/MacOSX10.5.sdk', '-mmacosx-version-min=10.5' ]

    env.AppendUnique(
        CPPPATH = mac.getCommonInclude(),
        CPPDEFINES = mac.getCommonDefines(),
        LIBS = mac.getCommonLibs(),
        LIBPATH = mac.getCommonLibPath(),
        CXXFLAGS = mac.getCommonCxxFlags(),
        LINKFLAGS = mac.getCommonLinkerFlags(),
        CCFLAGS = plain_old_c_flags, # believe it or not, we need flags for 'plain old C' code!  it's for sqlite (written in C), in DataViewer
    )

    return env

def _get_mac_debug_defaults( env ):

    env.Replace(
        BUILD_TYPE_DESCRIPTION = 'MacOS Debug Build',
    )

    mac = MacSettings.MacSettings( env['WX_VERSION'] )

    env.AppendUnique(
        LIBS= mac.getDebugLibraries(),
        LINKFLAGS = mac.getDebugLinkerFlags(),
        CPPDEFINES= mac.getDebugDefines(),
        CXXFLAGS= mac.getDebugCxxFlags(),
        CPPPATH= mac.getDebugIncludes(),
        )

    return env

def _get_mac_release_defaults( env ):

    env.Replace(
        BUILD_TYPE_DESCRIPTION = 'MacOS Release Build',
        )

    mac = MacSettings.MacSettings( env['WX_VERSION'] )

    # the darned '-arch' flags prevent us from doing AppendUnique here
    env.Append(
        LIBS = mac.getReleaseLibraries(),
        LINKFLAGS = mac.getReleaseLinkerFlags(),
        CPPDEFINES = mac.getReleaseDefines(),
        CXXFLAGS = mac.getReleaseCxxFlags(),
        CPPPATH= mac.getReleaseIncludes(),
        CCFLAGS =  # believe it or not, we need flags for 'plain old C' code!  it's for sqlite (written in C), in DataViewer
            [ '-arch', 'i386' ],
        )

    return env

def _get_win_global_defaults( env ):

    win = WindowsSettings.WindowsSettings( env['WX_VERSION'] )

    env.AppendUnique(
        CPPDEFINES = win.getCommonDefines(),
        LIBS = win.getCommonLibs(),
        CPPPATH = win.getCommonInclude(),
        LIBPATH = win.getCommonLibPath(),
        LINKFLAGS = win.getCommonLinkerFlags(),
        CXXFLAGS = win.getCommonCxxFlags(),
        )

    return env

def _get_win_debug_defaults( env ):

    env.Replace(
        BUILD_TYPE_DESCRIPTION = 'Windows Debug Build',
        )

    win = WindowsSettings.WindowsSettings( env['WX_VERSION'] )

    env.AppendUnique(
        CPPDEFINES= win.getDebugDefines(),
        LIBS= win.getDebugLibraries(),
        CPPPATH= win.getDebugIncludes(),
        LINKFLAGS= win.getDebugLinkerFlags(),
        CXXFLAGS= win.getDebugCxxFlags(),
        CCFLAGS=[ '/MDd' ]
        )

    return env

def _get_win_release_defaults( env ):

    env.Replace(
        BUILD_TYPE_DESCRIPTION = 'Windows Release Build',
        )

    win = WindowsSettings.WindowsSettings( env['WX_VERSION'] )

    env.AppendUnique(
        CPPDEFINES= win.getReleaseDefines(),
        LIBS= win.getReleaseLibraries(),
        CPPPATH= win.getReleaseIncludes(),
        LINKFLAGS= win.getReleaseLinkerFlags(),
        CXXFLAGS= win.getReleaseCxxFlags(),
        CCFLAGS=[ '/MD' ]
        )

    return env

def _get_linux_global_defaults( env ):

    env['RPATHPREFIX'] = ''
    env['_RPATH'] = ''

    linux = LinuxSettings.LinuxSettings()

    env.AppendUnique(
        CPPDEFINES = linux.getCommonDefines(),
        LIBS = linux.getCommonLibs(),
        CPPPATH = linux.getCommonInclude(),
        LIBPATH = linux.getCommonLibPath(),
        LINKFLAGS = linux.getCommonLinkerFlags(),
        CXXFLAGS= linux.getCommonCxxFlags(),
        )

    return env

def _get_linux_debug_defaults( env ):

    env.Replace(
        BUILD_TYPE_DESCRIPTION = 'Linux Debug Build',
        )

    linux = LinuxSettings.LinuxSettings()

    env.AppendUnique(
        CPPDEFINES= linux.getDebugDefines(),
        LIBS= linux.getDebugLibraries(),
        CPPPATH= linux.getDebugIncludes(),
        LINKFLAGS= linux.getDebugLinkerFlags(),
        CXXFLAGS= linux.getDebugCxxFlags(),
        )

    return env

def _get_linux_release_defaults( env ):

    env.Replace(
        BUILD_TYPE_DESCRIPTION = 'Linux Release Build',
        )

    linux = LinuxSettings.LinuxSettings()

    env.AppendUnique(
        CPPDEFINES= linux.getReleaseDefines(),
        LIBS= linux.getReleaseLibraries(),
        CPPPATH= linux.getReleaseIncludes(),
        LINKFLAGS= linux.getReleaseLinkerFlags(),
        CXXFLAGS= linux.getReleaseCxxFlags(),
        )

    return env


def GetDefaultSetupForCurrentSystemAndCommandLine( env ):

    build_mode = env.GetOption('build_mode')
    print 'Chosen build mode: ' + str(build_mode)

    if build_mode == 'dbg':

        if sys.platform == 'darwin':
            env = _get_mac_global_defaults( env )
            env = _get_mac_debug_defaults( env )

        elif sys.platform == 'win32':
            env = _get_win_global_defaults( env )
            env = _get_win_debug_defaults( env )

        elif sys.platform == 'linux2':
            env = _get_linux_global_defaults( env )
            env = _get_linux_debug_defaults( env )

        else:
            raise ValueError('Unknown OS.')

    elif build_mode == 'opt':

        if sys.platform == 'darwin':
            env = _get_mac_global_defaults( env )
            env = _get_mac_release_defaults( env )

        elif sys.platform == 'win32':
            env = _get_win_global_defaults( env )
            env = _get_win_release_defaults( env )

        elif sys.platform == 'linux2':
            env = _get_linux_global_defaults( env )
            env = _get_linux_release_defaults( env )

        else:
            raise ValueError('Unknown OS.')

    else:
        raise ValueError('Unknown Build Mode. (we only accept dbg and opt)')

    return env


def PerformCedrusSConsGlobalGeneralStartup( no_longer_used='' ):

    # ------- Handling Problems With Value Expansion  (catching omissions and FAILING EARLY)
    #
    # If a problem occurs when expanding a construction variable, by
    # default it is expanded to '' (a null string), and will not cause
    # scons to fail.  This default behaviour can be changed using the
    # AllowSubstExceptions function. When a problem occurs with a variable
    # expansion it generates an exception, and the AllowSubstExceptions
    # function controls which of these exceptions are actually fatal and
    # which are allowed to occur safely. By default, NameError and
    # IndexError are the two exceptions that are allowed to occur: so
    # instead of causing scons to fail, these are caught, the variable
    # expanded to '' and scons execution continues. To require that all
    # construction variable names exist, and that indexes out of range are
    # not allowed, call AllowSubstExceptions with no extra arguments.

    #  YES!! we want to fail early with errors like this:
    #    NameError `name 'CEDRUS_SCONSCRIPT_PROJECT_NAME' is not defined' trying to evaluate `${CEDRUS_SCONSCRIPT_PROJECT_NAME}'
    # ...   so this is why we call the next line:
    AllowSubstExceptions()

    EnsurePythonVersion( 2, 6 )
    EnsureSConsVersion( 1, 2 )

    SCons.Script.AddOption(
        '--mode',
        dest='build_mode',
        nargs=1,
        type='string',
        action='store',# this is the python optparse default action
        metavar='MODE',
        default='dbg',
        help='build mode')

    # for backwards compatibility since we used to use '--verbose' with swtoolkit
    SCons.Script.AddOption(
        '--verbose',
        dest='something_currently_ignored_this_verbose_thing',
        nargs=0,
        type='string',
        action='store', # this is the python optparse default action
        metavar='IGNORED_VERBOSE_FLAG',
        help='this is currently *ignored*')

    # this is no longer supported. i will remove it when i have time to update hudson/jenkins and other scripts that might contain this
    SCons.Script.AddOption(
        '--msvc-version',
        dest='msvc-version',
        nargs=1,
        type='string',
        action='store',
        default='10.0',
        help='OBSOLETE. UNSUPPORTED. DO NOT USE.') # i just dont want to remove --msvc-version from IDE configs and hudson right now

    SCons.Script.AddOption(
        '--retest',
        dest='retest_flag',
        action='store_true',
        metavar='TRUTH',
        help='force a re-run of all tests')

    if GetOption('retest_flag'):
        print 'Force retest == TRUE'
    else:
        print 'Force retest == FALSE'

    if sys.platform == 'win32':
        # according to SCons documentation: you *must* set MSVC_VERSION in the env constructor
        env = Environment( MSVC_VERSION='10.0' )
        print "Using Visual Studio Version " + env['MSVC_VERSION']

        win_setting_for_vs100 = os.getenv('VS100COMNTOOLS')

        if str(win_setting_for_vs100) == '':
            win_vars_bat_path = 'C:\\Program Files (x86)\\Microsoft Visual Studio 10.0\\VC\\bin\\vcvars32.bat'
            print 'Failed to read the expected environment variable VS100COMNTOOLS.'
        else:
            win_vars_bat_path = str(win_setting_for_vs100) + '\\..\\..\\VC\\bin\\vcvars32.bat'

        # now it looks like both win7 *and* the vista machine are fixed if we use MSVC_USE_SCRIPT
        env = Environment(
            MSVC_VERSION='10.0',
            MSVC_USE_SCRIPT=win_vars_bat_path
            )

        env['WINDOWS_INSERT_MANIFEST'] = True

        env['PDB'] = '${TARGET.base}.pdb'

        env['LINKCOM'] = [env['LINKCOM'], 'mt.exe -nologo -manifest ${TARGET}.manifest -outputresource:$TARGET;1']
        env['SHLINKCOM'] = [env['SHLINKCOM'], 'mt.exe -nologo -manifest ${TARGET}.manifest -outputresource:$TARGET;2']

    else:
        env = Environment()

    env.SetOption('num_jobs', int(os.getenv('NUM_CPU',4))  )
    print "Running with -j", env.GetOption('num_jobs')

    #-------------------------------------------------------------------------------------
    #------ BEGIN SECTION:   ** so-called "GoFastButton" **     --------------------------

    # For more info on the "GoFastButton", see http://www.scons.org/wiki/GoFastButton

    # If anything in this section causes PROBLEMS, then we can REMOVE THESE THINGS.
    # Settings from the "GoFastButton" wiki are OPTIONAL (completely non-essential),
    # and they sometimes do have caveats.

    # 'MD5-timestamp' means that if the timestamp matches, don't bother re-MD5ing the file.
    # I had thought that this was now the default, but it must not be because I got
    # a *HUGE* speedup on my XP machine by adding this
    env.Decider('MD5-timestamp')

    # like the Decider setting, this is also from http://www.scons.org/wiki/GoFastButton
    env.SetOption('max_drift', 900) # set to 15 min. otherwise SCons picks 2 days

    #------ END   SECTION:   ** so-called "GoFastButton" **     --------------------------
    #-------------------------------------------------------------------------------------


    #-------------------------------------------------------------------------------------
    #------ BEGIN SECTION:   ** CXXCOMSTR **     -----------------------------------------

    # We are explicity initializing a few constructions variables, because
    # otherwise we will get errors due to the fact that we called
    # 'AllowSubstExceptions()' earlier.  The errors would look like:
    #          NameError `LINKCOMSTR' trying to evaluate `$LINKCOMSTR'

    # CXXCOMSTR: The string displayed when a C++ source file is compiled to a
    # (static) object file. If this is not set, then $CXXCOM (the command
    # line) is displayed.
    env.Append( CXXCOMSTR = '')

    # Same as CXXCOMSTR, only for specifically compiling a shared object
    env.Append( SHCXXCOMSTR = '')
    # Same as CXXCOMSTR, only when linking a program to a shlib
    env.Append( SHLINKCOMSTR = '')
    # Same as CXXCOMSTR, only when objects are linked into an exe
    env.Append( LINKCOMSTR = '' )

    env.Append( MSVC_BATCH = '' )
    env.Append( PCHCOMSTR = '' )
    env.Append( RCCOMSTR = '' )

    env.Append( ARCOMSTR = '' )      # needed for static libs on windows
    env.Append( RANLIBCOMSTR = '' )  # needed for static libs on windows

    env.Append( CCCOMSTR = '' )      # needed for 'sqlite3.c' in DataViewer

    env.Append( PCH = '' )  # we need this here in case any projects DON'T want a PCH on windows. (those that do override this)

    env.Append( SHLIBVERSION = '' )

    #------ END SECTION:     ** CXXCOMSTR **     -----------------------------------------
    #-------------------------------------------------------------------------------------


    #-------------------------------------------------------------------------------------
    #------ BEGIN SECTION:   ** OBJSUFFIX **     -----------------------------------------

    #     The reason for setting our OBJSUFFIX to a suffix that VARIES
    #     from one project to the next is very simple: this allows you to
    #     take a file like 'UtilFuncs.cpp' and build that file inside of
    #     several different subordinate SConscript files without getting
    #     the error:
    #
    #           Two environments with different actions were specified for
    #           the same target: UtilFuncs.os


    # warning: don't do 'env.Append' on the next line, or file names will
    # end up like: wxLogHelperFunctions.os_PROJECT_.os (with '.os' twice)
    env.Replace(
        # TODO - FIXME - if I can figure out *why* some projects use
        # OBJSUFFIX while other projects use SHOBJSUFFIX, then I can
        # get rid of the '.object' thing.  For now, this is the only
        # way i can GUARANTEE that the 'Alias' call in
        # _common_cedrus_build_code will work for all cpp files.
        OBJSUFFIX = '_${CEDRUS_SCONSCRIPT_PROJECT_NAME}_' + '.object', #env['OBJSUFFIX'],
        SHOBJSUFFIX = '_${CEDRUS_SCONSCRIPT_PROJECT_NAME}_' + '.object', #env['SHOBJSUFFIX'],
        )

    #------ END SECTION:     ** OBJSUFFIX **     -----------------------------------------
    #-------------------------------------------------------------------------------------

    env[ 'BUILD_TYPE' ] = GetOption('build_mode')

    # Specify defaults for variables. Note that BUILD_TYPE *must* be set prior to this line!!!
    env.SetDefault(
        DESTINATION_ROOT= os.getcwd() + '/scons-out',
        TARGET_ROOT='$DESTINATION_ROOT/$BUILD_TYPE',
        OBJ_ROOT='$TARGET_ROOT/obj',
        STAGING_DIR='$TARGET_ROOT/staging',
        )

    if GetOption('retest_flag'):
        print 'Removing the test output directory to force tests to run again.'
        # You can also execute an action *immediately* (meaning at the time
        # the SConscript file is *read*) by using the Execute function. For
        # example, if we need to make sure that a directory exists before we
        # build any targets, Execute(Mkdir('/tmp/my_temp_directory'))
        Execute(Delete(Dir(env.subst('$STAGING_DIR/../tests'))))

    return env


def _cedrus_declare_shared_pch(
    env,
    pch_name,
    pch_cpp_location,
    pch_stop,
    alias_name
    ):
    """
    WARNING: If you make changes to the NAMING CONVENTION of the
    "PCH.obj" and "PCH.pch" files, then you MUST ALSO MAKE UPDATES to
    any projects that *override* these settings for 'env['PCH']' and
    similar.  As of the time of this writing (Sept 2011), that *only*
    includes updating SConscript.pyLSClient
    """
    if sys.platform == 'win32':
        # You might be surprised that we don't use CPPFLAGS for anything.
        # You are then probably confusing CPPFLAGS with CXXFLAGS. We
        # indeed do make use of CXXFLAGS.  We do not need CPPFLAGS,
        # however, because it is for the C **preprocessor** options, and
        # we do not send any special flags to the preprocessor.
        env.AppendUnique( CPPFLAGS = '') # quiets the warning when using AllowSubstExceptions()

        if env['BUILD_TYPE'] == 'opt':
            pch_name += '_opt_'

        env['PCH'] = env.PCH(pch_name+'PCH.pch', pch_cpp_location )[0]
        env['PCHSTOP'] = pch_stop
        env.AppendUnique(
            CXXFLAGS=str('/FI' + pch_stop),
            LINKFLAGS=str(pch_name+'PCH.obj')
            )

        env.Alias( alias_name, env['PCH'] )

def DeclareBuildOfGenericCommonPCH( env ):

    _cedrus_declare_shared_pch(
        env,
        'CedrusGeneralCommonPrecompilation_', #pch_name
        '$OBJ_ROOT/Common/src/precompiled.cpp', #pch_cpp_location,
        'CedrusPCH.h',
        'CedrusPCH'
        )

def DeclareBuildOfGenericSuperLabPCH( env ):

    _cedrus_declare_shared_pch(
        env,
        'CedrusGeneralSuperLabPrecompilation_', #pch_name
        '$OBJ_ROOT/SuperLabProject/src/SuperLab/precompiled.cpp', #pch_cpp_location,
        'superlab3.h',
        'SuperLabPCH'
        )

def UndoSuperLabPCH( env ):

    pch_stop = 'superlab3.h'
    pch_name = 'CedrusGeneralSuperLabPrecompilation_'

    if env['BUILD_TYPE'] == 'opt':
        pch_name += '_opt_'

    CedrusSConsHelperFunctions.FromSwtoolkitFilterOut( env,
                                                       CXXFLAGS=[str('/FI' + pch_stop)],
                                                       LINKFLAGS=[str(pch_name+'PCH.obj')] )

def DeclareBuildOfGenericCommonPCH_w_Qt( env ):

    UndoSuperLabPCH( env )

    _cedrus_declare_shared_pch(
        env,
        'CedrusGeneralCommonPrecompilationQt_', #pch_name
        '$OBJ_ROOT/Common/src/precompiled_qt.cpp', #pch_cpp_location,
        'CedrusPCH_w_Qt.h',
        'CedrusPCH_w_Qt'
        )

