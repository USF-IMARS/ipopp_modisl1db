#!/usr/bin/env python

# std modules:
import os
import shutil
import unittest
import subprocess

from nose.tools import nottest

from StationTester import test_helper, path_helper

 # NOTE: @nottest disables usage from nosetests b/c these tests are not
 #          properly sandboxed. They fail if run from outside of testscripts,
#           and they spew files all over the cwd.
@nottest
class Test_modisl1db_usingBashScripts(unittest.TestCase):
    def setUp(self):
        test_helper.SPATestSetUp()

    def tearDown(self):
        test_helper.SPATestTearDown()
        self._del_errfiles()
        self._del_stdfiles()
        self._cleanup_l1atob()

    def _run_bash_test(self, script, products, errfiles):
        subprocess.call(script, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        test_helper._expect_empty_errfiles(self, errfiles, path_helper.testscriptdir)
        test_helper._expect_files(self, products, path_helper._outdir)


    def _del_errfiles(self):
        print("rm errfile*...")
        filelist = [ f for f in os.listdir(path_helper.testscriptdir) if f.startswith('errfile')]
        for f in filelist:
            os.remove(os.path.join(path_helper.testscriptdir, f))

    def _del_stdfiles(self):
        print("rm stdfile*...")
        filelist = [ f for f in os.listdir(path_helper.testscriptdir) if f.startswith('stdfile')]
        for f in filelist:
            os.remove(os.path.join(path_helper.testscriptdir, f))

    def _cleanup_l1atob(self):
        print("rm {*hdf, *pcf}...")
        filelist = ([
            f for f in os.listdir(path_helper.testscriptdir)
            if (
                f.endswith('.hdf') or
                f.endswith('.pcf')
            )
        ])
        for f in filelist:
            os.remove(os.path.join(path_helper.testscriptdir, f))

        print("rm *_logs-pcf/...")
        folderlist = ([f for f in os.listdir(path_helper.testscriptdir) if f.endswith('_logs-pcf')])
        for f in folderlist:
            shutil.rmtree(os.path.join(path_helper.testscriptdir, f))


    # tests:
    ##################################
    def test_l0_to_l1_aqua(self):
        self._run_bash_test(
            './run-l0tol1_aqua',
            ['L1AAqua.hdf', 'GEOAqua.hdf'],
            ['errfileAquaGEO', 'errfileL1A']
        )

    def test_l0_to_l1_terra(self):
        self._run_bash_test(
            './run-l0tol1_terra',
            ['L1ATerra.hdf', 'GEOTerra.hdf'],
            ['errfileTerraGEO', 'errfileL1A']
        )

    def test_l1a_to_b_aqua(self):
        self._run_bash_test(
            './run-l1atob_aqua',
            ['L1B1KMAqua.hdf', 'L1BHKMAqua.hdf', 'L1BQKMAqua.hdf'],
            ['errfileL1B']
        )

    def test_l1a_to_b_terra(self):
        self._run_bash_test(
            './run-l1atob_terra',
            ['L1B1KMTerra.hdf', 'L1BHKMTerra.hdf', 'L1BQKMTerra.hdf'],
            ['errfileL1B']
        )
