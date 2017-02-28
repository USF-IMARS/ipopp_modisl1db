#! /usr/bin/env python

from modules.ParamUtils import ParamProcessing

class extract:
    def __init__(self, file=file, parfile=None, outfile=None, geofile=None, north=None, south=None, west=None, east=None
    ,
                 log=False, sensor=None, verbose=False):
        # defaults
        self.file = file
        self.parfile = parfile
        self.geofile = geofile
        self.outfile = outfile
        self.log = log
        self.proctype = 'modisGEO'
        self.ancdir = None
        self.curdir = False
        self.pcf_file = None
        self.verbose = verbose
        self.dirs = {}
        self.sensor = sensor
        self.north = north
        self.south = south
        self.west = west
        self.east = east

        if self.parfile:
            print self.parfile
            p = ParamProcessing(parfile=self.parfile)
            p.parseParFile(prog='geogen')
            print p.params
            phash = p.params['geogen']
            for param in (phash.keys()):
                print phash[param]
                if not self[param]:
                    self[param] = phash[param]

    def __setitem__(self, index, item):
        self.__dict__[index] = item

    def __getitem__(self, index):
        return self.__dict__[index]

    def chk(self):
        """
        Check parameters
        """
        import os
        import sys

        if self.file is None:
            print "ERROR: No MODIS_L1A_file was specified in either the parameter file or in the argument list. Exiting"
            sys.exit(1)
        if not os.path.exists(self.file):
            print "ERROR: File '" + self.file + "' does not exist. Exiting."
            sys.exit(1)
        if self.sensor.find('modis') < 0 and not os.path.exists(self.geofile):
            print "ERROR: Geolocation file (%s) not found!" % self.geofile
            sys.exit(1)
        if not (self.north and self.south and self.west and self.east):
            print "Error: All four NSWE coordinates required!"
            sys.exit(1)
        if self.north <= self.south:
            print "Error: North must be greater than South!"
            sys.exit(1)
        if self.north > 90. or self.south < -90.:
            print "Latitude range outside realistic bounds!"
            sys.exit(1)
        if self.west < -180 or self.west > 180. or self.east < -180. or self.east > 180:
            print "Longitudes must be between -180.0 and 180.0"
            sys.exit(1)

    def run(self):
        """
        Run lonlat2pixline and l1aextract
        """
        import subprocess
        import os

        if self.verbose:
            print ""
            print "Locating pixel/line range ..."
        lonlat2pixline = os.path.join(self.dirs['bin'], 'lonlat2pixline')
        pixlincmd = [lonlat2pixline, self.geofile, str(self.west), str(self.south), str(self.east), str(self.north)]
        p = subprocess.Popen(pixlincmd, stdout=subprocess.PIPE)
        line = p.communicate()[0]
        if not p.returncode:
            pixlin = line.splitlines()[0][2:].split()

            l1extract = os.path.join(self.dirs['bin'], 'l1aextract_modis')
            extractcmd = ' '.join([' ', self.file, pixlin[0], pixlin[1], pixlin[2], pixlin[3], self.outfile])
            retcode = subprocess.call(l1extract + extractcmd, shell=True)
            if retcode:
                print "Error extracting file %s" % self.file
                return 1

        else:
            if p.returncode == 120:
                print "No extract necessary, entire scene contained within the selected region of interest."
                return 120
            else:
                print "Error locating pixel/line range to extract."
                return 1

        return 0



      
