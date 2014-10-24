#!/usr/bin/env python

__author__  = "$Author: kjones $"
__version__ = "$Revision: 7073 $"
__date__    = "$Date: 2010-08-02 13:02:43 -0700 (Mon, 02 Aug 2010) $"

import os, sys, time


import time
import datetime
import re # regular expressions
import SCons

from subprocess import *

def get_current_version_suffix( path_to_scons_dir, version_file ):
    text_version_file = path_to_scons_dir + os.sep + version_file
    sock = open(text_version_file,"r")
    sock.readline().rstrip(' \n') # throw away first line
    version = sock.readline().rstrip(' \n')
    sock.close()
    return version

def get_git_version():
    git_version = "ABCDEFGHIJKLM"

    try:
        git_version = Popen([ 'git', 'rev-list', '-1', 'HEAD' ], stdout=PIPE).communicate()[0].rstrip('\n')
    except:
        for annoy in range(10):
            print "\n\n\n\n>>>>>>>>>>>>>>>>>>>>>>>>>>> If you are making a shippable RELEASE this is BAD! Otherwise not so much. (failure to retrieve the version control information)"
            time.sleep(1)

    git_version = git_version[:8] # take only the first 8 char of the git commit hash

    return git_version
    
def DeclareAutoversioningBuildDuties( env, header_path, version_file_path ):

    # This creates [repo_original_source_files]/header_path/AutoversionHeader.h
    def PopulateVersionHeaderWithCurrentDateAndCommitHash( target, source, env ):

        path_that_sits_inside_source_repo = env.subst( header_path )

        # IMPORTANT! do NOT make changes to how we create AutoversionHeader without
        # giving CAREFUL CONSIDERATION to potential side-effects on class DeveloperHeaderForDiskFile
        run(
            path_that_sits_inside_source_repo, # where to create the header file
            'AutoversionHeader.h', # name of file to create
            source[0].abspath, # input file (SuperLab Current Version.txt)
            )

        return None

    path_to_av_header = env.subst( header_path )
    input_file_for_autoversion_header = env.subst( version_file_path )

    autoversion_header_action = env.Command(
        path_to_av_header + '/AutoversionHeader.h',  # the RESULTANT OUTPUT of this command
        input_file_for_autoversion_header,
        PopulateVersionHeaderWithCurrentDateAndCommitHash
        )

    # this is here because the other calls that use this path won't
    # work until the path has been CREATED
    env.Depends( autoversion_header_action, env['CEDRUS_COMPLETE_THIRD_PARTY_STAGING'] )

    # I thought SCons would figure out on its own to put this in
    # OBJ_ROOT, but it didn't.  There could be better ways to handle
    # all the stuff for AutoversionHeader.h, but this works reliably.
    copied_autoversion_header_action = env.Command(
        '$OBJ_ROOT/AutoversionHeader.h',
        autoversion_header_action,
        SCons.Script.Copy("$TARGET", "$SOURCE")
        )

    # this is here because the other calls that use this path won't
    # work until the path has been CREATED
    env.Depends( copied_autoversion_header_action, env['CEDRUS_COMPLETE_THIRD_PARTY_STAGING'] )


def run(path,outfile,input_file):
    sock = open(input_file,"r")
    current_version = sock.readline().rstrip(' \n')
    sock.close()

    git_version = get_git_version()

    current_date = time.strftime("%B %d, %Y" )
    text_version ="Version %s\\n%s release (build %s)" % ( current_version, current_date, git_version )

    # IMPORTANT! do NOT make changes to how we populate AutoversionHeader without
    # giving CAREFUL CONSIDERATION to potential side-effects on class DeveloperHeaderForDiskFile
    output = """#define APPLICATION_BUILD_VERSION_STRING wxT("%s")
#define APPLICATION_SHORT_VERSION_STRING wxT("%s")
""" % ( text_version, current_version )

#   print( output )

    sock = open(os.path.join(path,outfile),"w")

    sock.write(output)
    sock.close()

# In bash terms, this is what the above python script does:
#
# SVN_VERSION=`${SVN} info | awk '/Revision/ {print $2}'`
# DATE=`date +'%B %e, %Y'`
# REVISION_STRING="${DATE} release (build ${SVN_VERSION})"
# TEXT_VERSION="Version ${APPLICATION_VERSION}\n${REVISION_STRING}"
#
# cd "${PROJECT_DIR}/../../src/SuperLab/"
#
# echo "#define APPLICATION_BUILD_VERSION_STRING wxT(\"${TEXT_VERSION}\")
# #define APPLICATION_SHORT_VERSION_STRING wxT(\"${APPLICATION_VERSION}\")" > ApplicationVersion.h
