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

        self.debug = (build_mode == 'dbg')

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

    def need_media(self):
        self.impl.need_media(self.env)

class CedrusWxWidgetsMac:

    def __init__(self, env, debug, wx_ver):
        self.debug = debug

        self.mac_str = 'macu'
        self.carb_coco_str = 'base_carbonu'

        self.wx_ver = wx_ver

        if StrictVersion(wx_ver) >= StrictVersion('2.9'):
            self.mac_str = 'osx_cocoau'
            self.carb_coco_str = 'baseu'

        self._always_need_base(env)
        self._proceed_with_include_paths(env)

    def _proceed_with_include_paths(self, env):
        # set cxxflags for wxWidgets
        cxxflags = [
                     '-isystem' + env['WX_DIR'] + '/include',
                     '-isystem' + env['WX_DIR'] + '/lib/wx/include/osx_cocoa-unicode-' + env['WX_VERSION']
                   ]

        env.AppendUnique( CXXFLAGS = cxxflags )

    def _always_need_base(self, env):
        build_tag = 'd-' if self.debug else '-'
        libname = 'wx_' + self.carb_coco_str + build_tag + self.wx_ver
        env.AppendUnique(LIBS=[libname])
        lib_path = [ env['WX_DIR'] + '/lib']
        env.AppendUnique( LIBPATH = lib_path, LIBS = [libname] )

    def publish_all_libs_to_staging(self, env):
        build_tag = '*ud[_-]*' if self.debug else '*u[_-]*'
        wxlibs = env.Glob( env['WX_DIR'] + '/lib/' + build_tag + '.dylib' )
        results = []
        for lib in wxlibs:
            results += env.Install( '$STAGING_DIR', lib )
        return results

    def need_core(self, env):
        self._always_need_base(env)
        self._proceed_with_include_paths(env)
        build_tag = 'd_core-' if self.debug else '_core-'
        libname = 'wx_' + self.mac_str + build_tag + self.wx_ver
        env.AppendUnique(LIBS=[libname])

    def need_net(self, env):
        self._always_need_base(env)
        self._proceed_with_include_paths(env)
        build_tag = 'd_net-' if self.debug else '_net-'
        libname = 'wx_' + self.carb_coco_str + build_tag + self.wx_ver
        env.AppendUnique(LIBS=[libname])

    def need_xml(self, env):
        self._always_need_base(env)
        self._proceed_with_include_paths(env)
        build_tag = 'd_xml-' if self.debug else '_xml-'
        libname = 'wx_' + self.carb_coco_str + build_tag + self.wx_ver
        env.AppendUnique(LIBS=[libname])

    def need_adv(self, env):
        self._always_need_base(env)
        self._proceed_with_include_paths(env)
        build_tag = 'd_adv-' if self.debug else '_adv-'
        libname = 'wx_' + self.mac_str + build_tag + self.wx_ver
        env.AppendUnique(LIBS=[libname])

    def need_aui(self, env):
        self._always_need_base(env)
        self._proceed_with_include_paths(env)
        build_tag = 'd_aui-' if self.debug else '_aui-'
        libname = 'wx_' + self.mac_str + build_tag + self.wx_ver
        env.AppendUnique(LIBS=[libname])

    def need_html(self, env):
        self._always_need_base(env)
        self._proceed_with_include_paths(env)
        build_tag = 'd_html-' if self.debug else '_html-'
        libname = 'wx_' + self.mac_str + build_tag + self.wx_ver
        env.AppendUnique(LIBS=[libname])

    def need_qa(self, env):
        self._always_need_base(env)
        self._proceed_with_include_paths(env)
        build_tag = 'd_qa-' if self.debug else '_qa-'
        libname = 'wx_' + self.mac_str + build_tag + self.wx_ver
        env.AppendUnique(LIBS=[libname])

    def need_richtext(self, env):
        self._always_need_base(env)
        self._proceed_with_include_paths(env)
        build_tag = 'd_richtext-' if self.debug else '_richtext-'
        libname = 'wx_' + self.mac_str + build_tag + self.wx_ver
        env.AppendUnique(LIBS=[libname])

    def need_xrc(self, env):
        self._always_need_base(env)
        self._proceed_with_include_paths(env)
        build_tag = 'd_xrc-' if self.debug else '_xrc-'
        libname = 'wx_' + self.mac_str + build_tag + self.wx_ver
        env.AppendUnique(LIBS=[libname])

    def need_media(self, env):
        self._always_need_base(env)
        self._proceed_with_include_paths(env)
        build_tag = 'd_media-' if self.debug else '_media-'
        libname = 'wx_' + self.mac_str + build_tag + self.wx_ver
        env.AppendUnique(LIBS=[libname])

class CedrusWxWidgetsWindows:
    def __init__(self, env, debug, wx_ver):
        self.debug = debug
        self.wx_ver = wx_ver
        self.wx_ver_no_dots = wx_ver.replace('.','')

        build_tag = 'ud' if self.debug else 'u'
        libname = 'wxbase' + self.wx_ver_no_dots + build_tag

        env.AppendUnique(LIBS=[libname])

        self.vc_dir = 'vc_dll_vc14' if env['MSVC_VERSION'] == '14.0' else 'vc_dll_vc10'

        cxxflags = [
                     '/I' + env['WX_DIR'] + '/lib/' + self.vc_dir + '/mswu/',
                     '/I' + env['WX_DIR'] + '/include',
                   ]

        lib_path = [ env['WX_DIR'] + '/lib/' + self.vc_dir, ]

        env.AppendUnique( CXXFLAGS = cxxflags,
                    LIBPATH = lib_path,
                    LIBS = [libname])

    def publish_all_libs_to_staging(self, env):
        build_tag = '*ud[_-]*' if self.debug else '*u[_-]*'

        wxlibs = env.Glob( env['WX_DIR'] + '/lib/' + self.vc_dir + '/' + build_tag + '.dll' )
        wxlibs += env.Glob( env['WX_DIR'] + '/lib/' + self.vc_dir + '/' + build_tag + '.pdb' )

        results = []

        for lib in wxlibs:
            name_parts = os.path.splitext(lib.name)
            lib_basename = name_parts[0]
            lib_basename = lib_basename.replace('_vcCedrus','')
            results += env.Install( '$STAGING_DIR', lib )

        return results

    def need_core(self, env):
        build_tag = 'ud_core' if self.debug else 'u_core'
        libname = 'wxmsw' + self.wx_ver_no_dots + build_tag
        env.AppendUnique(LIBS=[libname])

    def need_net(self, env):
        build_tag = 'ud_net' if self.debug else 'u_net'
        libname = 'wxbase' + self.wx_ver_no_dots + build_tag
        env.AppendUnique(LIBS=[libname])

    def need_xml(self, env):
        build_tag = 'ud_xml' if self.debug else 'u_xml'
        libname = 'wxbase' + self.wx_ver_no_dots + build_tag
        env.AppendUnique(LIBS=[libname])

    def need_adv(self, env):
        build_tag = 'ud_adv' if self.debug else 'u_adv'
        libname = 'wxmsw' + self.wx_ver_no_dots + build_tag
        env.AppendUnique(LIBS=[libname])

    def need_aui(self, env):
        build_tag = 'ud_aui' if self.debug else 'u_aui'
        libname = 'wxmsw' + self.wx_ver_no_dots + build_tag
        env.AppendUnique(LIBS=[libname])

    def need_html(self, env):
        build_tag = 'ud_html' if self.debug else 'u_html'
        libname = 'wxmsw' + self.wx_ver_no_dots + build_tag
        env.AppendUnique(LIBS=[libname])

    def need_qa(self, env):
        build_tag = 'ud_qa' if self.debug else 'u_qa'
        libname = 'wxmsw' + self.wx_ver_no_dots + build_tag
        env.AppendUnique(LIBS=[libname])

    def need_richtext(self, env):
        build_tag = 'ud_richtext' if self.debug else 'u_richtext'
        libname = 'wxmsw' + self.wx_ver_no_dots + build_tag
        env.AppendUnique(LIBS=[libname])

    def need_xrc(self, env):
        build_tag = 'ud_xrc' if self.debug else 'u_xrc'
        libname = 'wxmsw' + self.wx_ver_no_dots + build_tag
        env.AppendUnique(LIBS=[libname])

    def need_media(self, env):
        build_tag = 'ud_media' if self.debug else 'u_media'
        libname = 'wxmsw' + self.wx_ver_no_dots + build_tag
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
                '-isystem/usr/include/wx-' + env['WX_VERSION']+'/',
                '-isystem/usr/lib/x86_64-linux-gnu/wx/include/base-unicode-release-' + wx_ver +'/',
                ]

        lib_path = [ '/usr/lib/' ]

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
