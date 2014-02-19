import os
from SCons.Script import *
import platform

class CedrusQtSettings:
    def __init__(self, env, project_app_name):
        if sys.platform == 'win32':
            self.impl = CedrusQtSettingsWin32(env, project_app_name)
        elif sys.platform == 'darwin':
            self.impl = CedrusQtSettingsMac(env, project_app_name)
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
    def __init__(self, env, project_app_name):

        self.app_name = project_app_name


    def _use_qt_include_paths(self, env):

        # macosx/include  QT_BINARIES_REPO
        cxxflags = [
            '-isystem'+os.getenv('QT_BINARIES_REPO','')+'/macosx/include/',
            '-isystem'+os.getenv('QT_BINARIES_REPO','')+'/macosx/include/QtCore/',
            '-isystem'+os.getenv('QT_BINARIES_REPO','')+'/macosx/include/QtGui/',
            '-isystem'+os.getenv('QT_BINARIES_REPO','')+'/macosx/include/QtOpenGL/',
            '-isystem'+os.getenv('QT_BINARIES_REPO','')+'/macosx/include/QtOpenGLExtensions/',
            '-isystem'+os.getenv('QT_BINARIES_REPO','')+'/macosx/include/QtPlatformSupport/',
            '-isystem'+os.getenv('QT_BINARIES_REPO','')+'/macosx/include/QtPrintSupport/',
            '-isystem'+os.getenv('QT_BINARIES_REPO','')+'/macosx/include/QtSensors/',
            '-isystem'+os.getenv('QT_BINARIES_REPO','')+'/macosx/include/QtSvg/',
            '-isystem'+os.getenv('QT_BINARIES_REPO','')+'/macosx/include/QtTest/',
            '-isystem'+os.getenv('QT_BINARIES_REPO','')+'/macosx/include/QtWidgets/',
            '-isystem'+os.getenv('QT_BINARIES_REPO','')+'/macosx/include/QtXml/',
            ]

        lib_path = [
            os.getenv('QT_BINARIES_REPO','')+'/macosx/final-lib/',
            ]

        env.AppendUnique( CXXFLAGS = cxxflags,
                          LIBPATH = lib_path, )

    def add_library(self, env, library, num_suffix = '.5.1.1' ):

        self._use_qt_include_paths(env)

        if env['BUILD_TYPE'] == 'opt':
            library += num_suffix

        if env['BUILD_TYPE'] == 'dbg':
            library += '_debug' + num_suffix

        env.AppendUnique( LIBS = [library] )


    def _copy_plugin_but_no_linker(self, env, single_lib):

        suffix = ''
        if env['BUILD_TYPE'] == 'dbg':
            suffix += '_debug'

        staging_lib = str( env.subst('$STAGING_DIR') + '/lib' + str(single_lib) + suffix + env['SHLIBSUFFIX'] )

        mac_app_bundle_contents_dir = env.subst('$STAGING_DIR') + '/' + self.app_name + '.app/Contents/MacOS/'

        qt_plugins = env.Install(
                mac_app_bundle_contents_dir,
                staging_lib
                )

        # without the next line, SCons was just ignoring my 'env.Install' directive on these libraries
        env.Depends( self.app_name, qt_plugins )


    def _add_base_plugins(self,env):
        self._copy_plugin_but_no_linker(env, 'cocoaprintersupport')
        self._copy_plugin_but_no_linker(env, 'qcocoa')
        self._copy_plugin_but_no_linker(env, 'qgif')
        self._copy_plugin_but_no_linker(env, 'qico')
        self._copy_plugin_but_no_linker(env, 'qjpeg')
        self._copy_plugin_but_no_linker(env, 'qminimal')
        self._copy_plugin_but_no_linker(env, 'qoffscreen')
        self._copy_plugin_but_no_linker(env, 'qtaccessiblewidgets')

    def need_qt_basics(self,env):
        self._add_base_plugins(env)
        self.add_library(env, 'Qt5Widgets')
        self.add_library(env, 'Qt5Gui')
        self.add_library(env, 'Qt5Core')
        self.add_library(env, 'Qt5PrintSupport')

    def need_qt_opengl(self,env):
        self.add_library(env, 'Qt5OpenGL')

    def need_qt_sensors(self,env):
        self._copy_plugin_but_no_linker(env, 'qtsensorgestures_plugin')
        self._copy_plugin_but_no_linker(env, 'qtsensorgestures_shakeplugin')
        self._copy_plugin_but_no_linker(env, 'qtsensors_dummy')
        self._copy_plugin_but_no_linker(env, 'qtsensors_generic')
        self.add_library(env, 'Qt5Sensors')

    def need_qt_svg(self,env):
        self._copy_plugin_but_no_linker(env, 'qsvg')
        self._copy_plugin_but_no_linker(env, 'qsvgicon')
        self.add_library(env, 'Qt5Svg')

    def need_qt_test(self,env):
        self.add_library(env, 'Qt5Text')

    def need_qt_xml(self,env):
        self.add_library(env, 'Qt5Xml')


    def publish_all_libs_to_staging(self, env):

        want_debug_libs = False

        if env['BUILD_TYPE'] == 'dbg':
            want_debug_libs = True

        qt_libs = env.Glob( os.getenv('QT_BINARIES_REPO','')+'/macosx/final-lib/*dylib' )

        results = []

        for lib in qt_libs:
            is_a_debug_lib = ('debug' in str(lib) )
            not_symlink = (False == os.path.islink( str(lib) ) )

            if (want_debug_libs == is_a_debug_lib) and not_symlink:
                results += env.Install( '$STAGING_DIR', lib )

        return results



class CedrusQtSettingsWin32:
    def __init__(self, env, project_app_name):

        self.app_name = project_app_name


    def _use_qt_include_paths(self, env):

        cxxflags = [
            '/I'+os.getenv('QT_BINARIES_REPO','')+'/win32/include/',
            '/I'+os.getenv('QT_BINARIES_REPO','')+'/win32/include/QtANGLE/', # this replaces QtOpenGL on windows
            '/I'+os.getenv('QT_BINARIES_REPO','')+'/win32/include/QtCore/',
            '/I'+os.getenv('QT_BINARIES_REPO','')+'/win32/include/QtGui/',
            #'/I'+os.getenv('QT_BINARIES_REPO','')+'/win32/include/QtOpenGL/',  # no! we use QtANGLE instead, at least for now
            '/I'+os.getenv('QT_BINARIES_REPO','')+'/win32/include/QtPlatformSupport/',
            '/I'+os.getenv('QT_BINARIES_REPO','')+'/win32/include/QtPrintSupport/',
            '/I'+os.getenv('QT_BINARIES_REPO','')+'/win32/include/QtSensors/',
            '/I'+os.getenv('QT_BINARIES_REPO','')+'/win32/include/QtSvg/',
            '/I'+os.getenv('QT_BINARIES_REPO','')+'/win32/include/QtTest/',
            '/I'+os.getenv('QT_BINARIES_REPO','')+'/win32/include/QtWidgets/',
            '/I'+os.getenv('QT_BINARIES_REPO','')+'/win32/include/QtXml/',
            ]

        lib_path = [
            os.getenv('QT_BINARIES_REPO','')+'/win32/final-lib/',
            ]

        env.AppendUnique( CXXFLAGS = cxxflags,
                          LIBPATH = lib_path, )

    def add_library(self, env, library, num_suffix = '' ):

        self._use_qt_include_paths(env)

        if env['BUILD_TYPE'] == 'opt':
            library += num_suffix

        if env['BUILD_TYPE'] == 'dbg':
            library += 'd' + num_suffix

        env.AppendUnique( LIBS = [library] )


    def _copy_plugin_but_no_linker(self, env, single_lib):

        pass # we seem to not need the _copy_plugin_but_no_linker. publish_all_libs_to_staging is good enough on win32



    def _add_base_plugins(self,env):
        self._copy_plugin_but_no_linker(env, 'windowsprintersupport')
        self._copy_plugin_but_no_linker(env, 'qwindows')
        self._copy_plugin_but_no_linker(env, 'qgif')
        self._copy_plugin_but_no_linker(env, 'qico')
        self._copy_plugin_but_no_linker(env, 'qjpeg')
        self._copy_plugin_but_no_linker(env, 'qminimal')
        #self._copy_plugin_but_no_linker(env, 'qmng')        # does not exist on win32?
        self._copy_plugin_but_no_linker(env, 'qoffscreen')
        self._copy_plugin_but_no_linker(env, 'qtaccessiblewidgets')
        #self._copy_plugin_but_no_linker(env, 'qtga')        # does not exist on win32?
        #self._copy_plugin_but_no_linker(env, 'qtiff')       # does not exist on win32?
        #self._copy_plugin_but_no_linker(env, 'qwbmp')       # does not exist on win32?

    def need_qt_basics(self,env):
        self._add_base_plugins(env)
        self.add_library(env, 'Qt5Widgets')
        self.add_library(env, 'Qt5Gui')
        self.add_library(env, 'Qt5Core')
        self.add_library(env, 'Qt5PrintSupport')

    def need_qt_opengl(self,env):
        self.add_library(env, 'Qt5OpenGL')

    # in our Cedrus build, this was not (yet) possible on windows...
    #def need_qt_sensors(self,env):
    #    self._copy_plugin_but_no_linker(env, 'qtsensorgestures_plugin')
    #    self._copy_plugin_but_no_linker(env, 'qtsensorgestures_shakeplugin')
    #    self._copy_plugin_but_no_linker(env, 'qtsensors_dummy')
    #    self._copy_plugin_but_no_linker(env, 'qtsensors_generic')
    #    self.add_library(env, 'Qt5Sensors')

    # in our Cedrus build, this was not (yet) possible on windows...
    #def need_qt_svg(self,env):
    #    self._copy_plugin_but_no_linker(env, 'qsvg')
    #    self._copy_plugin_but_no_linker(env, 'qsvgicon')
    #    self.add_library(env, 'Qt5Svg')

    def need_qt_test(self,env):
        self.add_library(env, 'Qt5Text')

    def need_qt_xml(self,env):
        self.add_library(env, 'Qt5Xml')


    def publish_all_libs_to_staging(self, env):

        want_debug_libs = False

        if env['BUILD_TYPE'] == 'dbg':
            want_debug_libs = True

        qt_libs = env.Glob( os.getenv('QT_BINARIES_REPO','')+'/win32/final-lib/*dll' )
        qt_libs += env.Glob( os.getenv('QT_BINARIES_REPO','')+'/win32/final-lib/*pdb' )

        results = []

        for lib in qt_libs:
            is_a_debug_lib = ('d.' in str(lib) )

            if want_debug_libs == is_a_debug_lib:
                results += env.Install( '$STAGING_DIR', lib )

        return results


