import os
from SCons.Script import *
import platform

class CedrusBoostSettings:
    def __init__(self, env):
        if sys.platform == 'win32':
            if env['BUILD_TYPE'] == 'opt':
                self.impl = CedrusBoostSettingsWindowsRelease(env)
            if env['BUILD_TYPE'] == 'dbg':
                self.impl = CedrusBoostSettingsWindowsDebug(env)
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
        return self.impl.publish_all_libs_to_staging(self.env)

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
            cxxflags = [
                '-isystem'+os.getenv('BOOST','')+'/include/boost-'+env['BOOST_VERSION']+'/',
            ]
        else:
            cxxflags = [
                '-I'+os.getenv('BOOST','')+'/include/boost-'+env['BOOST_VERSION']+'/',
            ]

        lib_path = [
            os.getenv('BOOST','')+'/lib/',
            ]

        env.AppendUnique( CXXFLAGS = cxxflags,
                    LIBPATH = lib_path, )

        if env['BOOST_VERSION'] != '1_42':
            # in retrospect, this flag is more like 'BOOST=MODERN' or BOOST=MORE_RECENT_THAN_1_42.
            # We want to set this flag for ANY boost beyond 1_42. i now realize this after testing 1_50.
            # It would be a burden to edit all source files now. Hindsight...
            env.AppendUnique( CPPDEFINES = [ 'BOOST_PREPROC_FLAG=1490' ] )


    def add_library(self, env, library):
        env.AppendUnique( LIBS = [library] )

    def need_boost_system(self, env):
        self.add_library(env, 'boost_system-xgcc811-mt-'+env['BOOST_VERSION'])

    def need_boost_chrono(self, env):
        self.add_library(env, 'boost_chrono-xgcc811-mt-'+env['BOOST_VERSION'])

    def need_boost_serialization(self, env):
        self.add_library(env, 'boost_serialization-xgcc811-mt-'+env['BOOST_VERSION'])
        self.add_library(env, 'boost_wserialization-xgcc811-mt-'+env['BOOST_VERSION'])


    def need_boost_thread(self, env):
        self.add_library(env, 'boost_thread-xgcc811-mt-'+env['BOOST_VERSION'])


    def need_boost_date_time(self, env):
        self.add_library(env, 'boost_date_time-xgcc811-mt-'+env['BOOST_VERSION'])


    def need_boost_filesystem(self, env):
        self.add_library(env, 'boost_filesystem-xgcc811-mt-'+env['BOOST_VERSION'])


    def need_boost_python(self, env):
        self.add_library(env, 'boost_python-xgcc811-mt-'+env['BOOST_VERSION'])


    def need_boost_regex(self, env):
        self.add_library(env, 'boost_regex-xgcc811-mt-'+env['BOOST_VERSION'])


    def need_boost_signals(self, env):
        self.add_library(env, 'boost_signals-xgcc811-mt-'+env['BOOST_VERSION'])

    def need_boost_math(self, env):
        pass

    def publish_all_libs_to_staging(self, env):
        # publish boost libraries
        boost_libs = env.Glob( os.getenv('BOOST')+'/lib/*' + env['BOOST_VERSION'] + '*.dylib' )

        results = []

        for lib in boost_libs:
            results += env.Install( '$STAGING_DIR', lib )

        return results


class CedrusBoostSettingsWindowsRelease:
    def __init__(self,env):

        # add boost to CXXflags
        include_path = [
            '/I'+os.getenv('BOOST_ROOT','')+'/include/boost-'+env['BOOST_VERSION']+'/',
            ]

        self.vcver = 'vc100'

        lib_path = [
            os.getenv('BOOST_ROOT','')+'/lib/',
            ]

        env.AppendUnique( CXXFLAGS = include_path,
                    LIBPATH = lib_path )

    def publish_all_libs_to_staging(self, env):
        boost_libs = env.Glob( os.getenv('BOOST_ROOT','')+'/lib/*'  + env['BOOST_VERSION'] + '*.dll' )

        results = []

        for lib in boost_libs:
            name_parts = os.path.splitext(lib.name)
            lib_basename = name_parts[0]
            results += env.Install( '$STAGING_DIR', lib )

        return results

    def add_library(self, env, library):
        env.AppendUnique( LIBS = [library] )


    def need_boost_system(self, env):
        self.add_library(env, 'boost_system-'+self.vcver+'-mt-'+env['BOOST_VERSION'])

    def need_boost_chrono(self, env):
        self.add_library(env, 'boost_chrono-'+self.vcver+'-mt-'+env['BOOST_VERSION'])

    def need_boost_serialization(self, env):
        self.add_library(env, 'boost_serialization-'+self.vcver+'-mt-'+env['BOOST_VERSION'])
        self.add_library(env, 'boost_wserialization-'+self.vcver+'-mt-'+env['BOOST_VERSION'])


    def need_boost_thread(self, env):
        self.add_library(env, 'boost_thread-'+self.vcver+'-mt-'+env['BOOST_VERSION'])


    def need_boost_date_time(self, env):
        self.add_library(env, 'boost_date_time-'+self.vcver+'-mt-'+env['BOOST_VERSION'])


    def need_boost_filesystem(self, env):
        self.add_library(env, 'boost_filesystem-'+self.vcver+'-mt-'+env['BOOST_VERSION'])


    def need_boost_python(self, env):
        self.add_library(env, 'boost_python-'+self.vcver+'-mt-'+env['BOOST_VERSION'])


    def need_boost_regex(self, env):
        self.add_library(env, 'boost_regex-'+self.vcver+'-mt-'+env['BOOST_VERSION'])


    def need_boost_signals(self, env):
        self.add_library(env, 'boost_signals-'+self.vcver+'-mt-'+env['BOOST_VERSION'])

    def need_boost_math(self, env):
        self.add_library(env, 'boost_math_c99f-'+self.vcver+'-mt-'+env['BOOST_VERSION'])
        self.add_library(env, 'boost_math_c99l-'+self.vcver+'-mt-'+env['BOOST_VERSION'])
        self.add_library(env, 'boost_math_c99-'+self.vcver+'-mt-'+env['BOOST_VERSION'])
        self.add_library(env, 'boost_math_tr1f-'+self.vcver+'-mt-'+env['BOOST_VERSION'])
        self.add_library(env, 'boost_math_tr1l-'+self.vcver+'-mt-'+env['BOOST_VERSION'])
        self.add_library(env, 'boost_math_tr1-'+self.vcver+'-mt-'+env['BOOST_VERSION'])



class CedrusBoostSettingsWindowsDebug:
    def __init__(self, env):

        # add boost to CXXflags
        include_path = [
            '/I'+os.getenv('BOOST_ROOT','')+'/include/boost-'+env['BOOST_VERSION']+'/',
            ]

        self.vcver = 'vc100'

        lib_path = [
            os.getenv('BOOST_ROOT','')+'/lib/',
            ]

        env.AppendUnique( CXXFLAGS = include_path,
                    LIBPATH = lib_path )

    def publish_all_libs_to_staging(self, env):
        boost_libs = env.Glob( os.getenv('BOOST_ROOT','')+'/lib/*'  + env['BOOST_VERSION'] + '*.dll' )

        results = []

        for lib in boost_libs:
            name_parts = os.path.splitext(lib.name)
            lib_basename = name_parts[0]
            results += env.Install( '$STAGING_DIR', lib )

        return results


    def add_library(self, env, library):
        env.AppendUnique( LIBS = [library] )


    def need_boost_system(self, env):
        self.add_library(env, 'boost_system-'+self.vcver+'-mt-gd-'+env['BOOST_VERSION'])

    def need_boost_chrono(self, env):
        self.add_library(env, 'boost_chrono-'+self.vcver+'-mt-gd-'+env['BOOST_VERSION'])

    def need_boost_serialization(self, env):
        self.add_library(env, 'boost_serialization-'+self.vcver+'-mt-gd-'+env['BOOST_VERSION'])
        self.add_library(env, 'boost_wserialization-'+self.vcver+'-mt-gd-'+env['BOOST_VERSION'])


    def need_boost_thread(self, env):
        self.add_library(env, 'boost_thread-'+self.vcver+'-mt-gd-'+env['BOOST_VERSION'])


    def need_boost_date_time(self, env):
        self.add_library(env, 'boost_date_time-'+self.vcver+'-mt-gd-'+env['BOOST_VERSION'])


    def need_boost_filesystem(self, env):
        self.add_library(env, 'boost_filesystem-'+self.vcver+'-mt-gd-'+env['BOOST_VERSION'])


    def need_boost_python(self, env):
        self.add_library(env, 'boost_python-'+self.vcver+'-mt-gd-'+env['BOOST_VERSION'])


    def need_boost_regex(self, env):
        self.add_library(env, 'boost_regex-'+self.vcver+'-mt-gd-'+env['BOOST_VERSION'])


    def need_boost_signals(self, env):
        self.add_library(env, 'boost_signals-'+self.vcver+'-mt-gd-'+env['BOOST_VERSION'])


    def need_boost_math(self, env):
        self.add_library(env, 'boost_math_c99f-'+self.vcver+'-mt-gd-'+env['BOOST_VERSION'])
        self.add_library(env, 'boost_math_c99l-'+self.vcver+'-mt-gd-'+env['BOOST_VERSION'])
        self.add_library(env, 'boost_math_c99-'+self.vcver+'-mt-gd-'+env['BOOST_VERSION'])
        self.add_library(env, 'boost_math_tr1f-'+self.vcver+'-mt-gd-'+env['BOOST_VERSION'])
        self.add_library(env, 'boost_math_tr1l-'+self.vcver+'-mt-gd-'+env['BOOST_VERSION'])
        self.add_library(env, 'boost_math_tr1-'+self.vcver+'-mt-gd-'+env['BOOST_VERSION'])



class CedrusBoostSettingsLinux:
    def __init__(self, env):

        cxxflags = [
			'-isystem/usr/include/boost-'+env['BOOST_VERSION']+'/',
            ]

        lib_path = [
            ]

        env.AppendUnique( CXXFLAGS = cxxflags,
                    LIBPATH = lib_path, )


    def publish_all_libs_to_staging(self, env):
        return []

    def need_boost_system(self, env):
        libname = 'boost_system-gcc43-mt-'+env['BOOST_VERSION']
        env.AppendUnique( LIBS= [libname] )

    def need_boost_chrono(self, env):
        libname = 'boost_chrono-gcc43-mt-'+env['BOOST_VERSION']
        env.AppendUnique( LIBS= [libname] )

    def need_boost_serialization(self, env):
        libname1 = 'boost_serialization-gcc43-mt-'+env['BOOST_VERSION']
        libname2 = 'boost_wserialization-gcc43-mt-'+env['BOOST_VERSION']
        env.AppendUnique( LIBS= [libname1, libname2] )


    def need_boost_thread(self, env):
        libname = 'boost_thread-gcc43-mt-'+env['BOOST_VERSION']
        env.AppendUnique( LIBS= [libname] )


    def need_boost_date_time(self, env):
        libname = 'boost_date_time-gcc43-mt-'+env['BOOST_VERSION']
        env.AppendUnique( LIBS = [libname] )


    def need_boost_filesystem(self, env):
        libname = 'boost_filesystem-gcc43-mt-'+env['BOOST_VERSION']
        env.AppendUnique( LIBS = [libname] )

    def need_boost_python(self, env):
        libname = 'boost_python-gcc43-mt-'+env['BOOST_VERSION']
        env.AppendUnique( LIBS = [libname] )

    def need_boost_regex(self, env):
        libname = 'boost_regex-gcc43-mt-'+env['BOOST_VERSION']
        env.AppendUnique( LIBS = [libname] )

    def need_boost_signals(self, env):
        libname = 'boost_signals-gcc43-mt-'+env['BOOST_VERSION']
        env.AppendUnique( LIBS = [libname] )

    def need_boost_math(self, env):
        pass


