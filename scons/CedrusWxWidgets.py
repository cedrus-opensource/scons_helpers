import os
from SCons.Script import *
import platform


class CedrusWxWidgetsSettings:
    def __init__(self, env ):
        wxVersion = env[ 'WX_VERSION' ]#expecting either 2.8 or 2.9

        if GetOption('build_mode') == 'default':
            build_mode = 'dbg'
        else:
            build_mode = GetOption('build_mode')

        if build_mode == 'dbg':
            self.debug = True
        else:
            self.debug = False

        if sys.platform == 'win32':
            self.impl = CedrusWxWidgetsWindows(env, self.debug, wxVersion)
        elif sys.platform == 'darwin':
            self.impl = CedrusWxWidgetsMac(env, self.debug, wxVersion)
        elif sys.platform == 'linux2':
            self.impl = CedrusWxWidgetsLinux(env, self.debug, wxVersion)
        else:
            raise ValueError('Unknown Operating System')

        if env['WX_VERSION'] == '2.9':
            env.AppendUnique( CPPDEFINES = [ 'WX_PREPROC_FLAG=2930' ] )

        self.env = env
        self.impl.wx_version_num = wxVersion

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

    def __init__(self, env, debug, wxVersion):
        self.debug = debug

        self.mac_str = 'macu'
        self.carb_coco_str = 'base_carbonu'

        if wxVersion == '2.9':
            self.mac_str = 'osx_cocoau'
            self.carb_coco_str = 'baseu'

        self.wx_version_num = wxVersion
        self._always_need_base(env)
        self._proceed_with_include_paths(env)


    def _proceed_with_include_paths(self, env):
        # set cxxflags for wxWidgets
        cxxflags = []
        if self.debug:
            if self.wx_version_num == '2.8':
                if not platform.mac_ver()[0].startswith('10.4'):
                    cxxflags = [
                        '-isystem'+os.getenv('WXWIN_SL','')+'/include/',
                        '-isystem'+os.getenv('WXWIN_SL','')+'/built_libs/lib/wx/include/mac-unicode-debug-'+env['WX_VERSION']+'-i386'
                        ]
                else:
                    cxxflags = [
                        '-I'+os.getenv('WXWIN_SL','')+'/include/',
                        '-I'+os.getenv('WXWIN_SL','')+'/built_libs/lib/wx/include/mac-unicode-debug-'+env['WX_VERSION']+'-i386',
                        ]
            else: # this 'else' used to be for testing 2.8.10, but now it's for 2.9 !
                if not platform.mac_ver()[0].startswith('10.4'):
                    cxxflags = [
                        '-isystem'+os.getenv('WXWIN_29','')+'/include/',
                        '-isystem'+os.getenv('WXWIN_29','')+'/built_libs/lib/wx/include/osx_cocoa-unicode-'+env['WX_VERSION']
                        ]
                else:
                    cxxflags = [
                        '-I'+os.getenv('WXWIN_29','')+'/include/',
                        '-I'+os.getenv('WXWIN_29','')+'/built_libs/lib/wx/include/osx_cocoa-unicode-'+env['WX_VERSION']
                        ]
        else:
            if self.wx_version_num == '2.8':
                if not platform.mac_ver()[0].startswith('10.4'):
                    cxxflags = [
                        '-isystem'+os.getenv('WXWIN_SL','')+'/include/',
                        '-isystem'+os.getenv('WXWIN_SL','')+'/built_libs/lib/wx/include/mac-unicode-release-'+env['WX_VERSION']+'-i386'
                        ]
                else:
                    cxxflags = [
                        '-I'+os.getenv('WXWIN_SL','')+'/include/',
                        '-I'+os.getenv('WXWIN_SL','')+'/built_libs/lib/wx/include/mac-unicode-release-'+env['WX_VERSION']+'-i386'
                        ]
            else:
                if not platform.mac_ver()[0].startswith('10.4'):
                    cxxflags = [
                        '-isystem'+os.getenv('WXWIN_29','')+'/include/',
                        '-isystem'+os.getenv('WXWIN_29','')+'/built_libs/lib/wx/include/osx_cocoa-unicode-'+env['WX_VERSION']
                        ]
                else:
                    cxxflags = [
                        '-I'+os.getenv('WXWIN_29','')+'/include/',
                        '-I'+os.getenv('WXWIN_29','')+'/built_libs/lib/wx/include/osx_cocoa-unicode-'+env['WX_VERSION']
                        ]

        env.AppendUnique( CXXFLAGS = cxxflags )


    def _always_need_base(self, env):
        if self.debug:
            libname = 'wx_' + self.carb_coco_str + 'd-'+env['WX_VERSION']
        else:
            libname = 'wx_' + self.carb_coco_str + '-'+env['WX_VERSION']

        env.AppendUnique(LIBS=[libname])

        if self.wx_version_num == '2.8':
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
        if self.wx_version_num == '2.8':
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
            libname = 'wx_' + self.mac_str + 'd_core-'+env['WX_VERSION']
        else:
            libname = 'wx_' + self.mac_str + '_core-'+env['WX_VERSION']

        env.AppendUnique(LIBS=[libname])


    def need_net(self, env):
        self._always_need_base(env)
        self._proceed_with_include_paths(env)

        if self.debug:
            libname = 'wx_' + self.carb_coco_str + 'd_net-'+env['WX_VERSION']
        else:
            libname = 'wx_' + self.carb_coco_str + '_net-'+env['WX_VERSION']

        env.AppendUnique(LIBS=[libname])


    def need_xml(self, env):
        self._always_need_base(env)
        self._proceed_with_include_paths(env)

        if self.debug:
            libname = 'wx_' + self.carb_coco_str + 'd_xml-'+env['WX_VERSION']
        else:
            libname = 'wx_' + self.carb_coco_str + '_xml-'+env['WX_VERSION']


        env.AppendUnique(LIBS=[libname])


    def need_adv(self, env):
        self._always_need_base(env)
        self._proceed_with_include_paths(env)

        if self.debug:
            libname = 'wx_' + self.mac_str + 'd_adv-'+env['WX_VERSION']
        else:
            libname = 'wx_' + self.mac_str + '_adv-'+env['WX_VERSION']


        env.AppendUnique(LIBS=[libname])

    def need_aui(self, env):
        self._always_need_base(env)
        self._proceed_with_include_paths(env)

        if self.debug:
            libname = 'wx_' + self.mac_str + 'd_aui-'+env['WX_VERSION']
        else:
            libname = 'wx_' + self.mac_str + '_aui-'+env['WX_VERSION']


        env.AppendUnique(LIBS=[libname])

    def need_html(self, env):
        self._always_need_base(env)
        self._proceed_with_include_paths(env)

        if self.debug:
            libname = 'wx_' + self.mac_str + 'd_html-'+env['WX_VERSION']
        else:
            libname = 'wx_' + self.mac_str + '_html-'+env['WX_VERSION']


        env.AppendUnique(LIBS=[libname])

    def need_qa(self, env):
        self._always_need_base(env)
        self._proceed_with_include_paths(env)

        if self.debug:
            libname = 'wx_' + self.mac_str + 'd_qa-'+env['WX_VERSION']
        else:
            libname = 'wx_' + self.mac_str + '_qa-'+env['WX_VERSION']


        env.AppendUnique(LIBS=[libname])

    def need_richtext(self, env):
        self._always_need_base(env)
        self._proceed_with_include_paths(env)

        if self.debug:
            libname = 'wx_' + self.mac_str + 'd_richtext-'+env['WX_VERSION']
        else:
            libname = 'wx_' + self.mac_str + '_richtext-'+env['WX_VERSION']


        env.AppendUnique(LIBS=[libname])


    def need_xrc(self, env):
        self._always_need_base(env)
        self._proceed_with_include_paths(env)

        if self.debug:
            libname = 'wx_' + self.mac_str + 'd_xrc-'+env['WX_VERSION']
        else:
            libname = 'wx_' + self.mac_str + '_xrc-'+env['WX_VERSION']


        env.AppendUnique(LIBS=[libname])


class CedrusWxWidgetsWindows:
    def __init__(self, env, debug, wxVersion):
        self.debug = debug
        self.wxnum = wxVersion

        if self.debug:
            libname = 'wxbase'+env['WIN_WX_VERSION']+'ud'
        else:
            libname = 'wxbase'+env['WIN_WX_VERSION']+'u'


        env.AppendUnique(LIBS=[libname])

        cxxflags = []
        lib_path = []
        if debug:
            if wxVersion == '2.8':
                if True:
                    cxxflags = [
                        '/I'+os.getenv('WXWIN_SL','')+'/lib/vc_dll_vc10/mswud/',
                        '/I'+os.getenv('WXWIN_SL','')+'/include/',
                        ]
                    lib_path = [
                        os.getenv('WXWIN_SL','')+'/lib/vc_dll_vc10/',
                        ]
            else:
                if True:
                    cxxflags = [
                        '/I'+os.getenv('WXWIN_29','')+'/lib/vc_dll_vc10/mswud/',
                        '/I'+os.getenv('WXWIN_29','')+'/include/',
                        ]
                    lib_path = [
                        os.getenv('WXWIN_29','')+'/lib/vc_dll_vc10',
                        ]
        else:
            if wxVersion == '2.8':
                if True:
                    cxxflags = [
                        '/I'+os.getenv('WXWIN_SL','')+'/lib/vc_dll_vc10/mswu/',
                        '/I'+os.getenv('WXWIN_SL','')+'/include/',
                        ]
                    lib_path = [
                        os.getenv('WXWIN_SL','')+'/lib/vc_dll_vc10/',
                        ]
            else:
                if True:
                    cxxflags = [
                        '/I'+os.getenv('WXWIN_29','')+'/lib/vc_dll_vc10/mswu/',
                        '/I'+os.getenv('WXWIN_29','')+'/include/',
                        ]
                    lib_path = [
                        os.getenv('WXWIN_29','')+'/lib/vc_dll_vc10',
                        ]

        env.AppendUnique( CXXFLAGS = cxxflags,
                    LIBPATH = lib_path,
                    LIBS = [libname])


    def publish_all_libs_to_staging(self, env):
        if self.wxnum == '2.8':
                wxlibs = env.Glob( os.getenv('WXWIN_SL','')+'/lib/vc_dll_vc10/*.dll' )
                wxlibs += env.Glob( os.getenv('WXWIN_SL','')+'/lib/vc_dll_vc10/*.pdb' )
        else:
            if self.debug:
                wxlibs = env.Glob( os.getenv('WXWIN_29','')+'/lib/vc_dll_vc10/*ud[_-]*.dll' )
                wxlibs += env.Glob( os.getenv('WXWIN_29','')+'/lib/vc_dll_vc10/*ud[_-]*.pdb' )
            else:
                wxlibs = env.Glob( os.getenv('WXWIN_29','')+'/lib/vc_dll_vc10/*u[_-]*.dll' )
                wxlibs += env.Glob( os.getenv('WXWIN_29','')+'/lib/vc_dll_vc10/*u[_-]*.pdb' )


        results = []

        for lib in wxlibs:
            name_parts = os.path.splitext(lib.name)
            lib_basename = name_parts[0]
            lib_basename = lib_basename.replace('_vcCedrus','')
            results += env.Install( '$STAGING_DIR', lib )

        return results

    def need_core(self, env):
        if self.debug:
            libname = 'wxmsw'+env['WIN_WX_VERSION']+'ud_core'
        else:
            libname = 'wxmsw'+env['WIN_WX_VERSION']+'u_core'


        env.AppendUnique(LIBS=[libname])


    def need_net(self, env):
        if self.debug:
            libname = 'wxbase'+env['WIN_WX_VERSION']+'ud_net'
        else:
            libname = 'wxbase'+env['WIN_WX_VERSION']+'u_net'


        env.AppendUnique(LIBS=[libname])


    def need_xml(self, env):
        if self.debug:
            libname = 'wxbase'+env['WIN_WX_VERSION']+'ud_xml'
        else:
            libname = 'wxbase'+env['WIN_WX_VERSION']+'u_xml'


        env.AppendUnique(LIBS=[libname])


    def need_adv(self, env):
        if self.debug:
            libname = 'wxmsw'+env['WIN_WX_VERSION']+'ud_adv'
        else:
            libname = 'wxmsw'+env['WIN_WX_VERSION']+'u_adv'


        env.AppendUnique(LIBS=[libname])

    def need_aui(self, env):
        if self.debug:
            libname = 'wxmsw'+env['WIN_WX_VERSION']+'ud_aui'
        else:
            libname = 'wxmsw'+env['WIN_WX_VERSION']+'u_aui'


        env.AppendUnique(LIBS=[libname])


    def need_html(self, env):
        if self.debug:
            libname = 'wxmsw'+env['WIN_WX_VERSION']+'ud_html'
        else:
            libname = 'wxmsw'+env['WIN_WX_VERSION']+'u_html'


        env.AppendUnique(LIBS=[libname])

    def need_qa(self, env):
        if self.debug:
            libname = 'wxmsw'+env['WIN_WX_VERSION']+'ud_qa'
        else:
            libname = 'wxmsw'+env['WIN_WX_VERSION']+'u_qa'


        env.AppendUnique(LIBS=[libname])

    def need_richtext(self, env):
        if self.debug:
            libname = 'wxmsw'+env['WIN_WX_VERSION']+'ud_richtext'
        else:
            libname = 'wxmsw'+env['WIN_WX_VERSION']+'u_richtext'


        env.AppendUnique(LIBS=[libname])


    def need_xrc(self, env):
        if self.debug:
            libname = 'wxmsw'+env['WIN_WX_VERSION']+'ud_xrc'
        else:
            libname = 'wxmsw'+env['WIN_WX_VERSION']+'u_xrc'


        env.AppendUnique(LIBS=[libname])


class CedrusWxWidgetsLinux:
    def __init__(self, env, debug, wxVersion):
        self.debug = debug

        if self.debug:
            libname = 'wx_baseud-'+env['WX_VERSION']
        else:
            libname = 'wx_baseu-'+env['WX_VERSION']


        env.AppendUnique(LIBS=[libname])


        cxxflags = []
        if debug:
            cxxflags = [
                '-isystem/usr/include/wx-'+env['WX_VERSION']+'/',
                '-isystem/usr/lib/x86_64-linux-gnu/wx/include/base-unicode-release-'+env['WX_VERSION']+'/',
                ]
        else:
            cxxflags = [
                '-isystem/usr/include/wx-'+env['WX_VERSION']+'/',
                '-isystem/usr/lib/x86_64-linux-gnu/wx/include/base-unicode-release-'+env['WX_VERSION']+'/',
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
            libname = 'wx_gtk2ud_core-'+env['WX_VERSION']
        else:
            libname = 'wx_gtk2u_core-'+env['WX_VERSION']


        env.AppendUnique(LIBS=[libname])


    def need_net(self, env):
        if self.debug:
            libname = 'wx_baseud_net-'+env['WX_VERSION']
        else:
            libname = 'wx_baseu_net-'+env['WX_VERSION']


        env.AppendUnique(LIBS=[libname])


    def need_xml(self, env):
        if self.debug:
            libname = 'wx_baseud_xml-'+env['WX_VERSION']
        else:
            libname = 'wx_baseu_xml-'+env['WX_VERSION']


        env.AppendUnique(LIBS=[libname])


    def need_adv(self, env):
        if self.debug:
            libname = 'wx_gtk2ud_adv-'+env['WX_VERSION']
        else:
            libname = 'wx_gtk2u_adv-'+env['WX_VERSION']


        env.AppendUnique(LIBS=[libname])

    def need_aui(self, env):
        if self.debug:
            libname = 'wx_gtk2ud_aui-'+env['WX_VERSION']
        else:
            libname = 'wx_gtk2u_aui-'+env['WX_VERSION']


        env.AppendUnique(LIBS=[libname])

    def need_html(self, env):
        if self.debug:
            libname = 'wx_gtk2ud_html-'+env['WX_VERSION']
        else:
            libname = 'wx_gtk2u_html-'+env['WX_VERSION']


        env.AppendUnique(LIBS=[libname])

    def need_qa(self, env):
        if self.debug:
            libname = 'wx_gtk2ud_qa-'+env['WX_VERSION']
        else:
            libname = 'wx_gtk2u_qa-'+env['WX_VERSION']


        env.AppendUnique(LIBS=[libname])

    def need_richtext(self, env):
        if self.debug:
            libname = 'wx_gtk2ud_richtext-'+env['WX_VERSION']
        else:
            libname = 'wx_gtk2u_richtext-'+env['WX_VERSION']


        env.AppendUnique(LIBS=[libname])


    def need_xrc(self, env):
        if self.debug:
            libname = 'wx_gtk2ud_xrc-'+env['WX_VERSION']
        else:
            libname = 'wx_gtk2u_xrc-'+env['WX_VERSION']


        env.AppendUnique(LIBS=[libname])

