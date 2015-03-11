import os
from unittest import TestCase
import matlab_controller

__author__ = 'daeyun'


class TestMatlabController(TestCase):
    def setUp(self):
        self.controller = matlab_controller.MatlabController()
        self.controller.activate_vim_window()

    def tearDown(self):
        self.controller.close()

    def test_window_switching(self):
        """
        "Test successful." should appear in MATLAB command window after this
        completes.
        """
        mpath = self.controller.find_mfile_path()
        self.controller.run_commands(['a=0'])
        self.controller.run_cell_at(1, 1, os.path.join(mpath, 'testVimMatlab.m'))
        self.controller.run_cell_at(4, 1, os.path.join(mpath, 'testVimMatlab.m'))
        self.controller.run_cell_at(8, 1, os.path.join(mpath, 'testVimMatlab.m'))
        self.controller.run_cell_at(13, 1, os.path.join(mpath, 'testVimMatlab.m'))
        self.controller.run_commands(['a=0'])
        self.controller.run_cell_at(4, 1, os.path.join(mpath, 'testVimMatlab.m'))
        self.controller.run_cell_at(8, 1, os.path.join(mpath, 'testVimMatlab.m'))
        self.controller.run_cell_at(16, 1, os.path.join(mpath, 'testVimMatlab.m'))