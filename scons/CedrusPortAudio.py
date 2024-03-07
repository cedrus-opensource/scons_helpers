#!/usr/bin/env python

import SCons
import os
import platform
import sys
import glob

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
    ENV_VAR_VAL_PORTAUDIO = str(env['PORTAUDIO'])
    env.PrependUnique(
        LIBS=['portaudio', 'sndfile'],
        CPPPATH=[ENV_VAR_VAL_PORTAUDIO + '/include'],
        LIBPATH=[ENV_VAR_VAL_PORTAUDIO + '/lib'], )

    dependency_port_audio_name = 'portaudio.dll'

def need_pa_w_sndfile_mac(env):
    ENV_VAR_VAL_PORTAUDIO = str(env['PORTAUDIO'])
    env.PrependUnique(
        CPPPATH=[ENV_VAR_VAL_PORTAUDIO + os.path.sep +  'include'],
        LIBS=['sndfile.1', 'portaudio.2'],
        LIBPATH=[ENV_VAR_VAL_PORTAUDIO + os.path.sep + 'lib'], )

    dependency_port_audio_name = 'libportaudio.2.dylib'

def publish_all_libs_to_staging_windows(env, app_suffix):
    ENV_VAR_VAL_PORTAUDIO = str(env['PORTAUDIO'])
    dependency_libsndfile = ENV_VAR_VAL_PORTAUDIO + '/lib/sndfile.dll'
    dependency_port_audio_name = 'portaudio.dll'
    dependency_port_audio = ENV_VAR_VAL_PORTAUDIO + '/lib/' + dependency_port_audio_name

    additional_libs = []

    additional_libs += env.Glob(ENV_VAR_VAL_PORTAUDIO + '/lib/vorbis.dll')
    additional_libs += env.Glob(ENV_VAR_VAL_PORTAUDIO + '/lib/vorbisenc.dll')
    additional_libs += env.Glob(ENV_VAR_VAL_PORTAUDIO + '/lib/FLAC.dll')
    additional_libs += env.Glob(ENV_VAR_VAL_PORTAUDIO + '/lib/mpg123.dll')
    additional_libs += env.Glob(ENV_VAR_VAL_PORTAUDIO + '/lib/opus.dll')
    additional_libs += env.Glob(ENV_VAR_VAL_PORTAUDIO + '/lib/ogg.dll')
    additional_libs += env.Glob(ENV_VAR_VAL_PORTAUDIO + '/lib/libmp3lame.dll')

    results = env.Install(_get_outer_app_folder(env, app_suffix),
                          dependency_libsndfile)

    for lib in additional_libs:
        results += env.Install(_get_outer_app_folder(env, app_suffix),
                          lib)

    results += env.Command(_get_outer_app_folder(env, app_suffix) + '/' + dependency_port_audio_name,
                           dependency_port_audio, SCons.Script.Copy("$TARGET", "$SOURCE"))

    return results

def publish_all_libs_to_staging_mac(env, app_suffix):
    ENV_VAR_VAL_PORTAUDIO = str(env['PORTAUDIO'])
    dependency_libsndfile = glob.glob(ENV_VAR_VAL_PORTAUDIO + os.path.sep + 'lib/*.dylib')
    dependency_port_audio_name = 'libportaudio.2.dylib'
    dependency_port_audio = ENV_VAR_VAL_PORTAUDIO + os.path.sep + 'lib/libportaudio.2.dylib'

    frameworks_dir1 = _get_outer_app_folder(env, app_suffix) + '/Contents/Frameworks/'

    results = env.Install(frameworks_dir1, dependency_libsndfile)

    results += env.Command(frameworks_dir1 + '/' + dependency_port_audio_name,
                           dependency_port_audio, SCons.Script.Copy("$TARGET", "$SOURCE"))

    # since SLPlugInCommon needs portaudio, and TestAppForRegistrationDialog needs SLPlugInCommon,
    # then (you can easily deduce) TestAppForRegistrationDialog needs the dylibs in its Frameworks
    frameworks_dir2 = _get_outer_testapp_folder(env) + '/Contents/Frameworks/'

    results += env.Install(frameworks_dir2, dependency_libsndfile)

    results += env.Command(frameworks_dir2 + '/' + dependency_port_audio_name,
                           dependency_port_audio, SCons.Script.Copy("$TARGET", "$SOURCE"))

    weird_other_folder_so_tests_launch = os.path.normpath( str( env.subst( '$STAGING_DIR/../Frameworks/' ) ) )

    results += env.Install(weird_other_folder_so_tests_launch, dependency_libsndfile)

    results += env.Command(weird_other_folder_so_tests_launch + '/' + dependency_port_audio_name,
                           dependency_port_audio, SCons.Script.Copy("$TARGET", "$SOURCE"))

    return results
