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
                {WRAP_HOME}/run \
                    /home/ipopp/drl/SPA/modisl1db/wrapper/l0tol1 \
                    modis.pds {IN_DIR}/{PDSFILE} \
                    modis.mxd01 {OUT_DIR}/{MOD01} \
                    modis.mxd03 {OUT_DIR}/{MODGEO} \
                    sat {SAT} \
                    gbad_att {IN_DIR}/{ATTFILE1} \
                    gbad_eph {IN_DIR}/{EPHFILE1} \
                    leapsec {IN_DIR}/leapsec.dat \
                    utcpole {IN_DIR}/utcpole.dat \
                    geocheck_threshold 50\
                """.format(
                    WRAP_HOME = TestHelper.wrapper_home,
                    IN_DIR    = TestHelper.testindir,
                    OUT_DIR   = TestHelper.testoutdir,
                    PDSFILE   = 'P1540064AAAAAAAAAAAAAA12255195533001.PDS',
                    MOD01     = 'L1AAqua.hdf',
                    MODGEO    = 'GEOAqua.hdf',
                    SAT       = 'AQUA',
                    ATTFILE1  = 'P1540957AAAAAAAAAAAAAA12255195533001.att',
                    EPHFILE1  = 'P1540957AAAAAAAAAAAAAA12255195533001.eph'
                )
            ),
            ['L1AAqua.hdf', 'GEOAqua.hdf'],
            ['errfileAquaGEO', 'errfileL1A'],
            0
        )


    def test_l0_to_l1_terra(self):
        # in-line substitutions to build up command:
        TestHelper.SPA_command( self,
            (
                TestHelper.wrapper_home+'/run'
                ' /home/ipopp/drl/SPA/modisl1db/wrapper/l0tol1'
                ' modis.pds '   + TestHelper.testindir  + '/P0420064AAAAAAAAAAAAAA12249171145001.PDS'
                ' modis.mxd01 ' + TestHelper.testoutdir + '/L1ATerra.hdf'
                ' modis.mxd03 ' + TestHelper.testoutdir + '/GEOTerra.hdf'
                ' sat '         + 'TERRA'
                ' leapsec '     + TestHelper.testindir  + '/leapsec.dat'
                ' utcpole '     + TestHelper.testindir  + '/utcpole.dat'
                ' geocheck_threshold 50'
            ),
            ['L1ATerra.hdf', 'GEOTerra.hdf'],
            ['errfileTerraGEO', 'errfileL1A'],
            0
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
