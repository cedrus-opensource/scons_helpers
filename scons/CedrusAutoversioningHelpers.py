#!/usr/bin/env python

import os, time

from subprocess import *

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

def run_autoversioning(path,outfile,input_file):
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
