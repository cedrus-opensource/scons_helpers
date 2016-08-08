import os
from SCons.Script import *
import platform
from distutils.version import LooseVersion, StrictVersion

class CedrusWxWidgetsSettings:
    def __init__(self, env ):
        wx_ver = env['WX_VERSION']

        if GetOption('build_mode') == 'default':
            build_mode = 'dbg'
        else:
            build_mode = GetOption('build_mode')

        if build_mode == 'dbg':
            self.debug = True
        else:
            self.debug = False

        if sys.platform == 'win32':
            self.impl = CedrusWxWidgetsWindows(env, self.debug, wx_ver)
        elif sys.platform == 'darwin':
            self.impl = CedrusWxWidgetsMac(env, self.debug, wx_ver)
        elif sys.platform == 'linux2':
            self.impl = CedrusWxWidgetsLinux(env, self.debug, wx_ver)
        else:
            raise ValueError('Unknown Operating System')

        if StrictVersion(wx_ver) >= StrictVersion('2.9'):
            env.AppendUnique( CPPDEFINES = [ 'WX_PREPROC_FLAG=2930' ] )

        self.env = env

    def publish_all_libs_to_staging(self):
        return self.impl.publish_all_libs_to_staging(self.env)

    def need_core(self):
        self.impl.need_core(self.env)

    def need_net(self):
        self.impl.need_net(self.env)

    def need_xml(self):
        self.impl.need_xml(self.env)

    def need_adv(self):
        self.impl.need_adv(self.env)

    def need_aui(self):
        self.impl.need_aui(self.env)

    def need_html(self):
        self.impl.need_html(self.env)

    def need_qa(self):
        self.impl.need_qa(self.env)

    def need_richtext(self):
        self.impl.need_richtext(self.env)

    def need_xrc(self):
        self.impl.need_xrc(self.env)

class CedrusWxWidgetsMac:

    def __init__(self, env, debug, wx_ver):
        self.debug = debug

        self.mac_str = 'macu'
        self.carb_coco_str = 'base_carbonu'

        self.wx_ver = wx_ver
        self.wx_ver_no_dots = wx_ver.replace('.','')

        if StrictVersion(wx_ver) >= StrictVersion('2.9'):
            self.mac_str = 'osx_cocoau'
            self.carb_coco_str = 'baseu'

        self._always_need_base(env)
        self._proceed_with_include_paths(env)

    def _proceed_with_include_paths(self, env):
        # set cxxflags for wxWidgets
        cxxflags = []
        if self.debug:
            if StrictVersion(wx_ver) == StrictVersion('2.9'):
                cxxflags = [
                    '-isystem'+os.getenv('WXWIN_SL','')+'/include/',
                    '-isystem'+os.getenv('WXWIN_SL','')+'/built_libs/lib/wx/include/mac-unicode-debug-'+env['WX_VERSION']+'-i386'
                    ]

            else: # this 'else' used to be for testing 2.8.10, but now it's for 2.9 !
                cxxflags = [
                    '-isystem'+os.getenv('WXWIN_29','')+'/built_libs/include/wx-'+env['WX_VERSION'],
                    '-isystem'+os.getenv('WXWIN_29','')+'/built_libs/lib/wx/include/osx_cocoa-unicode-'+env['WX_VERSION']
                    ]
        else:
            if StrictVersion(wx_ver) == StrictVersion('2.8'):
                cxxflags = [
                    '-isystem'+os.getenv('WXWIN_SL','')+'/include/',
                    '-isystem'+os.getenv('WXWIN_SL','')+'/built_libs/lib/wx/include/mac-unicode-release-'+env['WX_VERSION']+'-i386'
                    ]
            else:
                cxxflags = [
                    '-isystem'+os.getenv('WXWIN_29','')+'/built_libs/include/wx-'+env['WX_VERSION'],
                    '-isystem'+os.getenv('WXWIN_29','')+'/built_libs/lib/wx/include/osx_cocoa-unicode-'+env['WX_VERSION']
                    ]

        env.AppendUnique( CXXFLAGS = cxxflags )

    def _always_need_base(self, env):
        if self.debug:
            libname = 'wx_' + self.carb_coco_str + 'd-' + self.wx_ver_no_dots
        else:
            libname = 'wx_' + self.carb_coco_str + '-' + self.wx_ver_no_dots 

        env.AppendUnique(LIBS=[libname])

        if StrictVersion(wx_ver) == StrictVersion('2.8'):
            lib_path = [
                os.getenv('WXWIN_SL','')+'/lib/',
                ]
            lib_path.append( os.getenv('WXWIN_SL','') + '/built_libs/lib/' )
        else: # this 'else' used to be for testing 2.8.10, but now it's for 2.9 !
            lib_path = []
            lib_path.append( os.getenv('WXWIN_29','') + '/built_libs/lib/' )

        env.AppendUnique( LIBPATH = lib_path,
                          LIBS=[libname])

    def publish_all_libs_to_staging(self, env):
        if StrictVersion(wx_ver) == StrictVersion('2.8'):
            wxlibs = env.Glob( os.getenv('WXWIN_SL','')+'/built_libs/lib/*.dylib' )

        else: # this 'else' used to be for testing 2.8.10, but now it's for 2.9 !
            if self.debug:
                wxlibs = env.Glob( os.getenv('WXWIN_29','')+'/built_libs/lib/*ud[_-]*.dylib' )
            else:
                wxlibs = env.Glob( os.getenv('WXWIN_29','')+'/built_libs/lib/*u[_-]*.dylib' )

        results = []

        for lib in wxlibs:
            results += env.Install( '$STAGING_DIR', lib )

        return results

    def need_core(self, env):
        self._always_need_base(env)
        self._proceed_with_include_paths(env)

        if self.debug:
            libname = 'wx_' + self.mac_str + 'd_core-' + self.wx_ver_no_dots
        else:
            libname = 'wx_' + self.mac_str + '_core-'+ self.wx_ver_no_dots

        env.AppendUnique(LIBS=[libname])

    def need_net(self, env):
        self._always_need_base(env)
        self._proceed_with_include_paths(env)

        if self.debug:
            libname = 'wx_' + self.carb_coco_str + 'd_net-' + self.wx_ver_no_dots
        else:
            libname = 'wx_' + self.carb_coco_str + '_net-' + self.wx_ver_no_dots

        env.AppendUnique(LIBS=[libname])

    def need_xml(self, env):
        self._always_need_base(env)
        self._proceed_with_include_paths(env)

        if self.debug:
            libname = 'wx_' + self.carb_coco_str + 'd_xml-' + self.wx_ver_no_dots
        else:
            libname = 'wx_' + self.carb_coco_str + '_xml-' + self.wx_ver_no_dots

        env.AppendUnique(LIBS=[libname])

    def need_adv(self, env):
        self._always_need_base(env)
        self._proceed_with_include_paths(env)

        if self.debug:
            libname = 'wx_' + self.mac_str + 'd_adv-' + self.wx_ver_no_dots
        else:
            libname = 'wx_' + self.mac_str + '_adv-' + self.wx_ver_no_dots

        env.AppendUnique(LIBS=[libname])

    def need_aui(self, env):
        self._always_need_base(env)
        self._proceed_with_include_paths(env)

        if self.debug:
            libname = 'wx_' + self.mac_str + 'd_aui-' + self.wx_ver_no_dots
        else:
            libname = 'wx_' + self.mac_str + '_aui-' + self.wx_ver_no_dots

        env.AppendUnique(LIBS=[libname])

    def need_html(self, env):
        self._always_need_base(env)
        self._proceed_with_include_paths(env)

        if self.debug:
            libname = 'wx_' + self.mac_str + 'd_html-' + self.wx_ver_no_dots
        else:
            libname = 'wx_' + self.mac_str + '_html-' + self.wx_ver_no_dots

        env.AppendUnique(LIBS=[libname])

    def need_qa(self, env):
        self._always_need_base(env)
        self._proceed_with_include_paths(env)

        if self.debug:
            libname = 'wx_' + self.mac_str + 'd_qa-' + self.wx_ver_no_dots
        else:
            libname = 'wx_' + self.mac_str + '_qa-' + self.wx_ver_no_dots

        env.AppendUnique(LIBS=[libname])

    def need_richtext(self, env):
        self._always_need_base(env)
        self._proceed_with_include_paths(env)

        if self.debug:
            libname = 'wx_' + self.mac_str + 'd_richtext-' + self.wx_ver_no_dots
        else:
            libname = 'wx_' + self.mac_str + '_richtext-' + self.wx_ver_no_dots

        env.AppendUnique(LIBS=[libname])

    def need_xrc(self, env):
        self._always_need_base(env)
        self._proceed_with_include_paths(env)

        if self.debug:
            libname = 'wx_' + self.mac_str + 'd_xrc-' + self.wx_ver_no_dots
        else:
            libname = 'wx_' + self.mac_str + '_xrc-' + self.wx_ver_no_dots

        env.AppendUnique(LIBS=[libname])

class CedrusWxWidgetsWindows:
    def __init__(self, env, debug, wx_ver):
        self.debug = debug
        self.wx_ver = wx_ver    
        self.wx_ver_no_dots = wx_ver.replace('.','')

        if self.debug:
            libname = 'wxbase' + self.wx_ver_no_dots +'ud'
        else:
            libname = 'wxbase' + self.wx_ver_no_dots +'u'

        self.vc_dir = 'vc_dll_vc10'
        if env['MSVC_VERSION'] == '14.0' :
            self.vc_dir = 'vc_dll_vc14'

        env.AppendUnique(LIBS=[libname])

        cxxflags = []
        lib_path = []
        if debug:
            if StrictVersion(wx_ver) == StrictVersion('2.8'):
                cxxflags = [
                    '/I'+os.getenv('WXWIN_SL','')+'/lib/' + self.vc_dir + '/mswud/',
                    '/I'+os.getenv('WXWIN_SL','')+'/include/',
                    ]
                lib_path = [
                    os.getenv('WXWIN_SL','')+'/lib/' + self.vc_dir,
                    ]
            else:
                cxxflags = [
                    '/I'+ env['WX_DIR'] + '/lib/' + self.vc_dir + '/mswud/',
                    '/I'+ env['WX_DIR'] + '/include/',
                    ]
                lib_path = [
                    env['WX_DIR'] + '/lib/' + self.vc_dir,
                    ]
        else:
            if StrictVersion(wx_ver) == StrictVersion('2.8'):
                cxxflags = [
                    '/I'+os.getenv('WXWIN_SL','')+'/lib/' + self.vc_dir + '/mswu/',
                    '/I'+os.getenv('WXWIN_SL','')+'/include/',
                    ]
                lib_path = [
                    os.getenv('WXWIN_SL','')+'/lib/' + self.vc_dir ,
                    ]
            else:
                cxxflags = [
                    '/I' + env['WX_DIR'] + '/lib/' + self.vc_dir + '/mswu/',
                    '/I' + env['WX_DIR'] + '/include/',
                    ]
                lib_path = [
                    env['WX_DIR'] + '/lib/' + self.vc_dir,
                    ]

        env.AppendUnique( CXXFLAGS = cxxflags,
                    LIBPATH = lib_path,
                    LIBS = [libname])

    def publish_all_libs_to_staging(self, env):
        if StrictVersion(self.wx_ver) == StrictVersion("2.8"):
                wxlibs = env.Glob( os.getenv('WXWIN_SL','')+'/lib/' + self.vc_dir + '/*.dll' )
                wxlibs += env.Glob( os.getenv('WXWIN_SL','')+'/lib/' + self.vc_dir + '/*.pdb' )
        else:
            if self.debug:
                wxlibs = env.Glob( env['WX_DIR'] + '/lib/' + self.vc_dir + '/*ud[_-]*.dll' )
                wxlibs += env.Glob( env['WX_DIR'] + '/lib/' + self.vc_dir + '/*ud[_-]*.pdb' )
            else:
                wxlibs = env.Glob( env['WX_DIR'] + '/lib/' + self.vc_dir + '/*u[_-]*.dll' )
                wxlibs += env.Glob( env['WX_DIR'] + '/lib/' + self.vc_dir + '/*u[_-]*.pdb' )

        results = []

        for lib in wxlibs:
            name_parts = os.path.splitext(lib.name)
            lib_basename = name_parts[0]
            lib_basename = lib_basename.replace('_vcCedrus','')
            results += env.Install( '$STAGING_DIR', lib )

        return results

    def need_core(self, env):
        if self.debug:
            libname = 'wxmsw' + self.wx_ver_no_dots + 'ud_core'
        else:
            libname = 'wxmsw' + self.wx_ver_no_dots + 'u_core'

        env.AppendUnique(LIBS=[libname])

    def need_net(self, env):
        if self.debug:
            libname = 'wxbase' + self.wx_ver_no_dots + 'ud_net'
        else:
            libname = 'wxbase' + self.wx_ver_no_dots + 'u_net'

        env.AppendUnique(LIBS=[libname])

    def need_xml(self, env):
        if self.debug:
            libname = 'wxbase' + self.wx_ver_no_dots + 'ud_xml'
        else:
            libname = 'wxbase' + self.wx_ver_no_dots + 'u_xml'

        env.AppendUnique(LIBS=[libname])

    def need_adv(self, env):
        if self.debug:
            libname = 'wxmsw' + self.wx_ver_no_dots + 'ud_adv'
        else:
            libname = 'wxmsw' + self.wx_ver_no_dots + 'u_adv'

        env.AppendUnique(LIBS=[libname])

    def need_aui(self, env):
        if self.debug:
            libname = 'wxmsw' + self.wx_ver_no_dots + 'ud_aui'
        else:
            libname = 'wxmsw' + self.wx_ver_no_dots + 'u_aui'

        env.AppendUnique(LIBS=[libname])

    def need_html(self, env):
        if self.debug:
            libname = 'wxmsw' + self.wx_ver_no_dots + 'ud_html'
        else:
            libname = 'wxmsw' + self.wx_ver_no_dots + 'u_html'

        env.AppendUnique(LIBS=[libname])

    def need_qa(self, env):
        if self.debug:
            libname = 'wxmsw' + self.wx_ver_no_dots + 'ud_qa'
        else:
            libname = 'wxmsw' + self.wx_ver_no_dots + 'u_qa'

        env.AppendUnique(LIBS=[libname])

    def need_richtext(self, env):
        if self.debug:
            libname = 'wxmsw' + self.wx_ver_no_dots + 'ud_richtext'
        else:
            libname = 'wxmsw' + self.wx_ver_no_dots + 'u_richtext'

        env.AppendUnique(LIBS=[libname])

    def need_xrc(self, env):
        if self.debug:
            libname = 'wxmsw' + self.wx_ver_no_dots + 'ud_xrc'
        else:
            libname = 'wxmsw' + self.wx_ver_no_dots + 'u_xrc'

        env.AppendUnique(LIBS=[libname])

class CedrusWxWidgetsLinux:
    def __init__(self, env, debug, wx_ver):
        self.debug = debug
        self.wx_ver = wx_ver
        self.wx_ver_no_dots = wx_ver.replace('.','')

        if self.debug:
            libname = 'wx_baseud-' + self.wx_ver_no_dots
        else:
            libname = 'wx_baseu-' + self.wx_ver_no_dots

        env.AppendUnique(LIBS=[libname])

        cxxflags = []
        if debug:
            cxxflags = [
                '-isystem/usr/include/wx-' + wx_ver +'/',
                '-isystem/usr/lib/x86_64-linux-gnu/wx/include/base-unicode-release-' + wx_ver +'/',
                ]
        else:
            cxxflags = [
                '-isystem/usr/include/wx-'+env['WX_VERSION']+'/',
                '-isystem/usr/lib/x86_64-linux-gnu/wx/include/base-unicode-release-' + wx_ver +'/',
                ]

        lib_path = [
            '/usr/lib/',
            ]

        env.AppendUnique( CXXFLAGS = cxxflags,
                    LIBPATH = lib_path,
                    LIBS = [libname])

    def publish_all_libs_to_staging(self, env):
        return []

    def need_core(self, env):
        if self.debug:
            libname = 'wx_gtk2ud_core-' + self.wx_ver_no_dots
        else:
            libname = 'wx_gtk2u_core-' + self.wx_ver_no_dots

        env.AppendUnique(LIBS=[libname])

    def need_net(self, env):
        if self.debug:
            libname = 'wx_baseud_net-' + self.wx_ver_no_dots
        else:
            libname = 'wx_baseu_net-' + self.wx_ver_no_dots

        env.AppendUnique(LIBS=[libname])

    def need_xml(self, env):
        if self.debug:
            libname = 'wx_baseud_xml-' + self.wx_ver_no_dots
        else:
            libname = 'wx_baseu_xml-' + self.wx_ver_no_dots

        env.AppendUnique(LIBS=[libname])

    def need_adv(self, env):
        if self.debug:
            libname = 'wx_gtk2ud_adv-' + self.wx_ver_no_dots
        else:
            libname = 'wx_gtk2u_adv-' + self.wx_ver_no_dots

        env.AppendUnique(LIBS=[libname])

    def need_aui(self, env):
        if self.debug:
            libname = 'wx_gtk2ud_aui-' + self.wx_ver_no_dots
        else:
            libname = 'wx_gtk2u_aui-' + self.wx_ver_no_dots

        env.AppendUnique(LIBS=[libname])

    def need_html(self, env):
        if self.debug:
            libname = 'wx_gtk2ud_html-' + self.wx_ver_no_dots
        else:
            libname = 'wx_gtk2u_html-' + self.wx_ver_no_dots

        env.AppendUnique(LIBS=[libname])

    def need_qa(self, env):
        if self.debug:
            libname = 'wx_gtk2ud_qa-' + self.wx_ver_no_dots
        else:
            libname = 'wx_gtk2u_qa-' + self.wx_ver_no_dots

        env.AppendUnique(LIBS=[libname])

    def need_richtext(self, env):
        if self.debug:
            libname = 'wx_gtk2ud_richtext-' + self.wx_ver_no_dots
        else:
            libname = 'wx_gtk2u_richtext-' + self.wx_ver_no_dots

        env.AppendUnique(LIBS=[libname])

    def need_xrc(self, env):
        if self.debug:
            libname = 'wx_gtk2ud_xrc-' + self.wx_ver_no_dots
        else:
            libname = 'wx_gtk2u_xrc-' + self.wx_ver_no_dots

        env.AppendUnique(LIBS=[libname])
