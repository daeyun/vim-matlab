import os

__author__ = 'daeyun'


def find_plugin_matlab_path():
    return os.path.abspath(os.path.join(__file__, '../matlab'))