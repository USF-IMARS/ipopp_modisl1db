#! /usr/bin/env python

"""
update_luts.py

Updates LUTS for the various sensors. 
"""

import sys
from modules.setupenv import env
from optparse import OptionParser
import modules.lut_utils as lu

if __name__ == "__main__":
    mission = None
    verbose = False
    printlist = True

    msnlst = ['seawifs','aqua','terra','aquarius']
    version = "%prog 1.0"

    # Read commandline options...
    usage = '''
    %prog [OPTIONS] MISSION

    MISSION is either seawifs, aqua, terra, or aquarius'''

    parser = OptionParser(usage=usage, version=version)

    parser.add_option("-v", "--verbose", action="store_true", dest='verbose',
        default=False, help="print status messages")

    (options, args) = parser.parse_args()

    if args:
        mission = args[0]
    if options.verbose:
        verbose = options.verbose

    if mission is None:
        parser.print_help()
        sys.exit(0)

    if not (mission.lower() in msnlst):
        print "Mission needs to be one of:"
        for m in msnlst:
            print m

        sys.exit(0)

    l=lu.lut_utils(verbose=verbose,mission=mission.lower())
    
    env(l)

    if mission.lower() == 'aquarius':
        l.update_aquarius()
    if mission.lower() == 'seawifs':
        l.update_seawifs()
    if mission.lower() in ['aqua','terra']:
        l.update_modis()

    exit(l.status)