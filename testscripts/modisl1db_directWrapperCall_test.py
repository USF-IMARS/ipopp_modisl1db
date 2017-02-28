#!/usr/bin/env python

"""
Re-creates tests from modisl1db_usingBashScripts_tests but directly calls the
wrapper from python and does not depend on the run-* bash scripts.

NOTE: l1atob tests NOT re-created.
"""

import os
import shutil
import unittest
import subprocess

# static helpers (common w/ other test classes):
###########################################################
class helper:
    wrapper_home = '/home/ipopp/drl/station-tester/wrapper/lib'
    testoutdir = "../testdata/output"
    testindir = "../testdata/input"
    testscriptdir = "./"
    FNULL = open(os.devnull, 'w')

    @staticmethod
    def _del_testdata_out():
        print("rm test output...")
        filelist = [ f for f in os.listdir(helper.testoutdir) ]
        for f in filelist:
            os.remove(os.path.join(helper.testoutdir, f))

    @staticmethod
    def _del_errfiles():
        print("rm errfile*...")
        filelist = [ f for f in os.listdir(helper.testscriptdir) if f.startswith('errfile')]
        for f in filelist:
            os.remove(os.path.join(helper.testscriptdir, f))

    @staticmethod
    def _del_stdfiles():
        print("rm stdfile*...")
        filelist = [ f for f in os.listdir(helper.testscriptdir) if f.startswith('stdfile')]
        for f in filelist:
            os.remove(os.path.join(helper.testscriptdir, f))

    @staticmethod
    def _cleanup_l1atob():
        print("rm {*hdf, *pcf}...")
        filelist = ([
            f for f in os.listdir(helper.testscriptdir)
            if (
                f.endswith('.hdf') or
                f.endswith('.pcf')
            )
        ])
        for f in filelist:
            os.remove(os.path.join(helper.testscriptdir, f))

        print("rm *_logs-pcf/...")
        folderlist = ([f for f in os.listdir(helper.testscriptdir) if f.endswith('_logs-pcf')])
        for f in folderlist:
            shutil.rmtree(os.path.join(helper.testscriptdir, f))

    @staticmethod
    def file_is_empty(filename):
        return os.stat(filename).st_size == 0

    @staticmethod
    def clean():
        helper._del_testdata_out()
        helper._del_errfiles()
        helper._del_stdfiles()
        helper._cleanup_l1atob()

    @staticmethod
    def mySetup():
        print ("test setup.")
        helper.clean()

    @staticmethod
    def myTeardown():
        print ("test clean up.")
        helper.clean()

    @staticmethod
    def test_products_and_errfiles(testClass, products, errfiles):
        # assert expected product exists
        for expected_product in products:
            # print(expected_product, '?')
            testClass.assertTrue(
                os.path.exists(os.path.join(helper.testoutdir, expected_product)),
                'expected product: "' + expected_product + '" not found.'
            )
        # assert no errs in errfiles
        for errfile in errfiles:
            # print(errfile, '?')
            testClass.assertTrue(
                helper.file_is_empty(errfile),
                'errfile "' + errfile + '" not empty.'
            )


class Test_modisl1db_directWrapperCall(unittest.TestCase):

    def setup(self):
        helper.mySetup()

    def teardown(self):
        helper.myTeardown()

    def _test_cmd(self, command, products, errfiles, expected_return_value):
        print(command)
        return_value = subprocess.call(  # use check_call to check for malformed command
            command, shell=True, stdout=helper.FNULL, stderr=subprocess.STDOUT
        )

        helper.test_products_and_errfiles(self, products, errfiles)

        self.assertEquals(return_value, expected_return_value)

    # tests:
    #########################
    def test_l0_to_l1_aqua(self):
        # using "".format() kwargs to make command:
        self._test_cmd(
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
                    WRAP_HOME = helper.wrapper_home,
                    IN_DIR    = helper.testindir,
                    OUT_DIR   = helper.testoutdir,
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
        self._test_cmd(
            (
                helper.wrapper_home+'/run'
                ' /home/ipopp/drl/SPA/modisl1db/wrapper/l0tol1'
                ' modis.pds '   + helper.testindir  + '/P0420064AAAAAAAAAAAAAA12249171145001.PDS'
                ' modis.mxd01 ' + helper.testoutdir + '/L1ATerra.hdf'
                ' modis.mxd03 ' + helper.testoutdir + '/GEOTerra.hdf'
                ' sat '         + 'TERRA'
                ' leapsec '     + helper.testindir  + '/leapsec.dat'
                ' utcpole '     + helper.testindir  + '/utcpole.dat'
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
    #     helper._cleanup_l1atob()
    #
    # def test_l1a_to_b_terra(self):
    #     self._test_cmd(
    #         './run-l1atob_terra',
    #         ['L1B1KMTerra.hdf', 'L1BHKMTerra.hdf', 'L1BQKMTerra.hdf'],
    #         ['errfileL1B']
    #     )
    #    helper._cleanup_l1atob()
