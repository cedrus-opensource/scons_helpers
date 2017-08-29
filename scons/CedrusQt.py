import os
from SCons.Script import *
import platform

class CedrusQtSettings:
    def __init__(self, env):
        if sys.platform == 'win32':
            self.impl = CedrusQtSettingsWin32()
        elif sys.platform == 'darwin':
            self.impl = CedrusQtSettingsMac()
        else:
            raise ValueError('Operating System Not Yet Supported in CedrusQt.py Module')

        self.env = env

    def publish_all_libs_to_staging(self):
        return self.impl.publish_all_libs_to_staging(self.env)

    def need_qt_basics(self):
        self.impl.need_qt_basics(self.env)

    def need_qt_opengl(self):
        self.impl.need_qt_opengl(self.env)

    def need_qt_sensors(self):
        self.impl.need_qt_sensors(self.env)

    def need_qt_svg(self):
        self.impl.need_qt_svg(self.env)

    def need_qt_test(self):
        self.impl.need_qt_test(self.env)

    def need_qt_xml(self):
        self.impl.need_qt_xml(self.env)

    def need_all(self):
        # qt python is purposely excluded
        self.need_qt_basics()
        self.need_qt_opengl()
        self.need_qt_sensors()
        self.need_qt_svg()
        self.need_qt_test()
        self.need_qt_xml()

class CedrusQtSettingsMac:
    def _use_qt_include_paths(self, env):

        # macosx/include  QT_BINARIES_REPO
        cxxflags = [
            '-isystem' + env['QT_DIR'] + '/include/',
            '-isystem' + env['QT_DIR'] + '/include/QtCore/',
            '-isystem' + env['QT_DIR'] + '/include/QtGui/',
            '-isystem' + env['QT_DIR'] + '/include/QtWidgets/',
            '-isystem' + env['QT_DIR'] + '/include/QtMultimedia/',
            '-isystem' + env['QT_DIR'] + '/include/QtMultimediaWidgets/'


            ]

        lib_path = [  env['QT_DIR']+'/lib' ]

        env.AppendUnique( CXXFLAGS = cxxflags, LIBPATH = lib_path)

        if env['BUILD_TYPE'] == 'opt':
            env.AppendUnique( CPPDEFINES = ['QT_NO_DEBUG_OUTPUT'] )

    def add_library(self, env, library):
        self._use_qt_include_paths(env)
        num_suffix = '.5'
        library += num_suffix
        env.AppendUnique( LIBS = [library] )

    def need_qt_basics(self,env):
        self.add_library(env, 'Qt5Widgets')
        self.add_library(env, 'Qt5Gui')
        self.add_library(env, 'Qt5Core')
        self.add_library(env, 'Qt5PrintSupport')
        self.add_library(env, 'Qt5DBus')
        self.add_library(env, 'Qt5Multimedia')
        self.add_library(env, 'Qt5MultimediaWidgets')
        self.add_library(env, 'Qt5OpenGL')
        self.add_library(env, 'Qt5Network')

    def need_qt_opengl(self,env):
        self.add_library(env, 'Qt5OpenGL')

    def need_qt_test(self,env):
        self.add_library(env, 'Qt5Text')

    def need_qt_xml(self,env):
        self.add_library(env, 'Qt5Xml')

    def publish_all_libs_to_staging(self, env):
        # We're keeping track of which libs
        # we've added so far to avoid breaking SCons by trying to install two identical
        # libs from different sources into the same target.
        env.SetDefault(STAGED_QT_LIBS = [])
        staged_libs = env['STAGED_QT_LIBS']
        qt_libs = env.Glob( env['QT_DIR'] + '/lib/*.dylib' )

        results = []

        for lib in qt_libs:
            if ( False == os.path.islink( str(lib) ) ) and ( lib.name not in staged_libs ):
                results += env.Install( '$STAGING_DIR', lib )
                env.AppendUnique(STAGED_QT_LIBS = lib.name)

        qt_plugins_platforms = env.Glob( env['QT_DIR'] + '/plugins/platforms/*.dylib' )
        qt_plugins_imgformats = env.Glob( env['QT_DIR'] + '/plugins/imageformats/*.dylib')
        qt_plugins_audio = env.Glob( env['QT_DIR'] + '/plugins/audio/*.dylib' )
        qt_plugins_mediaservice = env.Glob( env['QT_DIR'] + '/plugins/mediaservice/*.dylib' )
        for lib in qt_plugins_platforms:
            results += env.Install( env.subst('$STAGING_DIR/') + env['APP_BUNDLE_NAME'] + '.app/Contents/PlugIns/platforms/', lib )

        for lib in qt_plugins_imgformats:
            results += env.Install( env.subst('$STAGING_DIR/') + env['APP_BUNDLE_NAME'] + '.app/Contents/PlugIns/imageformats/', lib )

        for lib in qt_plugins_audio:
            results += env.Install( env.subst('$STAGING_DIR/') + env['APP_BUNDLE_NAME'] + '.app/Contents/PlugIns/audio/', lib )

        for lib in qt_plugins_mediaservice:
            results += env.Install( env.subst('$STAGING_DIR/') + env['APP_BUNDLE_NAME'] + '.app/Contents/PlugIns/mediaservice/', lib )

        qt_conf = env.Install( env.subst('$STAGING_DIR/') + env['APP_BUNDLE_NAME'] + '.app/Contents/Resources/', env.Glob( env['QT_DIR'] + '/qt.conf' ) )
        results += qt_conf

        return results

class CedrusQtSettingsWin32:
    def _use_qt_include_paths(self, env):

        cxxflags = [
            '/I' + env['QT_DIR'] + '/include/',
            '/I' + env['QT_DIR'] + '/include/QtCore/',
            '/I' + env['QT_DIR'] + '/include/QtGui/',
            '/I' + env['QT_DIR'] + '/include/QtWidgets/',
			'/I' + env['QT_DIR'] + '/include/QtMultimedia/',
			'/I' + env['QT_DIR'] + '/include/QtMultimediaWidgets/',
            ]

        lib_path = [ env['QT_DIR'] + '/win32/final-lib/' ]

        env.AppendUnique( CXXFLAGS = cxxflags,
                          LIBPATH = lib_path,
                          CPPDEFINES = ['QT_NO_KEYWORDS'] )

        if env['BUILD_TYPE'] == 'opt':
            env.AppendUnique( CPPDEFINES = ['QT_NO_DEBUG_OUTPUT'] )

    def add_library(self, env, library, num_suffix = '' ):
        self._use_qt_include_paths(env)

        if env['BUILD_TYPE'] == 'opt':
            library += num_suffix
        elif env['BUILD_TYPE'] == 'dbg':
            library += 'd' + num_suffix

        env.AppendUnique( LIBS = [library] )

    def _copy_plugin_but_no_linker(self, env, single_lib):

        pass # we seem to not need the _copy_plugin_but_no_linker. publish_all_libs_to_staging is good enough on win32

    def need_qt_basics(self,env):
        self.add_library(env, 'Qt5Widgets')
        self.add_library(env, 'Qt5Gui')
        self.add_library(env, 'Qt5Core')
        self.add_library(env, 'QtMultimedia')
        self.add_library(env, 'QtMultimediaWidgets')
        self.add_library(env, 'libEGL')
        self.add_library(env, 'libGLESv2')

    def need_qt_opengl(self,env):
        self.add_library(env, 'Qt5OpenGL')

    def need_qt_test(self,env):
        self.add_library(env, 'Qt5Text')

    def need_qt_xml(self,env):
        self.add_library(env, 'Qt5Xml')

    def publish_all_libs_to_staging(self, env):
        wild_card = '*d.dll' if env['BUILD_TYPE'] == 'dbg' else '*.dll'
        qt_libs = env.Glob( env['QT_DIR'] + '/bin/' + wild_card )

        results = []

        for lib in qt_libs:
            results += env.Install( '$STAGING_DIR', lib )

        qt_plugins_platforms = env.Glob( env['QT_DIR'] + '/plugins/platforms/' + wild_card )
        qt_plugins_imgformats = env.Glob( env['QT_DIR'] + '/plugins/imageformats/' + wild_card )
        qt_plugins_audio = env.Glob( env['QT_DIR'] + '/plugins/audio/' + wild_card )
        qt_plugins_mediaservice = env.Glob( env['QT_DIR'] + '/plugins/mediaservice/' + wild_card )

        for lib in qt_plugins_platforms:
            results += env.Install( '$STAGING_DIR' + '/platforms/', lib )

        for lib in qt_plugins_imgformats:
            results += env.Install( '$STAGING_DIR' + '/imageformats/', lib )

        for lib in qt_plugins_audio:
            results += env.Install( '$STAGING_DIR' + '/audio/', lib )

        for lib in qt_plugins_mediaservice:
            results += env.Install( '$STAGING_DIR' + '/mediaservice/', lib )

        qt_conf = env.Install( '$STAGING_DIR', env.Glob( env['QT_DIR'] + '/qt.conf' ) )
        results += qt_conf

        return results
