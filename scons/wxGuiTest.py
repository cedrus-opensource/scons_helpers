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

    if env['BUILD_TYPE'] == 'opt':
        lib = os.getenv('WXWIN_29','') + '/built_libs/lib/libwxGuiTesting_opt.dylib'
    else:
        lib = os.getenv('WXWIN_29','') + '/built_libs/lib/libwxGuiTesting_dbg.dylib'

    results = []

    results += env.Install( '$STAGING_DIR', lib )

    return results

def publish_all_libs_to_staging_windows(env):
    # no need to publish.  Statically linked
    return []

def need_wxGuiTest_mac(env):

    include_path = [ '-isystem'+os.getenv('WXGUITEST','')+'/cppunit-1.13.2/include',
                     '-isystem'+os.getenv('WXGUITEST','')+'/wxGuiTest/include' ]

    if env['BUILD_TYPE'] == 'opt':
        linked_libs = [ 'wxGuiTesting_opt', 'cppunit' ]
    else:
        linked_libs = [ 'wxGuiTesting_dbg', 'cppunit' ]

    lib_path = [ os.getenv('WXWIN_29','') + '/built_libs/lib/' ]

    env.AppendUnique( CXXFLAGS = include_path,
                      LIBS = linked_libs,
                      LIBPATH = lib_path,
                      )


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

