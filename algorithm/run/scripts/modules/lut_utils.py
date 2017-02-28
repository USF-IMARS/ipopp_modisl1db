import os
import re
import ProcUtils as ProcUtils

class lut_utils:
    def __init__(self,mission=None,verbose=False,curdir=False,ancdir=None):
        """
        Utilities to update various LUT files for processing
        """

        self.mission = mission
        self.ancdir = ancdir
        self.curdir = curdir

        self.dirs = {}
        self.files = {}
        self.verbose = verbose
        self.status = 0

	#asurin 011317
        #self.query_site = "http://oceancolor.gsfc.nasa.gov"
        #self.data_site = "http://oceandata.sci.gsfc.nasa.gov"
        self.query_site = "https://oceancolor.gsfc.nasa.gov"
        self.data_site = "https://oceandata.sci.gsfc.nasa.gov"


    def update_aquarius(self):
        """
        update the aquarius luts
        """
        if self.verbose: print "[ Aquarius ]"

        # solar_flux_noon.txt
        url = self.data_site + "/Ancillary/LUTs/aquarius/solar_flux_noon.txt"
        outputdir = os.path.join(self.dirs['var'], 'aquarius')
        status = ProcUtils.httpdl(url, localpath=outputdir)
        if status:
            print "* ERROR: The download failed with status code: " + str(status)
            print "* Please check your network connection and for the existence of the remote file:"
            print "* " + self.data_site + "/Ancillary/LUTs/aquarius/solar_flux_noon.txt"
            self.status = 1
        else:
            if self.verbose: print "+ solar_flux_noon.txt"

        if self.verbose: print "[ Done ]\n"


    def update_seawifs(self):
        """
        update the SeaWiFS elements.dat and time_anomaly files
        """
        if self.verbose: print "[ SeaWiFS ]"

        # elements.dat
        url = self.data_site + "/Ancillary/LUTs/seawifs/elements.dat"
        outputdir = os.path.join(self.dirs['var'], 'seawifs')
        status = ProcUtils.httpdl(url, localpath=outputdir)
        if status:
            print "* ERROR: The download failed with status code: " + str(status)
            print "* Please check your network connection and for the existence of the remote file:"
            print "* " + self.data_site + "/Ancillary/LUTs/seawifs/elements.dat"
            self.status = 1
        else:
            if self.verbose: print "+ elements.dat"

        # time_anomaly.txt
        url = self.data_site + "/Ancillary/LUTs/seawifs/time_anomaly.txt"
        outputdir = os.path.join(self.dirs['var'], 'seawifs')
        status = ProcUtils.httpdl(url, localpath=outputdir)
        if status:
            print "*** ERROR: The download failed with status code: " + str(status)
            print "*** Please check your network connection and for the existence of the remote file:"
            print "* " + self.data_site + "/Ancillary/LUTs/seawifs/time_anomaly.txt"
            self.status = 1
        else:
            if self.verbose: print "+ time_anomaly.txt"

        if self.verbose: print "[ Done ]\n"


    def update_modis(self):
        """
        update the calibration LUTs, utcpole.dat and leapsec.dat files
        """
        if self.verbose: print "[ MODIS ]"

        msn = {'aqua':'modisa','terra':'modist'}
        url = self.data_site + "/Ancillary/LUTs/modis/leapsec.dat"
        outputdir = os.path.join(self.dirs['var'],'modis')
        status = ProcUtils.httpdl(url, localpath=outputdir)
        if status:
            print "* ERROR: The download failed with status code: " + str(status)
            print "* Please check your network connection and for the existence of the remote file:"
            print "* " + self.data_site + "/Ancillary/LUTs/modis/leapsec.dat"
            self.status = 1
        else:
            if self.verbose: print "+ leapsec.dat"

        url = self.data_site + "/Ancillary/LUTs/modis/utcpole.dat"
        outputdir = os.path.join(self.dirs['var'],'modis')
        status = ProcUtils.httpdl(url, localpath=outputdir)
        if status:
            print "* ERROR: The download failed with status code: " + str(status)
            print "* Please check your network connection and for the existence of the remote file:"
            print "* " + self.data_site + "/Ancillary/LUTs/modis/utcpole.dat"
            self.status = 1
        else:
            if self.verbose: print "+ utcpole.dat"

        if self.verbose:
            print "[ MODIS: %s ]" % self.mission.upper()

        # Get most recent version from local disk
        outputdir = os.path.join(self.dirs['var'], msn[self.mission],'cal', 'OPER')
        listFile =  os.path.join(outputdir,"index.html")
        luts = os.listdir(outputdir)
        for f in luts:
            if os.path.isdir(f) or re.search('^\.',f):
                luts.remove(f)
        
        # Get remote list of files and download if necessary
        # OPER
        status = ProcUtils.httpdl(self.data_site + "/Ancillary/LUTs/"+msn[self.mission] +"/cal/OPER/index.html", localpath=outputdir)
        if status:
            print "Error downloading %s" % '/'.join([self.data_site , "/Ancillary/LUTs/",msn[self.mission] ,"/cal/OPER/"])
            self.status = 1

        operlist = ProcUtils.cleanList(listFile)
        ProcUtils.remove(listFile)
        operversion = operlist[0].split('LUTs.')[1]

        #check for version - if different, remove existing files
        for f in luts:
            if f.find(operversion) < 0:
                os.remove(os.path.join(self.dirs['var'], msn[self.mission] , 'cal', 'OPER', f))
                if self.verbose: print "- OPER:" + f
        #check for existing files, if not there, get 'em!
        for f in operlist:
            if not os.path.exists(os.path.join(outputdir,f)):
                status = ProcUtils.httpdl(self.data_site + "/Ancillary/LUTs/"+msn[self.mission] +"/cal/OPER/" + f,localpath=outputdir)
                if status:
                    print "Error downloading %s" % f
                    self.status = 1
                else:
                    if self.verbose: print "+ OPER:" + f


        # EVAL
        outputdir = os.path.join(self.dirs['var'], msn[self.mission],'cal', 'EVAL')
        listFile =  os.path.join(outputdir,"index.html")

        status = ProcUtils.httpdl(self.data_site + "/Ancillary/LUTs/"+msn[self.mission] +"/cal/EVAL/index.html", localpath=outputdir)
        if status:
            print "Error downloading %s" % '/'.join([self.data_site , "/Ancillary/LUTs/",msn[self.mission] ,"/cal/EVAL/"])
            self.status = 1
        evallist = ProcUtils.cleanList(listFile)
        ProcUtils.remove(listFile)

        for f in evallist:
            if not os.path.exists(os.path.join(outputdir,f)):
                status = ProcUtils.httpdl(self.data_site + "/Ancillary/LUTs/"+msn[self.mission] +"/cal/EVAL/" + f,localpath=outputdir)
                if status:
                    print "Error downloading %s" % f
                    self.status = 1
                else:
                    if self.verbose: print "+ EVAL:" + f

        if self.verbose: print "[ Done ]\n"
