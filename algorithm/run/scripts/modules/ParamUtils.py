# Utilities used by processing module, ocproc.py

__author__="Sean Bailey, Futuretech Corporation"
__date__ ="$Apr 10, 2010 4:49:15 PM$"

import re

class ParamProcessing:
    """
    Parameter processing class - build and parse par files
    """
    def __init__(self, params=None,parfile=None,parstr='',sensor=None):
        """
        Set up parameter processing methods
        """
        if params is None: params = {}
        self.params = params
        self.parfile = parfile
        self.parstr = parstr
        self.sensor = sensor

    ############################################################################
    def buildParameterFile(self,prog):
        """Build a parameter file  from a dictionary of parameters.
        Writes parfile if pfile is defined, else Returns parfile string."""

        for k in self.params[prog].keys():
            if re.match('ocproc',k):
                del self.params[prog][k]

        filelst = ['ifile','ofile','ofile1','ofile2','ofile3','geofile',
            'spixl','dpixl','epixl','sline','eline','dline',
            'north','south','west','east']
        self.parstr = ''
        for f in filelst:
            try:
                pstr = '='.join([f, self.params[prog][f]])
                self.parstr = "\n".join([self.parstr,pstr])
            except Exception:
                pass

        for k,v in sorted(self.params[prog].items()):
            try:
                try:
                    filelst.index(k)
                    pass
                except Exception:
                    pstr = '='.join([k, v])
                    self.parstr = "\n".join([self.parstr,pstr])
            except Exception:
                pass

        if self.parfile:
            print "Writing parfile %s" % self.parfile
            logfile = open(self.parfile, 'w')
            logfile.write(self.parstr)
            logfile.write("\n")
            logfile.close()


    ############################################################################
    def parseParFile(self,prog='main'):
        """Parse a parameter file
        Returns a dictionary listing"""
        try:
            print 'PAR',self.parfile
            pfile = self.parfile
            pf = open(pfile,'r')
        except Exception:
            print "File %s not found!", self.parfile
            return None

        line = pf.read()
        arr = line.split('\n')
        try:
            self.params[prog]
        except Exception:
            self.params[prog]={}

        for m in arr:
            if re.match('^#',m):
                parts = m.split()
                try:
                    ix = parts.index('section')
                    prog = parts[ix+1].strip()
                    try:
                        self.params[prog] #TODO Fix this odd construction
                        continue
                    except Exception:
                        self.params[prog]={}
                except Exception:
                    pass
                continue
            if re.match('^\s+$',m):
                continue
            n = m.strip().split('=')
            if n[0]:
                if n[0] == 'par':
                    p2 = ParamProcessing(parfile=n[1])
                    p2.parseParFile(prog=prog)
                    self.params[prog].update(p2.params[prog])

                else:
                    self.params[prog][n[0]] = n[1]

    ############################################################################
    def genOutputFilename(self,prog=None):
        """Given a program, derive a standard output filename"""

        ifile = self.params[prog]['ifile']
        modsen ={'A':'T','P':'A'}
        ofile = None
        
        try:
            ofile = self.params[prog]['ofile']
        except Exception:
            fparts = ifile.split('.')
            if prog == 'l1agen':
                if re.search('L0',ifile):
                    ofile = ifile.replace('L0','L1A')
                elif re.match('M?D*',ifile):
                    type = ifile[6]
                    yrdy = ifile[7:14]
                    hrmn = ifile[15:19]
                    ofile = ''.join([modsen[type],yrdy,hrmn,'00.L1A_LAC'])
            elif prog == 'l1brsgen':
                ofile = '.'.join([fparts[0],'L1_BRS'])
            elif prog == 'l1mapgen':
                ofile = '.'.join([fparts[0],'L1_MAP'])
            elif prog == 'l2gen':
                if re.search('L1[AB]',ifile):
                    of = re.compile( '(L1A|L1B)')
                    ofile = of.sub( 'L2', ifile)
                else:
                    ofile = '.'.join([fparts[0],'L2'])
            elif prog == 'l2brsgen':
                try:
                    prod = self.params[prog]['prod']
                except Exception:
                    prod = 'chlor_a'
                ofile = '.'.join([fparts[0],prod,'L2_BRS'])
            elif prog == 'l2mapgen':
                try:
                    prod = self.params[prog]['prod']
                except Exception:
                    prod = 'chlor_a'
                ofile = '.'.join([fparts[0],prod,'L2_MAP'])
            elif prog == 'l2bin':
                ofile = 'output.file'
            elif prog == 'l3bin':
                ofile = 'output.file'
            elif prog == 'smigen':
                  ofile = 'output.file'
            elif prog == 'smitoppm':
                ofile = '.'.join([ifile,'ppm'])
            elif prog == 'l3gen':
                ofile = 'output.file'

            else:
                ofile = '.'.join([prog,'output_file'])

        self.params[prog]['ofile'] = ofile
