#!/usr/bin/env python

"""
Re-creates tests from modisl1db_usingBashScripts_tests but directly calls the
wrapper from python and does not depend on the run-* bash scripts.

NOTE: l1atob tests NOT re-created.
"""

# std modules:
import unittest

# dependencies:
from StationTester.TestHelper import TestHelper

class Test_modisl1db_directWrapperCall(unittest.TestCase):

    def setup(self):
        TestHelper.mySetup()

    def teardown(self):
        TestHelper.myTeardown()

    # tests:
    #########################
    def test_l0_to_l1_aqua(self):
        # using "".format() kwargs to make command:
        TestHelper.SPA_command( self,
            (
                """\
                    ~/drl/SPA/modisl1db/wrapper/l0tol1 \
                    modis.pds $INPUT/{PDSFILE} \
                    modis.mxd01 $OUTPUT/{MOD01} \
                    modis.mxd03 $OUTPUT/{MODGEO} \
                    sat {SAT} \
                    gbad_att $INPUT/{ATTFILE1} \
                    gbad_eph $INPUT/{EPHFILE1} \
                    leapsec $INPUT/leapsec.dat \
                    utcpole $INPUT/utcpole.dat \
                    geocheck_threshold 50\
                """.format(
                    PDSFILE   = 'P1540064AAAAAAAAAAAAAA12255195533001.PDS',
                    MOD01     = 'L1AAqua.hdf',
                    MODGEO    = 'GEOAqua.hdf',
                    SAT       = 'AQUA',
                    ATTFILE1  = 'P1540957AAAAAAAAAAAAAA12255195533001.att',
                    EPHFILE1  = 'P1540957AAAAAAAAAAAAAA12255195533001.eph'
                )
            ),
            products=['L1AAqua.hdf', 'GEOAqua.hdf'],
            errfiles=['errfileAquaGEO', 'errfileL1A']
        )


    def test_l0_to_l1_terra(self):
        # in-line substitutions to build up command:
        TestHelper.SPA_command( self,
            (
                ' ~/drl/SPA/modisl1db/wrapper/l0tol1'
                ' modis.pds $INPUT/P0420064AAAAAAAAAAAAAA12249171145001.PDS'
                ' modis.mxd01 $OUTPUT/L1ATerra.hdf'
                ' modis.mxd03 $OUTPUT/GEOTerra.hdf'
                ' sat '         + 'TERRA'
                ' leapsec $INPUT/leapsec.dat'
                ' utcpole $INPUT/utcpole.dat'
                ' geocheck_threshold 50'
            ),
            products=['L1ATerra.hdf', 'GEOTerra.hdf'],
            errfiles=['errfileTerraGEO', 'errfileL1A'],
        )

    # TODO: re-create these also:
    # def test_l1a_to_b_aqua(self):
    #     self._test_cmd(
    #         './run-l1atob_aqua',
    #         ['L1B1KMAqua.hdf', 'L1BHKMAqua.hdf', 'L1BQKMAqua.hdf'],
    #         ['errfileL1B']
    #     )
    #     TestHelper._cleanup_l1atob()
    #
    # def test_l1a_to_b_terra(self):
    #     self._test_cmd(
    #         './run-l1atob_terra',
    #         ['L1B1KMTerra.hdf', 'L1BHKMTerra.hdf', 'L1BQKMTerra.hdf'],
    #         ['errfileL1B']
    #     )
    #    TestHelper._cleanup_l1atob()
