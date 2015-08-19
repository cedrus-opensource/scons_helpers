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
            return [
                '-F$OBJ_ROOT',
                '-isysroot/Applications/Xcode.app/Contents/Developer/Platforms/MacOSX.platform/Developer/SDKs/MacOSX10.7.sdk',
                '-mmacosx-version-min=10.7',
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
            return UnixCompilerFlags.unix_common_cxxflags + [
                '-Wmost',
                '-Wshorten-64-to-32',
                '-Wnewline-eof',
                '-Woverloaded-virtual',
                '-fvisibility-ms-compat',
                '-fvisibility-inlines-hidden',
                '-isysroot/Applications/Xcode.app/Contents/Developer/Platforms/MacOSX.platform/Developer/SDKs/MacOSX10.7.sdk',
                '-mmacosx-version-min=10.7',
                '-fstrict-aliasing',
                '-std=c++11',
                '-stdlib=libc++',
                ]

    def getDebugCxxFlags(self):
        current_arch = platform.machine()

        flags = [
            '-arch',
            current_arch,
            '-g',
            '-O0'
        ]
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
            'i386',
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
        current_arch = platform.machine()

        flags = [
            '-arch',
            current_arch,
        ]
        return flags

    def getReleaseLinkerFlags(self):
        return [
            '-arch',
            'i386',
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

