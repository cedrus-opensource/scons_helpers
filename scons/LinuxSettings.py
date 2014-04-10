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
        """
        Note: prior to upgrading from Ubuntu 10 (lucid) to Ubuntu 13 (saucy),
        we used to put '/usr/include' and '/usr/local/include' on the path here.
        For some reason, in Ubuntu 13 that *royally* screws up the build. It seems to
        be related to the fact that GCC is prepared to build for either 32-bit or 64-bit apps,
        and GCC itself needs to choose paths based on which bit-ed-ness is happening.
        So by us trying to *explicitly* mention system paths, it makes things BAD.
        """
        return UnixCompilerFlags.unix_common_cxxflags + [
            #'-isystem/usr/include', # see note above
            '-isystem/usr/include/mysql',
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

