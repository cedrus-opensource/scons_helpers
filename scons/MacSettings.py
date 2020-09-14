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
        elif wxVersion == 'NONE':
            self.wxEnvVar = 'NONE'
        else:
            print ("Unsupported wxWidgets version!")
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
                'MACOSX_DEPLOYMENT_TARGET=10.13',
                'OS_MACOSX=OS_MACOSX',
            ]

        elif self.wxEnvVar == 'NONE':
            return [
                '__DARWIN__',
                '_FILE_OFFSET_BITS=64',
                '_LARGE_FILES',
                'MAC_OS_X_VERSION_MIN_REQUIRED=1070',
                'MACOSX_DEPLOYMENT_TARGET=10.13',
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

        elif self.wxEnvVar == 'WXWIN_29' or self.wxEnvVar == 'NONE':
                return [
                    '-F$OBJ_ROOT',
                    '-isysroot/Applications/Xcode.app/Contents/Developer/Platforms/MacOSX.platform/Developer/SDKs/MacOSX10.13.sdk',
                    '-mmacosx-version-min=10.12',
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

        elif self.wxEnvVar == 'WXWIN_29' or self.wxEnvVar == 'NONE':
            return UnixCompilerFlags.unix_common_cxxflags + [
                '-Wmost',
                '-Wshorten-64-to-32',
                '-Wnewline-eof',
                '-Woverloaded-virtual',
                '-ftemplate-depth=256', # <-- our 10.8 machines were using 128. some boost spirit grammars need more.
                '-fvisibility-ms-compat',
                '-fvisibility-inlines-hidden',
                '-isysroot/Applications/Xcode.app/Contents/Developer/Platforms/MacOSX.platform/Developer/SDKs/MacOSX10.13.sdk',
                '-mmacosx-version-min=10.12',
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

        flags += [ '-fstandalone-debug' ]

        return flags


    def getReleaseCxxFlags(self):
        flags = [
            '-Os',
            '-fexpensive-optimizations',
            '-fstrength-reduce',
            '-foptimize-sibling-calls',
            '-fgcse',
            '-funit-at-a-time',
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

        if self.wxEnvVar == 'WXWIN_29' or self.wxEnvVar == 'NONE':
            result += [ 'wxDEBUG_LEVEL=2' ]

        return result

    def getReleaseDefines(self):
        result = []

        if self.wxEnvVar == 'WXWIN_29' or self.wxEnvVar == 'NONE':
            result += [ 'wxDEBUG_LEVEL=0' ]

        return result

    def getDebugLinkerFlags(self):

        """
        a note in case you are having trouble getting libgmalloc to load into your process.
        For me, on mac 10.8, i had to use linker flag:  #'-lgmalloc',
        ... and the path to the dylib was:
            '/Applications/Xcode.app/Contents/Developer/Platforms/MacOSX.platform/Developer/SDKs/MacOSX10.7.sdk/usr/lib'
        """

        flags = [
            '-arch',
            'x86_64',
        ]

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
