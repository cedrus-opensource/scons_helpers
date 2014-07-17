//
//    MacCocoaQtHelpers.mm
//
//    Created by Kelly Heller on 2013-12-13.
//    (c) Copyright 2013 Cedrus Corporation. All rights reserved.
//
//


#include "MacCocoaQtHelpers.h"
#import <AppKit/NSApplication.h>
#import <Foundation/NSBundle.h>
#import <Foundation/NSURL.h>

std::string Cedrus::GetMacAppBundlePath()
{
    NSURL* url=[[NSBundle mainBundle] bundleURL];

    std::string result( [url.path UTF8String] );

    [url release];

    return result;
}
