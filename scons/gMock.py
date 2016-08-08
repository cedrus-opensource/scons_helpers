#!/usr/bin/env python

import os
import platform
import sys

def need_gmock(env):
    if sys.platform == 'darwin':
        need_gmock_mac(env)
    elif sys.platform == 'win32':
        need_gmock_windows(env)
    elif sys.platform == 'linux2':
        need_gmock_linux(env)
    else:
        raise ValueError('Unknown OS')

def need_gmock_windows(env):
    # no need to publish. Statically linked

    vs_ver = '2010'
    if env['MSVC_VERSION'] == '14.0' :
        vs_ver = '2015'

    if env['BUILD_TYPE'] == 'opt':
        lib_path = [ env['GMOCK_DIR'] + '/Release' + vs_ver]
        linked_libraries = [ 'gmock', 'gtest' ]
    else:
        lib_path = [ env['GMOCK_DIR'] + '/Debug' + vs_ver ]
        linked_libraries = [ 'gmock', 'gtestd' ]

    include_path = [ '/I' + env['GMOCK_DIR'] + '/win32/include' ]

    cppdefines = [
        'GTEST_USE_OWN_TR1_TUPLE=0',
        ]

    env.AppendUnique( CXXFLAGS = include_path,
                LIBPATH = lib_path,
                LIBS = linked_libraries,
                CPPDEFINES = cppdefines )

def need_gmock_mac(env):

    include_path = [ '-isystem' + env['GMOCK_DIR'] + '/include', ]

    lib_path = [ env['GMOCK_DIR'] + '/lib', ]
    linked_libs = [ 'gtest.0' ]

    env.AppendUnique( CXXFLAGS = include_path,
                LIBS = linked_libs,
                LIBPATH = lib_path,
                )

def publish_all_libs_to_staging(env):
    # publish gmock libraries
    gmock_libs = env.Glob( env['GMOCK_DIR'] + '/lib/*.dylib')
    gmock_libs += env.Glob( env['GMOCK_DIR'] + '/lib/*.a')

    results = []

    for lib in gmock_libs:
        name_parts = os.path.splitext(lib.name)
        if name_parts[1] == '.dylib':
            results += env.Install( '$STAGING_DIR', lib )

    return results

def need_gmock_linux(env):
    linked_libs = [ 'gtest', 'pthread' ]

    lib_path = [ '/usr/src/gtest' ]

    env.AppendUnique( LIBS = linked_libs,
                      LIBPATH = lib_path,
                )

