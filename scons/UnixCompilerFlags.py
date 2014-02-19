#!/usr/bin/env python
import platform

unix_common_cxxflags =  [
	'-fmessage-length=0',
	'-pipe',
	'-fpermissive',
	'-fstack-check',
	'-ftrapv',
	'-fno-gnu-keywords',
	'-funit-at-a-time',
#	'-finline-limit=10000',
#	'--param',
#	'large-function-growth=10000',
#	'--param',
#	'inline-unit-growth=10000',

	# Warning Flags Here to End	
	'-Wall',
	'-Wextra',
#	'-Werror',

	'-Wstrict-null-sentinel',
	'-Woverloaded-virtual',
	'-Wmissing-braces',
	'-Wunused-parameter',
	'-Wsign-compare',
	'-Wconversion',
	'-Wfloat-equal',
	'-Winvalid-pch',
	'-Wdisabled-optimization',
	'-Wcast-align',
	'-Wcast-qual',
	'-Wno-endif-labels',
	'-Wmissing-format-attribute',
	'-Wpointer-arith',
	'-Wmissing-field-initializers',
	'-Wredundant-decls',
#	'-Winline',
	'-Wwrite-strings',
	'-Wformat=2',
	'-Wstrict-aliasing=2',
	'-Wno-unknown-pragmas',
	'-Wno-system-headers',
	'-Wno-deprecated-declarations',
	'-Wno-invalid-offsetof',
	'-Woverloaded-virtual',
]

if not platform.mac_ver()[0].startswith('10.4'):
    unix_common_cxxflags.append('-pthread')
