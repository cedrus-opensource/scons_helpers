#!/usr/bin/env python

import os
import platform
import sys

def need_mysql_client(env):
    if sys.platform == 'darwin':
        need_mysql_client_mac(env)
    elif sys.platform == 'win32':
        need_mysql_client_windows(env)
    elif sys.platform == 'linux2':
        need_mysql_client_linux(env)
    else:
        raise ValueError('Unknown Operating System.')

def publish_all_libs_to_staging(env):
    if sys.platform == 'darwin':
        return publish_all_libs_to_staging_mac(env)
    elif sys.platform == 'win32':
        return publish_all_libs_to_staging_windows(env)
    elif sys.platform == 'linux2':
        return []
    else:
        raise ValueError('Unknown Operating System.')

def publish_all_libs_to_staging_mac(env):
    # publish mysql libs
    mysql_libs = env.Glob( os.getenv('MYSQL','')+'/lib/mysql/*.dylib' )
    mysql_libs += env.Glob( os.getenv('MYSQL','')+'/lib/mysql/*.a')

    results = []

    for lib in mysql_libs:
        name_parts = os.path.splitext(lib.name)
        if name_parts[1] == '.dylib':
            results += env.Install( '$STAGING_DIR', lib )

    # also publish mysql++ (mysqlpp) libs
    mysqlpp_libs = env.Glob( os.getenv('MYSQLPP','')+'/lib/*.dylib' )

    for lib in mysqlpp_libs:
        results += env.Install( '$STAGING_DIR', lib )

    return results

def publish_all_libs_to_staging_windows(env):
    # publish libraries
    mysql_libs = env.Glob( os.getenv('MYSQL','')+'/lib/*.dll' )

    results = []

    for lib in mysql_libs:
        name_parts = os.path.splitext(lib.name)
        lib_basename = name_parts[0]
        results += env.Install( '$STAGING_DIR', lib )

    return results


def need_mysql_client_mac(env):
    cxxflags = [ '-isystem'+os.getenv('MYSQL','')+'/include/mysql' ]

    lib_dirs = [ os.getenv('MYSQL','')+'/lib/mysql' ]
    lib_dependencies = [ 'mysqlclient' ]

    env.AppendUnique( CXXFLAGS = cxxflags,
                LIBPATH = lib_dirs,
                LIBS = lib_dependencies, )

def need_mysql_client_windows(env):

    lib_path = [ os.getenv('MYSQL','')+'/lib' ]
    include_path = [ '/I'+os.getenv('MYSQL','')+'/include/' ]
    libs = [ 'mysqlclient' ]

    env.AppendUnique( LIBPATH = lib_path,
                CXXFLAGS = include_path,
                LIBS = libs, )



def need_mysql_client_linux(env):
    cxxflags = [ '-isystem/usr/include/mysql' ]
    lib_dependencies = [ 'mysqlclient' ]

    env.AppendUnique( LIBS = lib_dependencies,
                CXXFLAGS = cxxflags, )


def need_mysqlpp(env):

    if sys.platform == 'darwin':
        need_mysqlpp_mac(env)
    elif sys.platform == 'win32':
        need_mysqlpp_windows(env)
    elif sys.platform == 'linux2':
        need_mysqlpp_linux(env)
    else:
        raise ValueError('Unknown Operating System')


def need_mysqlpp_mac(env):

    need_mysql_client_mac(env)

    if not platform.mac_ver()[0].startswith('10.4'):
        cxxflags = [ '-isystem'+os.getenv('MYSQLPP','')+'/include/mysql++' ]
    else:
        cxxflags = [ '-I'+os.getenv('MYSQLPP','')+'/include/mysql++' ]

    lib_path = [ os.getenv('MYSQLPP','')+'/lib' ]
    libs = [ 'mysqlpp' ]

    env.AppendUnique( CXXFLAGS = cxxflags,
                LIBPATH = lib_path,
                LIBS = libs, )

def need_mysqlpp_windows(env):

    include_path = [ '/I'+os.getenv('MYSQLPP','') + '/include/mysql++' ]
    lib_path = [ os.getenv('MYSQLPP','') + '/lib' ]

    include_path += [ '/I'+os.getenv('MYSQL','')+'/include/' ]

    if env['BUILD_TYPE'] == 'opt':
        lib_dependencies = [ 'mysqlpp_d' ]
    else:
        lib_dependencies = [ 'mysqlpp' ]

    env.AppendUnique( CXXFLAGS = include_path,
                LIBPATH = lib_path,
                LIBS = lib_dependencies, )

def need_mysqlpp_linux(env):
    cxxflags = [ '-isystem/usr/include/mysql++' ]
    libs = [ 'mysqlpp' ]

    env.AppendUnique( CXXFLAGS = cxxflags,
                LIBS = libs, )
