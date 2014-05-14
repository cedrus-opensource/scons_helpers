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
    if env['BUILD_TYPE'] == 'opt':
        if True:
            lib_path = [ os.getenv('GMOCK','')+'/lib/Release2010']
        linked_libraries = [ 'gmock', 'gtest' ]
    else:
        if True:
            lib_path = [ os.getenv('GMOCK','')+'/lib/Debug2010' ]
        linked_libraries = [ 'gmock', 'gtestd' ]

    include_path = [ '/I'+os.getenv('GMOCK','')+'/include/' ]

    cppdefines = [
        'GTEST_USE_OWN_TR1_TUPLE=0',
        ]

    env.AppendUnique( CXXFLAGS = include_path,
                LIBPATH = lib_path,
                LIBS = linked_libraries,
                CPPDEFINES = cppdefines )


def need_gmock_mac(env):

    if not platform.mac_ver()[0].startswith('10.4'):
        include_path = [ '-isystem'+os.getenv('GMOCK', '')+'/include', ]
    else:
        include_path = [ '-I'+os.getenv('GMOCK', '')+'/include', ]

    lib_path = [ os.getenv('GMOCK', '')+'/lib', ]
    linked_libs = [ 'gmock', 'gtest' ]

    env.AppendUnique( CXXFLAGS = include_path,
                LIBS = linked_libs,
                LIBPATH = lib_path,
                )

def publish_all_libs_to_staging(env):
    # publish gmock libraries
    gmock_libs = env.Glob( os.getenv('GMOCK', '')+'/lib/*.dylib')
    gmock_libs += env.Glob( os.getenv('GMOCK', '')+'/lib/*.a')

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



