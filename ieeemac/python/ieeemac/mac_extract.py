#!/usr/bin/env python
# ieeemac-extract
# Copyright (C) 2007, 2008 Justin Azoff JAzoff@uamail.albany.edu
#
# This module is released under the MIT License:
# http://www.opensource.org/licenses/mit-license.php

import sys
from ieeemac import find_macs, REGEXES

def mac_extract(format=None):
    """Extract ip addresses from stdin"""
    for line in sys.stdin:
        for mac in find_macs(line):
            if not format:
                print mac
            else:
                print mac.to_format(format)

def main():
    from optparse import OptionParser
    parser = OptionParser()
    format_help = "output format, one of %s" % ','.join(REGEXES.keys())
    parser.add_option("-f", "--format",        dest="format", action="store", help=format_help)

    (options, args) = parser.parse_args()
    mac_extract(options.format)

if __name__ == "__main__": 
    main()
