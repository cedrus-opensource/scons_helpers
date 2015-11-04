#!/usr/bin/env python

import SCons
import os
import platform
import sys
import glob

CEDRUS_LIBSNDFILE_VERSION_UNDERSCORE = 'libsndfile_1.0.24'

CEDRUS_LIBSNDFILE_VERSION_HYPHEN = 'libsndfile-1.0.24'


def _get_outer_app_folder(env, app_suffix):

    if sys.platform == 'darwin':
        return env.subst('$STAGING_DIR/') + 'SuperLab ' + app_suffix + '.app'
    elif sys.platform == 'win32':
        return env.subst('$STAGING_DIR/')

def _get_outer_testapp_folder(env):

    if sys.platform == 'darwin':
        return env.subst('$STAGING_DIR/') + 'TestAppForRegistrationDialog.app'
    elif sys.platform == 'win32':
        # not really needed at all on win32. dll(s) already put here by _get_outer_app_folder
        return env.subst('$STAGING_DIR/')


def need_pa_w_sndfile(env):
    if sys.platform == 'darwin':
        need_pa_w_sndfile_mac(env)
    elif sys.platform == 'win32':
        need_pa_w_sndfile_windows(env)
    else:
        raise ValueError('Unknown OS')


def publish_all_libs_to_staging(env, app_suffix):
    if sys.platform == 'darwin':
        return publish_all_libs_to_staging_mac(env, app_suffix)
    elif sys.platform == 'win32':
        return publish_all_libs_to_staging_windows(env, app_suffix)
    else:
        raise ValueError('Unknown OS')


def need_pa_w_sndfile_windows(env):

    env.PrependUnique(
        CPPPATH=[str(os.getenv('LIBSNDFILE', '') + '/' +
                     CEDRUS_LIBSNDFILE_VERSION_UNDERSCORE + '/src')],
        LIBS=['libsndfile-1'],
        LIBPATH=[str(os.getenv('LIBSNDFILE', '') + '/' +
                     CEDRUS_LIBSNDFILE_VERSION_UNDERSCORE + '/Win32')], )

    ENV_VAR_VAL_PORTAUDIO = str(os.getenv('PORTAUDIO', ''))

    env.PrependUnique(LIBPATH=[ENV_VAR_VAL_PORTAUDIO], )

    dependency_port_audio_name = 'portaudio_x86.dll'

    env.PrependUnique(
        LIBS=['portaudio_x86'],
        CPPPATH=[ENV_VAR_VAL_PORTAUDIO + '/include/'],
        LIBPATH=[ENV_VAR_VAL_PORTAUDIO + '/build/msvc/Win32/Release'], )


def need_pa_w_sndfile_mac(env):

    env.PrependUnique(
        CPPPATH=[str(os.getenv('PA_WITH_LIBSF', '') + os.path.sep +
                     'include/mac/' + CEDRUS_LIBSNDFILE_VERSION_HYPHEN)],
        LIBS=['sndfile.1'],
        LIBPATH=[str(os.getenv('PA_WITH_LIBSF', '') + os.path.sep + 'lib')], )

    ENV_VAR_VAL_PORTAUDIO = str(os.getenv('PA_WITH_LIBSF', ''))

    env.PrependUnique(
        CPPPATH=[str(os.getenv('PA_WITH_LIBSF', '') + os.path.sep +
                     'include/mac/pa_stable_v19_20110326')],
        LIBS=['portaudio.2'],
        LIBPATH=[str(os.getenv('PA_WITH_LIBSF', '') + os.path.sep + 'lib')], )

    dependency_port_audio_name = 'libportaudio.2.dylib'


def publish_all_libs_to_staging_windows(env, app_suffix):

    dependency_libsndfile = str(os.getenv(
        'LIBSNDFILE', '') + '/' + CEDRUS_LIBSNDFILE_VERSION_UNDERSCORE +
                                '/Win32/libsndfile-1.dll')

    ENV_VAR_VAL_PORTAUDIO = str(os.getenv('PORTAUDIO', ''))

    dependency_port_audio_name = 'portaudio_x86.dll'
    dependency_port_audio = ENV_VAR_VAL_PORTAUDIO + '/build/msvc/Win32/Release/' + dependency_port_audio_name

    results = env.Install(_get_outer_app_folder(env, app_suffix),
                          dependency_libsndfile)

    results += env.Command(
        _get_outer_app_folder(env,
                              app_suffix) + '/' + dependency_port_audio_name,
        dependency_port_audio, SCons.Script.Copy("$TARGET", "$SOURCE"))

    return results


def publish_all_libs_to_staging_mac(env, app_suffix):

    dependency_libsndfile = glob.glob(str(os.getenv('PA_WITH_LIBSF', '') +
                                          os.path.sep + 'lib/*.dylib'))

    dependency_port_audio_name = 'libportaudio.2.dylib'
    dependency_port_audio = os.getenv(
        'PA_WITH_LIBSF', '') + os.path.sep + 'lib/libportaudio.2.dylib'

    frameworks_dir1 = _get_outer_app_folder(
        env, app_suffix) + '/Contents/Frameworks/'

    results = env.Install(frameworks_dir1, dependency_libsndfile)

    results += env.Command(
        frameworks_dir1 + '/' + dependency_port_audio_name,
        dependency_port_audio, SCons.Script.Copy("$TARGET", "$SOURCE"))

    # since SLPlugInCommon needs portaudio, and TestAppForRegistrationDialog needs SLPlugInCommon,
    # then (you can easily deduce) TestAppForRegistrationDialog needs the dylibs in its Frameworks
    frameworks_dir2 = _get_outer_testapp_folder(
        env) + '/Contents/Frameworks/'

    results += env.Install(frameworks_dir2, dependency_libsndfile)

    results += env.Command(
        frameworks_dir2 + '/' + dependency_port_audio_name,
        dependency_port_audio, SCons.Script.Copy("$TARGET", "$SOURCE"))

    weird_other_folder_so_tests_launch = os.path.normpath( str( env.subst( '$STAGING_DIR/../Frameworks/' ) ) )

    results += env.Install(weird_other_folder_so_tests_launch, dependency_libsndfile)

    results += env.Command(
        weird_other_folder_so_tests_launch + '/' + dependency_port_audio_name,
        dependency_port_audio, SCons.Script.Copy("$TARGET", "$SOURCE"))

    return results
