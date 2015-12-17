#!/usr/bin/env python

from SCons.Script import *
import gMock
import os
import sys
import time
import smtplib
import platform

#------------------------------------------------------------------------------

# This function originally came from $SWTOOLKIT/site_scons/site_tools/environment_tools.py
def FromSwtoolkitFilterOut(env, **kw):
    """Removes values from existing construction variables in an Environment.

    The values to remove should be a list.  For example:

    FromSwtoolkitFilterOut(
        env,
        CPPDEFINES=['REMOVE_ME', 'ME_TOO'],
        LINKFLAGS=['MUST_GO_AWAY', 'THIS_TOO']
        )

    Args:
      env: Environment to alter.
      kw: (Any other named arguments are values to remove).
    """

    kw = SCons.Environment.copy_non_reserved_keywords(kw)
    for key, val in kw.items():
        envval = env.get(key, None)

        # Note from Kelly: I cannot figure out why, but envval ended
        # up holding some sort of DEEP reference to the 'global-est'
        # environment settings (after the call above to env.get).
        # Then, lower down in this function, where we call
        # 'remove(vremove)', the values were getting removed for ALL
        # FUTURE SCONSCRIPTS that follow whichever SConscript called
        # this function currently. That is bad!!  The whole point of
        # passing in the cloned environment to this function is so
        # that we only filter the CURRENT environment. Making a *copy*
        # of the list solves this problem.
        local_val = list( envval ) # Again: not sure why, but it's necessary

        if envval is None:
            # No existing variable in the environment, so nothing to delete.
            continue

        for vremove in val:
            # Use while not if, so we can handle duplicates.
            while vremove in local_val:
                local_val.remove(vremove)

        env[key] = local_val

        # TODO: SCons.Environment.Append() has much more logic to deal with various
        # types of values.  We should handle all those cases in here too.  (If
        # variable is a dict, etc.)

#------------------------------------------------------------------------------

def NowIsDuringBusinessHoursWhenSomeoneCanReactToSomeHungTest():

    is_business_day = False
    during_work_hours = False

    # tm_wday ranges from 0-6. 0 is monday
    if time.localtime().tm_wday < 5:
        is_business_day = True

    if time.localtime().tm_hour >= 7 and time.localtime().tm_hour < 19:
        during_work_hours = True

    result = (is_business_day and during_work_hours)

    if result == True:
        print 'The Cedrus Python SCons helper function determined that this build is running *DURING* business hours.'
    else:
        print 'The Cedrus Python SCons helper function found that this build is _NOT_ happening during normal work hours.'

    return result


def _make_one_lambda_for_shared_lib():
    return lambda e, name, input : e.SharedLibrary( name, input )

def _make_one_lambda_for_simple_program():
    return lambda e, name, input : e.Program( name, input )

def _make_one_lambda_for_static_lib():
    return lambda e, name, input : e.StaticLibrary( name, input )

def _common_cedrus_build_code(
    env,
    pch_name,
    project_target_name,
    inputs,
    defines,
    cpppath,
    cxxflags,
    frameworks,
    libs,
    libpath,
    linkflags,
    lambda_functor,
    flag_to_enable_direct_staging=False
):
    # if we ever have a Cedrus project that *NEEDS* to actually set
    # FRAMEWORKSFLAGS or CPPFLAGS to some non-empty value, then we
    # should consider making that another argument to the
    # 'DeclareSConsSharedLibraryBuild' function
    #
    # The reason we must initialize FRAMEWORKSFLAGS and CPPFLAGS is
    # that we want to use a special call to 'AllowSubstExceptions()'
    # in order to make sure we FAIL EARLY if scons tries to expand any
    # uninitialized construction variable. These two variables seem to
    # always be uninitialized in our build, so I am initializing them
    # to quiet the failures that would be specific just to these two
    # variables.
    env.AppendUnique( FRAMEWORKSFLAGS = '' )
    # You might be surprised that we don't use CPPFLAGS for anything.
    # You are then probably confusing CPPFLAGS with CXXFLAGS. We
    # indeed do make use of CXXFLAGS.  We do not need CPPFLAGS,
    # however, because it is for the C **preprocessor** options, and
    # we do not send any special flags to the preprocessor.
    env.AppendUnique( CPPFLAGS = '')

    env['CEDRUS_SCONSCRIPT_PROJECT_NAME'] = project_target_name

    # we want to make a short alias for each source file, so we can build one file at a time if necessary
    for each_input in inputs:

        # rsplit starts splitting the string from RIGHT to left
        path_portions = str(each_input).rsplit( '/', 1 ) # the one means only split ONCE
        if len(path_portions) > 0:
            input_file_name = path_portions[len(path_portions)-1]
            file_base_name_no_extension = input_file_name.rsplit( '.', 1 )

            if len(file_base_name_no_extension) >= 0:
                compiled_output_for_sourcefile = file_base_name_no_extension[0] + env['OBJSUFFIX']
                # Now we know the name of the gcc output for this
                # file. So alias that to the simple 'sourcefile.cpp'
                # name.  NOTE: if a source file is in MORE THAN ONE
                # sub-project, then that is okay!  What will happen is
                # actually really nice.  If you build, for example:
                # './build.sh wxLogHelperFunctions.cpp' then what will
                # happen is that SCons will build ALL OF THE FOLLOWING:
                #     wxLogHelperFunctions_CedrusThreads_.object
                #     wxLogHelperFunctions_LSClient_.object
                #     wxLogHelperFunctions_AdminApp_.object
                #     ... etc ..
                #
                # Therefore, if you are making changes to just one
                # file, and you want to compile only that file to
                # discover whether you broken anything or not, then
                # using './build.sh FILENAME.cpp' is perfect. You will
                # discover whether your changes fail to build in ANY
                # PROJECT THAT DEPENDS ON THAT FILE (since different
                # projects might build the same file using different
                # DEFINE(s) and flags).
                env.Alias( input_file_name, path_portions[0] + '/' + compiled_output_for_sourcefile )

    # as of March 1, 2011, the pch stuff moved to CedrusSConsDefaultEnvironments.DeclareBuildOfGenericCommonPCH

    libpath.append( str( env.subst('$STAGING_DIR') ) )

    env.AppendUnique(
        CPPDEFINES= defines,
        CPPPATH = cpppath,
        CXXFLAGS = cxxflags,
        FRAMEWORKS = frameworks,
        LIBS = libs,
        LIBPATH = libpath,
        LINKFLAGS = linkflags,
        )

    # Note: 'flag_to_enable_direct_staging' began as an experiment. At
    # least for starters, we are only setting this to TRUE in the case
    # of SHARED LIBRARIES.  This was done because on Windows, the unit
    # test EXE programs were (for unknown reasons) not getting
    # 'registered' in SCons so that SCons could know that these EXE
    # files need our DLL files to be PRESENT in 'STAGING_DIR' before
    # we can EXECUTE the test.  So, due to that problem, SCons was
    # attempting to launch, say, "TestLSClient.exe" before
    # LSCommon.dll had been copied to the staging dir via the
    # 'env.Install' directive (below).  To get around that problem, I
    # am now building the DLL libraries directly into the STAGING_DIR
    # instead of building them and then later using 'env.Install' as a
    # separate step. At some point we may just use the 'direct'
    # technique for EVERYTHING (not just dlls).
    if flag_to_enable_direct_staging == True:
        directly_staged_target = os.path.join(os.path.abspath(str( env.subst('$STAGING_DIR') )), project_target_name)
        built_final_compiled_product = lambda_functor( env, directly_staged_target, inputs )
        stage_it = built_final_compiled_product
    else:
        built_final_compiled_product = lambda_functor( env, project_target_name, inputs )
        stage_it = env.Install( env.subst('$STAGING_DIR'), built_final_compiled_product )

    # for now i only run dsymutil in a debug build. (i don't want dSYM bundles polluting the installer, and have not refined for that yet)
    if sys.platform == 'darwin' and env['BUILD_TYPE'] == 'dbg':
        def dsymutilFunc( env, source, target ):
            os.system( "dsymutil " + target[0].get_abspath() )

        env.AddPostAction( stage_it, dsymutilFunc )


    env.Alias( str(project_target_name), stage_it )

    # this line means that building ANY SINGLE project (whether it be
    # a test, a GUI app, a python module, a library, etc) *ALWAYS*
    # triggers the complete population of the staging area with our
    # third-party dependencies present.
    env.Depends( stage_it, env['CEDRUS_COMPLETE_THIRD_PARTY_STAGING'] )

    return stage_it

def DeclareSConsSharedLibraryBuildWithPCH(
    env,
    pch_name,
    project_target_name,
    inputs,
    defines,
    cpppath,
    cxxflags,
    frameworks,
    libs,
    libpath,
    linkflags,
):
    return _common_cedrus_build_code(
        env,
        pch_name,
        project_target_name,
        inputs,
        defines,
        cpppath,
        cxxflags,
        frameworks,
        libs,
        libpath,
        linkflags,
        _make_one_lambda_for_shared_lib(),
        True
        )

def DeclareSConsSharedLibraryBuild(
    env,
    project_target_name,
    inputs,
    defines,
    cpppath,
    cxxflags,
    frameworks,
    libs,
    libpath,
    linkflags
):
    return _common_cedrus_build_code(
        env,
        project_target_name, # this is the pch name. use same as project_target_name
        project_target_name,
        inputs,
        defines,
        cpppath,
        cxxflags,
        frameworks,
        libs,
        libpath,
        linkflags,
        _make_one_lambda_for_shared_lib(),
        True
        )

def DeclareSConsStaticLibraryBuild(
    env,
    project_target_name,
    inputs,
    defines,
    cpppath,
    cxxflags,
    frameworks,
    libs,
    libpath,
    linkflags
):
    return _common_cedrus_build_code(
        env,
        project_target_name, # this is the pch name. use same as project_target_name
        project_target_name,
        inputs,
        defines,
        cpppath,
        cxxflags,
        frameworks,
        libs,
        libpath,
        linkflags,
        _make_one_lambda_for_static_lib(),
        True
        )

def DeclareSConsSimpleProgramBuild(
    env,
    project_target_name,
    inputs,
    defines,
    cpppath,
    cxxflags,
    frameworks,
    libs,
    libpath,
    linkflags
):
    return _common_cedrus_build_code(
        env,
        project_target_name, # this is the pch name. use same as project_target_name
        project_target_name,
        inputs,
        defines,
        cpppath,
        cxxflags,
        frameworks,
        libs,
        libpath,
        linkflags,
        _make_one_lambda_for_simple_program()
        )

def DeclareSConsGUIAppProgramBuild(
    env,
    project_target_name,
    inputs,
    defines,
    cpppath,
    cxxflags,
    frameworks,
    libs,
    libpath,
    linkflags,
    app_resources
):

    if sys.platform == 'win32':
        linkflags += [ '/SUBSYSTEM:WINDOWS' ] # means that this is *not* a console app

    installed_executable = DeclareSConsSimpleProgramBuild(
        env,
        project_target_name,
        inputs,
        defines,
        cpppath,
        cxxflags,
        frameworks,
        libs,
        libpath,
        linkflags
        )

    total_nodes_for_app = installed_executable

    if sys.platform == 'darwin':

        mac_app_bundle_contents_dir = env.subst('$STAGING_DIR') + '/' + project_target_name + '.app/Contents/'
        total_nodes_for_app += env.Install( mac_app_bundle_contents_dir + 'MacOS/' , installed_executable )

        total_nodes_for_app += env.Command(
            mac_app_bundle_contents_dir + 'Info.plist',
            './' + project_target_name +'-Info.plist',
            [Copy('$TARGET', '$SOURCE'),
             Chmod('$TARGET', 0644)]
            )

        for rsrc in app_resources:
            total_nodes_for_app += env.Install( mac_app_bundle_contents_dir + 'Resources/', rsrc )

        total_nodes_for_app += env.Install( mac_app_bundle_contents_dir , './PkgInfo' )

        libs_to_copy = set( env['LIBS'] )
        libs_to_copy = libs_to_copy.difference( set( env[ 'CEDRUS_NON_COPYABLE_LIBS' ] ) )

        # env['SHLIBPREFIX'] did not work here, for some reason. but
        # this portion is Mac-only anyway
        for single_lib in libs_to_copy:
            total_nodes_for_app += env.Install(
                mac_app_bundle_contents_dir + 'MacOS/',
                env.subst('$STAGING_DIR') + '/lib' + str(single_lib) + env['SHLIBSUFFIX']
                )

    elif sys.platform == 'win32':
        for rsrc in app_resources:
            total_nodes_for_app += env.Install( env.subst('$STAGING_DIR'), rsrc )

    # this next Alias line makes it so that running (for example)
    # "./build.sh AdminApp" will go ahead and build both the bare
    # executable *and* "AdminApp.app"
    env.Alias( str(project_target_name), total_nodes_for_app )

    return total_nodes_for_app


def _make_a_mac_app_plist(
    app_name,
    info_string,
    version_string,
    min_macos_version,
    target,
    source,
    env
    ):

    os.system( 'cp "' + source[0].abspath + '" "' + target[0].abspath + '"' )

    target_for_mac_command = str( target[0].abspath.rsplit( '.', 1 )[0] )

    start_of_command = 'defaults write "' + target_for_mac_command + '" '

    os.system( start_of_command + ' CFBundleShortVersionString ' + '"' + version_string + '"' )
    os.system( start_of_command + ' CFBundleVersion '            + '"' + version_string + '"' )
    os.system( start_of_command + ' CFBundleGetInfoString '      + '"' + info_string + '"' )
    os.system( start_of_command + ' CFBundleExecutable '         + '"' + app_name + '"' )
    os.system( start_of_command + ' LSMinimumSystemVersion '     + '"' + min_macos_version + '"' )

def _make_one_lambda_for_plist( app_name, info_string, version_string, min_macos_version ):
    return lambda target, source, env : _make_a_mac_app_plist( app_name, info_string, version_string, min_macos_version, target, source, env  )

def DeclareSConsComplexGUIAppProgramBuild(
    env,
    project_target_name, # this will name the exe (for windows)
    app_name, # this will name the app bundle name (for mac)
    plist_file,
    app_version_string,
    app_copyright_and_info_string,
    app_min_macos_version,
    inputs,
    defines,
    cpppath,
    cxxflags,
    frameworks,
    libs,
    libpath,
    linkflags,
    app_resources,  # mac:  Contents/Resources/
    shared_support_content, # mac:  Contents/SharedSupport/
    frameworks_content, # mac:  Contents/Frameworks/
):
    if sys.platform == 'win32':
        linkflags += [ '/SUBSYSTEM:WINDOWS' ] # means that this is *not* a console app

    installed_executable = DeclareSConsSimpleProgramBuild(
        env,
        project_target_name,
        inputs,
        defines,
        cpppath,
        cxxflags,
        frameworks,
        libs,
        libpath,
        linkflags
        )

    total_nodes_for_app = installed_executable

    if sys.platform == 'darwin':

        mac_app_bundle_contents_dir = env.subst('$STAGING_DIR') + '/' + app_name + '.app/Contents/'
        total_nodes_for_app += env.InstallAs( mac_app_bundle_contents_dir + 'MacOS/' + app_name , installed_executable )
        total_nodes_for_app += env.Command(
            mac_app_bundle_contents_dir + 'Info.plist',
            './' + plist_file,
            [_make_one_lambda_for_plist(
                app_name,
                app_copyright_and_info_string,
                app_version_string,
                app_min_macos_version),
             Chmod('$TARGET', 0644)]
            )

        for rsrc in app_resources:
            total_nodes_for_app += env.Install( mac_app_bundle_contents_dir + 'Resources/', rsrc )

        for support in shared_support_content:
            total_nodes_for_app += env.Install( mac_app_bundle_contents_dir + 'SharedSupport/', shared_support_content )

        for frmwork in frameworks_content:
            total_nodes_for_app += env.Install( mac_app_bundle_contents_dir + 'Frameworks/', frmwork )

        total_nodes_for_app += env.Install( mac_app_bundle_contents_dir , './PkgInfo' )

        libs_to_copy = set( env['LIBS'] )
        libs_to_copy = libs_to_copy.difference( set( env[ 'CEDRUS_NON_COPYABLE_LIBS' ] ) )

        # env['SHLIBPREFIX'] did not work here, for some reason. but
        # this portion is Mac-only anyway
        for single_lib in libs_to_copy:
            total_nodes_for_app += env.Install(
                mac_app_bundle_contents_dir + 'MacOS/',
                env.subst('$STAGING_DIR') + '/lib' + str(single_lib) + env['SHLIBSUFFIX']
                )

    elif sys.platform == 'win32':
        for rsrc in app_resources:
            total_nodes_for_app += env.Install( env.subst('$STAGING_DIR'), rsrc )

    # this next Alias line makes it so that running (for example)
    # "./build.sh AdminApp" will go ahead and build both the bare
    # executable *and* "AdminApp.app"
    env.Alias( str(project_target_name), total_nodes_for_app )

    return total_nodes_for_app


def DeclareSConsProgramWithRunnableGoogleTests(
    env,
    project_target_name,
    inputs,
    defines,
    cpppath,
    cxxflags,
    frameworks,
    libs,
    libpath,
    linkflags,
    skip_test_execution = False
):
    if platform.mac_ver()[0].startswith('10.7'):
        return

    cpppath.append( str( os.getenv('GMOCK','')+'/include' ) )
    cpppath.append( str( os.getenv('GTEST','')+'/include' ) )

    if env['PLATFORM'] == 'win32':
        FromSwtoolkitFilterOut( env, CPPDEFINES = ['_WINDOWS'] )
        defines += [ '_CONSOLE' ]

    gMock.need_gmock(env)

    installed_executable = DeclareSConsSimpleProgramBuild(
        env,
        project_target_name,
        inputs,
        defines,
        cpppath,
        cxxflags,
        frameworks,
        libs,
        libpath,
        linkflags
        )

    if False == skip_test_execution:

        test_results = env.subst('$STAGING_DIR/../tests/') + project_target_name + '.xml'

        command_line_string = ''

        if sys.platform == 'linux2':
            # this assumes that the test executable was installed to STAGING !!
            command_line_string += ' export LD_LIBRARY_PATH=' + env.subst('$STAGING_DIR') + '; '

        command_line_string += ' "' + str(installed_executable[0].abspath) + '"' + ' --gtest_output=xml:' + '"' + test_results + '"'
        #print command_line_string

        run_the_test = env.Command(
            test_results,  # the target
            installed_executable,
            command_line_string
            )

        # this next Alias line makes it so that running (for example)
        # "./build.sh TestLSCommon" will go ahead and *run* the test
        # executable after it gets built
        env.Alias( str(project_target_name), run_the_test )

    return installed_executable


def _ConfigureCedrusVersionNumbersForProjectsThatHaveDebs(
    env,
    list_of_version_files,
    ):

    # determine package versions for debian packages
    def determineVersion(packageName):
        for one_file in list_of_version_files:
            versionFile = open(one_file,'r')
            for line in versionFile:
                app = line.rstrip().replace(' ','').split(':')
                if app[0] == packageName:
                    return app[1]

    version_summary_strings_in_deb_control_style = []
    version_dictionary_by_deb_name = {}

    ADMIN_SERVER_VERSION = determineVersion('adminserver')
    CEDRUS_NETWORKING_VERSION = determineVersion('libcedrusnetworking')
    CEDRUS_STREAMS_VERSION = determineVersion('libcedrusstreams')
    CEDRUS_THREADS_VERSION = determineVersion('libcedrusthreads')
    DATABASE_LAYER_VERSION = determineVersion('libdatabaselayer')
    LS_CLIENT_VERSION = determineVersion('liblsclient')
    LS_COMMON_VERSION = determineVersion('liblscommon')
    LS_COMMON_ADMIN_VERSION = determineVersion('liblscommonadmin')
    PY_LS_CLIENT_VERSION = determineVersion('pylsclient')
    TINY_SERVER_VERSION = determineVersion('tinylicenseserverdaemon')


    if ADMIN_SERVER_VERSION:
        version_string = 'adminserver (>= ' + ADMIN_SERVER_VERSION + ')'
        version_summary_strings_in_deb_control_style += [ version_string ]
        version_dictionary_by_deb_name[ 'adminserver' ] = ADMIN_SERVER_VERSION

    if CEDRUS_NETWORKING_VERSION:
        version_string = 'libcedrusnetworking (>= ' + CEDRUS_NETWORKING_VERSION + ')'
        version_summary_strings_in_deb_control_style += [ version_string ]
        version_dictionary_by_deb_name[ 'libcedrusnetworking' ] = CEDRUS_NETWORKING_VERSION

    if CEDRUS_STREAMS_VERSION:
        version_string = 'libcedrusstreams (>= ' + CEDRUS_STREAMS_VERSION + ')'
        version_summary_strings_in_deb_control_style += [ version_string ]
        version_dictionary_by_deb_name[ 'libcedrusstreams' ] = CEDRUS_STREAMS_VERSION

    if CEDRUS_THREADS_VERSION:
        version_string = 'libcedrusthreads (>= ' + CEDRUS_THREADS_VERSION + ')'
        version_summary_strings_in_deb_control_style += [ version_string ]
        version_dictionary_by_deb_name[ 'libcedrusthreads' ] = CEDRUS_THREADS_VERSION

    if DATABASE_LAYER_VERSION:
        version_string = 'libdatabaselayer (>= ' + DATABASE_LAYER_VERSION + ')'
        version_summary_strings_in_deb_control_style += [ version_string ]
        version_dictionary_by_deb_name[ 'libdatabaselayer' ] = DATABASE_LAYER_VERSION

    if LS_CLIENT_VERSION:
        version_string = 'liblsclient (>= ' + LS_CLIENT_VERSION + ')'
        version_summary_strings_in_deb_control_style += [ version_string ]
        version_dictionary_by_deb_name[ 'liblsclient' ] = LS_CLIENT_VERSION

    if LS_COMMON_VERSION:
        version_string = 'liblscommon (>= ' + LS_COMMON_VERSION + ')'
        version_summary_strings_in_deb_control_style += [ version_string ]
        version_dictionary_by_deb_name[ 'liblscommon' ] = LS_COMMON_VERSION

    if LS_COMMON_ADMIN_VERSION:
        version_string = 'liblscommonadmin (>= ' + LS_COMMON_ADMIN_VERSION + ')'
        version_summary_strings_in_deb_control_style += [ version_string ]
        version_dictionary_by_deb_name[ 'liblscommonadmin' ] = LS_COMMON_ADMIN_VERSION

    if PY_LS_CLIENT_VERSION:
        version_string = 'pylsclient (>= ' + PY_LS_CLIENT_VERSION + ')'
        version_summary_strings_in_deb_control_style += [ version_string ]
        version_dictionary_by_deb_name[ 'pylsclient' ] = PY_LS_CLIENT_VERSION

    if TINY_SERVER_VERSION:
        version_string = 'tinylicenseserverdaemon (>= ' + TINY_SERVER_VERSION + ')'
        version_summary_strings_in_deb_control_style += [ version_string ]
        version_dictionary_by_deb_name[ 'tinylicenseserverdaemon' ] = TINY_SERVER_VERSION

    return [ version_summary_strings_in_deb_control_style, version_dictionary_by_deb_name ]


def _convert_version_list_into_comma_string(
    version_list_full,
    current_deb_name
    ):

    version_list = []

    for one_deb in version_list_full:
        if not (one_deb.find( current_deb_name ) == 0):
            version_list += [ one_deb ]

    result = ''

    if len(version_list) > 0:
        result = version_list[0]

    for i in range(1, len(version_list)):
        result += ', '
        result += version_list[i]

    return result


def DeclareDebPackage(
    env,
    project_target_name,
    prefix_prepended_to_name_for_binary,
    suffix_appended_to_name_for_binary,
    staged_binary,
    final_install_destination_folder,
    folder_with_deb_package_scripts,
    folder_with_init_d_scripts,
    deb_name,
    deb_desc,
    extra_dpkg_depends_statements=[]
):
    """
    NOTE: it is *intentional* that as much of the deb-related code as
    possible *will* be run on EVERY PLATFORM (not just on the linux
    platform).  This might seem a little 'wasteful' on non-linux
    platforms, because none of the files that are produced will be
    useful, and the final deb file is not actually made.  However,
    this is really only a *MINISCULE* overhead on the non-linux
    builds. And there is a benefit: you can find out quite early
    whether some change you are making to a SConscript might break
    anything in the linux build.

    Therefore, the BENEFIT of running these commands on ALL PLATFORMS
    more than compensates for the tiny 'wasteful' overhead of a few
    extra ('useless') things running on Mac and Windows builds.
    """

    DEBARCH = 'amd64'
    DEBMAINT = 'Cedrus Corp <developers@cedrus.com>'

    CONTROL_TEMPLATE = """
Package: %s
Priority: extra
Section: misc
Installed-Size: %s
Maintainer: %s
Architecture: %s
Version: %s
Depends: %s
Description: %s

"""

    deb_depends = ['boost-cedrus (>= 1.42)']

    if env['BUILD_TYPE'] == 'dbg':
        deb_depends += ['wxwidgets-cedrus-debug (>= 2.8.4)']
    else:
        deb_depends += ['wxwidgets-cedrus (>= 2.8.4)']

    deb_depends += extra_dpkg_depends_statements

    versioning_info_struct = _ConfigureCedrusVersionNumbersForProjectsThatHaveDebs(
        env,
        env['CEDRUS_DEBS_PACKAGE_VERSIONS_FILES']
        )

    deb_depends += versioning_info_struct[ 0 ]

    deb_version = versioning_info_struct[ 1 ][ deb_name ]

    # outer folder is something like:  scons-out/dbg/staging/liblscommon/  (all lower case)
    outer_folder_for_this_deb = os.path.join( env.subst('$STAGING_DIR/dpkg_debs/'), deb_name )

    #-------------------------------------------------------------------------------------------------------------------
    #------ BEGIN SECTION:   ** actual end-user binaries that we ultimately want installed on Ubuntu **     -------------

    # although this 'inner_deb_staged_folder' is still underneath the
    # 'scons-out' folder, the inner folder represents the LINUX PATH
    # where things ultimately are placed by apt-get. This path will
    # look like: scons-out/dbg/staging/liblscommon/usr/lib/
    # (Note how the path ends with 'usr/lib/')
    inner_deb_staged_folder = os.path.join(outer_folder_for_this_deb, final_install_destination_folder)

    # this will be something like: scons-out/dbg/staging/liblscommon/usr/lib//libLSCommon.so
    binary_placed_for_deb = str( inner_deb_staged_folder ) + '/' + str(
        prefix_prepended_to_name_for_binary + project_target_name + suffix_appended_to_name_for_binary )

    # real, actual, 'for the user' binaries consist of the main object and any init.d scripts
    binaries_for_deb_install = []
    binaries_for_deb_install += env.Command( binary_placed_for_deb, staged_binary, SCons.Script.Copy('$TARGET', '$SOURCE') )

    if folder_with_init_d_scripts != '':
        for root, dirs, files in os.walk(folder_with_init_d_scripts):
            for f in files:
                fullpath = os.path.join(root, f)
                script_placed_for_deb = str( outer_folder_for_this_deb ) + '/etc/init.d/' + str( f )
                binaries_for_deb_install += env.Command( script_placed_for_deb, fullpath,  SCons.Script.Copy('$TARGET', '$SOURCE') )

    #------ END   SECTION:   ** actual end-user binaries that we ultimately want installed on Ubuntu **     -------------
    #-------------------------------------------------------------------------------------------------------------------

    #-------------------------------------------------------------------------------------------------
    #------ BEGIN SECTION:   ** house-keeping/bureaucratic files required by dpkg **     -------------

    DEBDIR = os.path.join(outer_folder_for_this_deb, "DEBIAN") # scons-out/opt/obj/tinylicenseserverdaemon/DEBIAN/
    deb_control_file_abs_path = os.path.join(DEBDIR, "control")

    # going through postinst and postrm
    for root, dirs, files in os.walk(folder_with_deb_package_scripts):
        for f in files:
            fullpath = os.path.join(root, f)
            script_placed_for_deb = str( DEBDIR ) + '/' + str( f )
            env.Command( script_placed_for_deb, fullpath,  SCons.Script.Copy('$TARGET', '$SOURCE') )

    def make_deb_control_file(target=None, source=None, env=None):
        files_to_measure_for_deb_install = source
        installed_size = 0
        for i in files_to_measure_for_deb_install:
            installed_size += os.stat(str(i))[6]

        deb_depends_string = _convert_version_list_into_comma_string( deb_depends, deb_name )

        control_info = CONTROL_TEMPLATE % (
                deb_name, installed_size, DEBMAINT, DEBARCH, deb_version,
                deb_depends_string, deb_desc)
        f = open(str(target[0]), 'w')
        f.write(control_info)
        f.close()

    command_for_control_file = env.Command(deb_control_file_abs_path, binaries_for_deb_install, make_deb_control_file)

    #------ END   SECTION:   ** house-keeping/bureaucratic files required by dpkg **     -------------
    #-------------------------------------------------------------------------------------------------

    debpkg = '$STAGING_DIR/%s_%s_%s.deb' % (deb_name, deb_version, DEBARCH)

    if sys.platform != 'linux2': # see the comments above about why we run nearly all of this deb code on non-linux platforms, too.
        make_deb_pkg = None
        print "Not on linux, so we only pretend to specify deb file " + env.subst(debpkg)
        print "[following command not run due to non-linux os] fakeroot dpkg-deb -b %s %s" % (outer_folder_for_this_deb, debpkg)

    else:

        # make the deb
        make_deb_pkg = env.Command(
            debpkg,
            deb_control_file_abs_path,
            "fakeroot dpkg-deb -b %s %s" % (outer_folder_for_this_deb, "$TARGET")
            )

        # this dependency will make scons wait until all contents of
        # outer_folder_for_this_deb are produced before calling the
        # dpkg-deb command
        env.Depends( make_deb_pkg, outer_folder_for_this_deb )

    env.Alias( str(project_target_name), make_deb_pkg )

    # According to the SCons man page:
    #
    # "...Alias can be called multiple times for the same alias to add
    # additional targets to the alias ..."
    #
    # Therefore, by the time all SConscripts are read, the single
    # alias 'all_deb_packages' should "point" at all of our various
    # debs.
    env.Alias( 'all_deb_packages', make_deb_pkg )

    return make_deb_pkg
