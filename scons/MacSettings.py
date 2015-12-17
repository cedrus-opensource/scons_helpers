import os
from SCons.Script import *
import UnixCompilerFlags
import platform

class MacSettings:
    def __init__(self, wxVersion ):
        self.wxVersion = wxVersion
        if wxVersion == '2.8':
            self.wxEnvVar = 'WXWIN_SL'
        elif wxVersion >= '2.9':
            self.wxEnvVar = 'WXWIN_29'
        else:
            print "Unsupported wxWidgets version!"
            Exit(1)

    def getCommonDefines(self):
        if self.wxEnvVar == 'WXWIN_SL':
            return [
                '__DARWIN__',
                '_FILE_OFFSET_BITS=64',
                '_LARGE_FILES',
                '__WXMAC__',
                'WXUSINGDLL',
                'wxUSE_SERVICE_DISCOVERY=1',
                'MAC_OS_X_VERSION_MIN_REQUIRED=1040',
                'MACOSX_DEPLOYMENT_TARGET=10.4',
                'OS_MACOSX=OS_MACOSX',
            ]

        elif self.wxEnvVar == 'WXWIN_29':
            return [
                '__DARWIN__',
                '_FILE_OFFSET_BITS=64',
                '_LARGE_FILES',
                '__WXMAC__',
                'WXUSINGDLL',
                '__WXOSX__',
                '__WXOSX_COCOA__',
                'wxUSE_SERVICE_DISCOVERY=1',
                'MAC_OS_X_VERSION_MIN_REQUIRED=1070',
                'MACOSX_DEPLOYMENT_TARGET=10.7',
                'OS_MACOSX=OS_MACOSX',
            ]

    def getCommonLibs(self):
        return [
        ]

    def getCommonInclude(self):
        return [
        ]

    def getCommonLibPath(self):
        return [
        ]

    def getCommonLinkerFlags(self):
        if self.wxEnvVar == 'WXWIN_SL':
            return [
                '-F$OBJ_ROOT',
                '-isysroot/Developer/SDKs/MacOSX10.4u.sdk',
                '-mmacosx-version-min=10.4',
                ]

        elif self.wxEnvVar == 'WXWIN_29':
            # after we ship 5.0.5 we can remove this next 'if' and just ALWAYS do 10.9 sdk:
            if not platform.mac_ver()[0].startswith('10.11'):
                return [
                    '-F$OBJ_ROOT',
                    '-isysroot/Applications/Xcode.app/Contents/Developer/Platforms/MacOSX.platform/Developer/SDKs/MacOSX10.7.sdk',
                    '-mmacosx-version-min=10.7',
                    '-stdlib=libc++',
                ]
            else:
                return [
                    '-F$OBJ_ROOT',
                    '-isysroot/Applications/Xcode.app/Contents/Developer/Platforms/MacOSX.platform/Developer/SDKs/MacOSX10.9.sdk',
                    '-mmacosx-version-min=10.9',
                    '-stdlib=libc++',
                ]

    def getCommonCxxFlags(self):
        if self.wxEnvVar == 'WXWIN_SL':
            return UnixCompilerFlags.unix_common_cxxflags + [
                '-Wmost',
                '-Wshorten-64-to-32',
                '-Wnewline-eof',
                '-Woverloaded-virtual',
                '-fvisibility-ms-compat',
                '-fvisibility-inlines-hidden',
                '-isysroot/Developer/SDKs/MacOSX10.4u.sdk',
                '-mmacosx-version-min=10.4',
                '-fstrict-aliasing',
                ]

        elif self.wxEnvVar == 'WXWIN_29':
            # after we ship 5.0.5 we can remove this next 'if' and just ALWAYS do 10.9 sdk:
            if not platform.mac_ver()[0].startswith('10.11'):
                return UnixCompilerFlags.unix_common_cxxflags + [
                    '-Wmost',
                    '-Wshorten-64-to-32',
                    '-Wnewline-eof',
                    '-Woverloaded-virtual',
                    '-ftemplate-depth=256', # <-- our 10.8 machines were using 128. some boost spirit grammars need more.
                    '-fvisibility-ms-compat',
                    '-fvisibility-inlines-hidden',
                    '-isysroot/Applications/Xcode.app/Contents/Developer/Platforms/MacOSX.platform/Developer/SDKs/MacOSX10.7.sdk',
                    '-mmacosx-version-min=10.7',
                    '-fstrict-aliasing',
                    '-std=c++11',
                    '-stdlib=libc++',
                ]
            else:
                return UnixCompilerFlags.unix_common_cxxflags + [
                    '-Wmost',
                    '-Wshorten-64-to-32',
                    '-Wnewline-eof',
                    '-Woverloaded-virtual',
                    '-ftemplate-depth=256', # <-- our 10.8 machines were using 128. some boost spirit grammars need more.
                    '-fvisibility-ms-compat',
                    '-fvisibility-inlines-hidden',
                    '-isysroot/Applications/Xcode.app/Contents/Developer/Platforms/MacOSX.platform/Developer/SDKs/MacOSX10.9.sdk',
                    '-mmacosx-version-min=10.9',
                    '-fstrict-aliasing',
                    '-std=c++11',
                    '-stdlib=libc++',
                ]

    def getDebugCxxFlags(self):

        flags = [
            '-arch',
            'x86_64',
            '-g',
            '-O0'
        ]

        # after we ship 5.0.5 we can remove this next 'if' and just ALWAYS do this:
        if platform.mac_ver()[0].startswith('10.11'):
            # if you want (via homebrew) to get GDB, then you need this flag so breakpoints work in gdb:
            flags += [ '-fstandalone-debug' ]

        return flags


    def getReleaseCxxFlags(self):
        flags = [
            '-Os',
            '-fdelete-null-pointer-checks',
            '-fexpensive-optimizations',
            '-ftree-pre',
            '-fweb',
            '-fstrength-reduce',
            '-fthread-jumps',
            '-fcrossjumping',
            '-foptimize-sibling-calls',
            '-fcse-follow-jumps',
            '-fcse-skip-blocks',
            '-fgcse',
            '-fgcse-lm',
            '-fregmove',
            '-freorder-functions',
            '-funit-at-a-time',
            '-falign-labels',
            '-arch',
            'x86_64',
            '-ftree-vectorize',
        ]

        return flags

    def getDebugDefines(self):
        result = [
            '__DEBUG__',
            '__WXDEBUG__',
            '_DEBUG'
        ]

        if self.wxEnvVar == 'WXWIN_29':
            result += [ 'wxDEBUG_LEVEL=2' ]

        return result

    def getReleaseDefines(self):
        result = []

        if self.wxEnvVar == 'WXWIN_29':
            result += [ 'wxDEBUG_LEVEL=0' ]

        return result

    def getDebugLinkerFlags(self):

        flags = [
            '-arch',
            'x86_64',
        ]

        # after we ship 5.0.5 we can remove this next 'if' and just ALWAYS do this:
        if platform.mac_ver()[0].startswith('10.11'):
            # the '-fstandalone' is to help out GDB. but using the debug sym flags in the linker
            # is now ESSENTIAL so that our dSYM symbols work (in lldb! in Xcode! not just for gdb)
            flags += [ '-g', '-fstandalone-debug' ]

        return flags

    def getReleaseLinkerFlags(self):
        return [
            '-arch',
            'x86_64',
        ]

    def getDebugLibraries(self):
        return [
        ]

    def getReleaseLibraries(self):
        return [
        ]

    def getDebugIncludes(self):
        return [
        ]

    def getReleaseIncludes(self):
        return [
        ]
