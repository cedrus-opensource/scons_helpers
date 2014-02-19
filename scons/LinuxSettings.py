import os
from SCons.Script import *
import UnixCompilerFlags

class LinuxSettings:

    def getCommonDefines(self):
        return [
            '_FILE_OFFSET_BITS=64',
            '_LARGE_FILES',
            '__WXGTK__',
            'WXUSINGDLL',
            'wxUSE_SERVICE_DISCOVERY=1',
        ]

    def getCommonLibs(self):
        return [
        ]

    def getCommonInclude(self):
        return [
        ]

    def getCommonLibPath(self):
        return [
            '.',
            '/usr/local/lib/'       # gmock and gtest are in /usr/local/, whereas boost and wx are NOT (boost and wx are in just '/usr')
        ]

    def getCommonLinkerFlags(self):
        return [
        ]

    def getCommonCxxFlags(self):
        return UnixCompilerFlags.unix_common_cxxflags + [
            '-isystem/usr/include',
            '-isystem/usr/local/include',  # gmock and gtest are in /usr/local/, whereas boost and wx are NOT (boost and wx are in just '/usr')
            '-isystem/usr/include/mysql',
            '-isysroot/usr/include',
            '-fno-strict-aliasing',
        ]

    def getDebugCxxFlags(self):
        return [
            '-g',
            '-O0',
        ]

    def getReleaseCxxFlags(self):
        return [
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
            '-ftree-vectorize',
            '-Os',
        ]

    def getDebugDefines(self):
        return [
            '__DEBUG__',
            '__WXDEBUG__',
            '_DEBUG',
        ]

    def getReleaseDefines(self):
        return [
            'NDEBUG'
        ]

    def getDebugLinkerFlags(self):
        return [
        ]

    def getReleaseLinkerFlags(self):
        return [
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

