#!/usr/bin/env python

import os
from SCons.Script import *
import CedrusSConsHelperFunctions
import platform

def need_wxGuiTest(env):
    if sys.platform == 'darwin':
        need_wxGuiTest_mac(env)
    elif sys.platform == 'win32':
        need_wxGuiTest_windows(env)
    else:
        raise ValueError('Unsupported Operating System')

def publish_all_libs_to_staging(env):
    if sys.platform == 'darwin':
        return publish_all_libs_to_staging_mac(env)
    elif sys.platform == 'win32':
        return publish_all_libs_to_staging_windows(env)
    else:
        return []


def publish_all_libs_to_staging_mac(env):
    base_folder = os.getenv('WXGUITEST','')

    if env['WX_VERSION'] == '2.8':
        base_folder += '_2.8'

    # publish dylibs
    if env['BUILD_TYPE'] == 'dbg':
        gui_test_libs =  env.Glob(base_folder+'/built_libs/debug/*.dylib')
        gui_test_libs += env.Glob(base_folder+'/built_libs/debug/*.a')
    else:
        gui_test_libs =  env.Glob(base_folder+'/built_libs/release/*.dylib')
        gui_test_libs += env.Glob(base_folder+'/built_libs/release/*.a')

    results = []

    for lib in gui_test_libs:
        name_parts = os.path.splitext(lib.name)
        if name_parts[1] == '.dylib':
            results += env.Install( '$STAGING_DIR', lib )

    return results

def publish_all_libs_to_staging_windows(env):
    # no need to publish.  Statically linked
    return []

def need_wxGuiTest_mac(env):

    base_folder = os.getenv('WXGUITEST','')

    if env['WX_VERSION'] == '2.8':
        base_folder += '_2.8'

    if env['BUILD_TYPE'] == 'dbg':
        lib_path = base_folder+'/built_libs/debug'
    else:
        lib_path = base_folder+'/built_libs/release'

    if not platform.mac_ver()[0].startswith('10.4'):
        include_path = [ '-isystem'+os.getenv('WXGUITEST','')+'/include' ]
    else:
        include_path = [ '-I'+os.getenv('WXGUITEST','')+'/include' ]

    linked_libs = [ 'wxGuiTesting', 'cppunit' ]

    env.AppendUnique( CXXFLAGS = include_path,
                LIBS = linked_libs,
                LIBPATH = lib_path,
                )

    if sys.platform == 'darwin' and env['BUILD_TYPE'] == 'opt':
        # because wxGuiTest is only built for i386, we need to reset the
        # default -arch flags we give to g++ and ld
        CedrusSConsHelperFunctions.FromSwtoolkitFilterOut(
            env,
            CXXFLAGS=['-arch','i386','ppc'],
            LINKFLAGS=['-arch','i386','ppc']
            )
        env.Append(CXXFLAGS=['-arch','i386'],
                   LINKFLAGS=['-arch','i386'])


def need_wxGuiTest_windows(env):

    base_folder = os.getenv('WXGUITEST','')

    if env['WX_VERSION'] == '2.8':
        base_folder += '_2.8'

    # no need to publish.  Statically linked
    if env['BUILD_TYPE'] == 'opt':
            lib_path = [ base_folder+'/built_libs/vs2010-release' ]
    else:
            lib_path = [ base_folder+'/built_libs/vs2010-debug' ]

    include_path = [ '/I'+os.getenv('WXGUITEST','')+'/include' ]
    linked_libraries = [ 'wxGuiTest_StaticLib', 'libCppUnit' ]

    env.AppendUnique( CXXFLAGS = include_path,
                LIBPATH = lib_path,
                LIBS = linked_libraries
                )

