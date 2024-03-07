import os
from SCons.Script import *
import platform

class CedrusBoostSettings:
    def __init__(self, env):
        if sys.platform == 'win32':
             self.impl = CedrusBoostSettingsWindows(env)
        elif sys.platform == 'linux2':
            self.impl = CedrusBoostSettingsLinux(env)
        elif sys.platform == 'darwin':
            self.impl = CedrusBoostSettingsMac(env)
        else:
            raise ValueError('Unknown Operating System')

        if env['BOOST_VERSION'] != '1_42':
            # in retrospect, this flag is more like 'BOOST=MODERN' or BOOST=MORE_RECENT_THAN_1_42.
            # We want to set this flag for ANY boost beyond 1_42. i now realize this after testing 1_50.
            # It would be a burden to edit all source files now. Hindsight...
            env.AppendUnique( CPPDEFINES = [ 'BOOST_PREPROC_FLAG=1490' ] )

        self.env = env

    def publish_all_libs_to_staging(self):
        # We are still deeply menaced by the specter of this being a helper that can be
        # used by multiple parts of a build. We're keeping track of which boost libs
        # we've added so far to avoid breaking SCons by trying to install two identical
        # libs from different sources into the same target.
        lib_extension = "*.dll"
        if sys.platform == 'darwin':
            lib_extension = "*.dylib"

        self.env.SetDefault(STAGED_BOOST_LIBS = [])
        staged_libs = self.env['STAGED_BOOST_LIBS']

        boost_libs = self.env.Glob( self.env['BOOST_DIR'] + '/lib/*' + self.impl.publish_match_str + self.env['BOOST_VERSION'] + lib_extension )

        results = []

        for lib in boost_libs:
            if lib.name not in staged_libs:
                self.env.AppendUnique(STAGED_BOOST_LIBS = lib.name)
                results += self.env.Install( '$STAGING_DIR', lib )

        return results

    def need_boost_system(self):
        self.impl.need_boost_system(self.env)

    def need_boost_chrono(self):
        self.impl.need_boost_chrono(self.env)

    def need_boost_serialization(self):
        self.impl.need_boost_serialization(self.env)

    def need_boost_thread(self):
        self.impl.need_boost_thread(self.env)

    def need_boost_date_time(self):
        self.impl.need_boost_date_time(self.env)

    def need_boost_filesystem(self):
        self.impl.need_boost_filesystem(self.env)

    def need_boost_python(self):
        self.impl.need_boost_python(self.env)

    def need_boost_regex(self):
        self.impl.need_boost_regex(self.env)

    def need_boost_signals(self):
        self.impl.need_boost_signals(self.env)

    def need_boost_math(self):
        self.impl.need_boost_math(self.env)

    def need_all(self):
        # boost python is purposely excluded
        self.need_boost_system()
        self.need_boost_chrono()
        self.need_boost_serialization()
        self.need_boost_thread()
        self.need_boost_date_time()
        self.need_boost_filesystem()
        self.need_boost_regex()
        self.need_boost_signals()
        self.need_boost_math()

class CedrusBoostSettingsMac:
    def __init__(self, env):
        # add boost CXX flags
        if not platform.mac_ver()[0].startswith('10.4'):
            cxxflags = [ '-isystem' + env['BOOST_DIR'] + '/include' ]
        else:
            cxxflags = [ '-I' + env['BOOST_DIR'] + '/include' ]

        lib_path = [ env['BOOST_DIR'] + '/lib/' ]

        env.AppendUnique( CXXFLAGS = cxxflags, LIBPATH = lib_path, )

        if env['BOOST_VERSION'] != '1_42':
            # in retrospect, this flag is more like 'BOOST=MODERN' or BOOST=MORE_RECENT_THAN_1_42.
            # We want to set this flag for ANY boost beyond 1_42. i now realize this after testing 1_50.
            # It would be a burden to edit all source files now. Hindsight...
            env.AppendUnique( CPPDEFINES = [ 'BOOST_PREPROC_FLAG=1490' ] )

        self.publish_match_str = ''

    def add_library(self, env, library):
        env.AppendUnique( LIBS = [library] )

    def need_boost_system(self, env):
        self.add_library(env, 'boost_system-clang-darwin42-mt-'+env['BOOST_VERSION'])

    def need_boost_chrono(self, env):
        self.add_library(env, 'boost_chrono-clang-darwin42-mt-'+env['BOOST_VERSION'])

    def need_boost_serialization(self, env):
        self.add_library(env, 'boost_serialization-clang-darwin42-mt-'+env['BOOST_VERSION'])
        self.add_library(env, 'boost_wserialization-clang-darwin42-mt-'+env['BOOST_VERSION'])

    def need_boost_thread(self, env):
        self.add_library(env, 'boost_thread-clang-darwin42-mt-'+env['BOOST_VERSION'])

    def need_boost_date_time(self, env):
        self.add_library(env, 'boost_date_time-clang-darwin42-mt-'+env['BOOST_VERSION'])

    def need_boost_filesystem(self, env):
        self.add_library(env, 'boost_filesystem-clang-darwin42-mt-'+env['BOOST_VERSION'])

    def need_boost_python(self, env):
        self.add_library(env, 'boost_python-clang-darwin42-mt-'+env['BOOST_VERSION'])

    def need_boost_regex(self, env):
        self.add_library(env, 'boost_regex-clang-darwin42-mt-'+env['BOOST_VERSION'])

    def need_boost_signals(self, env):
        self.add_library(env, 'boost_signals-clang-darwin42-mt-'+env['BOOST_VERSION'])

    def need_boost_math(self, env):
        pass

class CedrusBoostSettingsWindows:
    def __init__(self, env):

        # add boost to CXXflags
        include_path = [ '/I' + env['BOOST_DIR'] + '/include' ]

        lib_path = [ env['BOOST_DIR'] + '/lib' ]

        env.AppendUnique( CXXFLAGS = include_path, LIBPATH = lib_path )

        self.vc_ver = 'vc143' if env['MSVC_VERSION'] == '14.3' else 'vc100'

        self.build_tag = '-mt-gd-x64-' if env['BUILD_TYPE'] == 'dbg' else '-mt-x64-'

        self.publish_match_str = "%s%s" % (self.vc_ver, self.build_tag)

    def add_library(self, env, library):
        env.AppendUnique( LIBS = [library] )

    def need_boost_system(self, env):
        self.add_library(env, 'boost_system-' + self.vc_ver + self.build_tag + env['BOOST_VERSION'])

    def need_boost_chrono(self, env):
        self.add_library(env, 'boost_chrono-' + self.vc_ver + self.build_tag + env['BOOST_VERSION'])

    def need_boost_serialization(self, env):
        self.add_library(env, 'boost_serialization-' + self.vc_ver + self.build_tag + env['BOOST_VERSION'])
        self.add_library(env, 'boost_wserialization-' + self.vc_ver + self.build_tag + env['BOOST_VERSION'])

    def need_boost_thread(self, env):
        self.add_library(env, 'boost_thread-' + self.vc_ver + self.build_tag + env['BOOST_VERSION'])

    def need_boost_date_time(self, env):
        self.add_library(env, 'boost_date_time-' + self.vc_ver + self.build_tag + env['BOOST_VERSION'])

    def need_boost_filesystem(self, env):
        self.add_library(env, 'boost_filesystem-' + self.vc_ver + self.build_tag + env['BOOST_VERSION'])

    def need_boost_python(self, env):
        self.add_library(env, 'boost_python-' + self.vc_ver + self.build_tag + env['BOOST_VERSION'])

    def need_boost_regex(self, env):
        self.add_library(env, 'boost_regex-' + self.vc_ver + self.build_tag + env['BOOST_VERSION'])

    def need_boost_signals(self, env):
        self.add_library(env, 'boost_signals-' + self.vc_ver + self.build_tag + env['BOOST_VERSION'])

    def need_boost_math(self, env):
        self.add_library(env, 'boost_math_c99f-' + self.vc_ver + self.build_tag + env['BOOST_VERSION'])
        self.add_library(env, 'boost_math_c99l-' + self.vc_ver + self.build_tag + env['BOOST_VERSION'])
        self.add_library(env, 'boost_math_c99-' + self.vc_ver + self.build_tag + env['BOOST_VERSION'])
        self.add_library(env, 'boost_math_tr1f-' + self.vc_ver + self.build_tag + env['BOOST_VERSION'])
        self.add_library(env, 'boost_math_tr1l-' + self.vc_ver + self.build_tag + env['BOOST_VERSION'])
        self.add_library(env, 'boost_math_tr1-' + self.vc_ver + self.build_tag + env['BOOST_VERSION'])

class CedrusBoostSettingsLinux:
    def __init__(self, env):
        # on Ubuntu 10 ('lucid'), we used to build boost, and it had version-suffixes.
        # on Ubuntu 13 ('saucy'), we use the 'standard' boost binaries provided by Ubuntu. They lack suffixes.
        cxxflags = [ '-isystem/usr/include/boost' ] #-'+env['BOOST_VERSION']+'/',  # see note about lucid/saucy above

        lib_path = [ ]

        env.AppendUnique( CXXFLAGS = cxxflags, LIBPATH = lib_path, )

        self.publish_match_str = ''

    def need_boost_system(self, env):
        libname = 'boost_system'            #-gcc43-mt-'+env['BOOST_VERSION']  # see note about lucid/saucy above
        env.AppendUnique( LIBS= [libname] )

    def need_boost_chrono(self, env):
        libname = 'boost_chrono'            #-gcc43-mt-'+env['BOOST_VERSION']  # see note about lucid/saucy above
        env.AppendUnique( LIBS= [libname] )

    def need_boost_serialization(self, env):
        libname1 = 'boost_serialization'    #-gcc43-mt-'+env['BOOST_VERSION']  # see note about lucid/saucy above
        libname2 = 'boost_wserialization'   #-gcc43-mt-'+env['BOOST_VERSION']  # see note about lucid/saucy above
        env.AppendUnique( LIBS= [libname1, libname2] )

    def need_boost_thread(self, env):
        libname = 'boost_thread'            #-gcc43-mt-'+env['BOOST_VERSION']  # see note about lucid/saucy above
        env.AppendUnique( LIBS= [libname] )

    def need_boost_date_time(self, env):
        libname = 'boost_date_time'         #-gcc43-mt-'+env['BOOST_VERSION']  # see note about lucid/saucy above
        env.AppendUnique( LIBS = [libname] )

    def need_boost_filesystem(self, env):
        libname = 'boost_filesystem'        #-gcc43-mt-'+env['BOOST_VERSION']  # see note about lucid/saucy above
        env.AppendUnique( LIBS = [libname] )

    def need_boost_python(self, env):
        libname = 'boost_python'            #-gcc43-mt-'+env['BOOST_VERSION']  # see note about lucid/saucy above
        env.AppendUnique( LIBS = [libname] )

    def need_boost_regex(self, env):
        libname = 'boost_regex'             #-gcc43-mt-'+env['BOOST_VERSION']  # see note about lucid/saucy above
        env.AppendUnique( LIBS = [libname] )

    def need_boost_signals(self, env):
        libname = 'boost_signals'           #-gcc43-mt-'+env['BOOST_VERSION']  # see note about lucid/saucy above
        env.AppendUnique( LIBS = [libname] )

    def need_boost_math(self, env):
        pass
