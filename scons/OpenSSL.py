#!/bin/python

import os
import sys

def need_openssl(env):
    if sys.platform == 'darwin':
        need_openssl_mac(env)
    elif sys.platform == 'win32':
        need_openssl_windows(env)
    elif sys.platform == 'linux2':
        need_openssl_linux(env)
    else:
        raise ValueError('Unknown Operating System')

def publish_all_libs_to_staging(env):
    if sys.platform == 'darwin':
        return publish_all_libs_to_staging_mac(env)
    elif sys.platform == 'win32':
        return publish_all_libs_to_staging_win(env)
    elif sys.platform == 'linux2':
        return []
    else:
        raise ValueError('Unknown Operating System')

def need_openssl_mac(env):
    lib_dependencies = ['ssl', 'crypto']
    include_path = ['-I/' + env['OPENSSL']+'/darwin/include/']
    libpath = [env['OPENSSL']+'/darwin/lib']

    env.AppendUnique( CXXFLAGS = include_path,
                LIBPATH = libpath,
                LIBS = lib_dependencies, )

def publish_all_libs_to_staging_win(env):
    ssl_libs = env.Glob(env['OPENSSL']+'/bin/*.dll')

    results = []

    for lib in ssl_libs:
        results += env.Install('$STAGING_DIR', lib)

    return results

def publish_all_libs_to_staging_mac(env):
    ssl_loc_prefix = env['OPENSSL']+'/darwin/lib/'

    exclude = [ssl_loc_prefix+'libssl.dylib', ssl_loc_prefix+'libcrypto.dylib']
    ssl_libs = env.Glob(ssl_loc_prefix+'*.dylib', exclude=exclude)

    results = []

    for lib in ssl_libs:
        results += env.Install('$STAGING_DIR', lib)
        results += env.Install(env.subst('$STAGING_DIR/') + env['APP_BUNDLE_NAME'] + '.app/Contents/MacOS/', lib)

    return results

def need_openssl_windows(env):
    lib_dependencies = [ 'ssleay32', 'libeay32' ]
    include_path = [ '/I' + env['OPENSSL']+'/include/' ]
    libpath = [ env['OPENSSL']+'/lib' ]

    env.AppendUnique( CXXFLAGS = include_path,
                LIBPATH = libpath,
                LIBS = lib_dependencies, )

def need_openssl_linux(env):
    lib_dependencies = [ 'ssl','crypto' ]

    env.AppendUnique( LIBS = lib_dependencies )

