import os
from SCons.Script import *

class WindowsSettings:
    def __init__(self, env):
        self.env = env

    def getCommonDefines(self):
        return [
            'WIN32',
            '_WIN32_WINNT=0x0601', # 0x501 means we target XP (or later) 0x601 is Win7 or later
            '_UNICODE',
            'BOOST_ALL_DYN_LINK',
            'BOOST_REGEX_DYN_LINK',
            'BOOST_LIB_DIAGNOSTIC',
            'UNICODE',
            'WXUSINGDLL',
            'wxUSE_SERVICE_DISCOVERY=1',
             '_ALLOW_RTCc_IN_STL',
             '_ATL_DISABLE_NOTHROW_NEW' 
        ]

    def getCommonLibs(self):
        return [
            #'unicows',  # commented out in Feb 2011 because it fails to be found on the slave2 win 7 machine. we don't need this ? ? why has it been here, then?
            'winmm',
            'comctl32',
            'rpcrt4',
            'oleacc',
            'kernel32',
            'user32',
            'gdi32',
            'winspool',
            'comdlg32',
            'advapi32',
            'shell32',
            'ole32',
            'oleaut32',
            'uuid',
            'odbc32',
            'odbccp32',
        ]

    def getCommonInclude(self):
        return [
        ]

    def getCommonLibPath(self):
        libs = [
            '.',
            os.getenv('SYSTEMDRIVE','') + '\Program Files\Bonjour SDK\lib\win32',
            os.getenv('SYSTEMDRIVE','') + '\Program Files (x86)\Bonjour SDK\lib\win32',
        ]

        return libs

    def getCommonLinkerFlags(self):
        flags = [
            '/MACHINE:X64',
            '/INCREMENTAL:NO',
        ]

        return flags

    def getCommonCxxFlags(self):
        flags = [
            '/EHs', # catch C++ exceptions AND assume that extern C functions may also throw an exception
            # '/FD', # IDE minimal rebuild.  This should not be used from the command line or a build script.
            '/Gy', # enable function-level linking, required for for Edit and Continue.  We may not need this, but there's a comment in the documentation about C++ member functions not being "packaged" without this.
            '/openmp',
            '/TP',
            '/FC', # use full pathnames in diagnostics (full paths will show up in "Error List" in visual studio
            '/W4',
            '/wd4068',  # no unknown pragmas
            '/wd4275',  # non dll-interface class used as base for dll-interface class. http://www.unknownroad.com/rtfm/VisualStudio/warningC4251.html
            '/wd4503',  # decorated name length exceeded, name was truncated
            '/wd4481',  # nonstandard extension used: override specifier 'override'
            '/wd4996',  # '____' was declared deprecated
            '/Zm370'
           #'/showIncludes'
        ]

        return flags

    def getDebugCxxFlags(self):
        return [
            '/RTC1', # enable stack frame run-time error checking, and report when a variable is used without having been initialized
            '/RTCc', # report when a value is assigned to a smaller data type and results in data loss
            '/MDd',
            '/Od',
        ]

    def getReleaseCxxFlags(self):
        return [
            '/MD',
            '/O1',
        ]

    def getDebugDefines(self):
        result = [
            '_DEBUG',
            '__DEBUG__',
            '__WXDEBUG__',
        ]

        if self.env['WX_VERSION'] == '3.0':
            result += [ 'wxDEBUG_LEVEL=2' ]

        return result

    def getReleaseDefines(self):
        result = [
        ]

        if self.env['WX_VERSION'] == '3.0':
            result += [ 'wxDEBUG_LEVEL=0' ]

        return result

    def getDebugLinkerFlags(self):
        return [
            '/DEBUG'
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

