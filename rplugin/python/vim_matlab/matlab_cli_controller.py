import time
from threading import Timer

from io_helper import find_plugin_matlab_path


__author__ = 'daeyun'

import socket
import logger


class MatlabCliController:
    def __init__(self):
        self.host, self.port = "localhost", 43889
        self.connect_to_server()

    def connect_to_server(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((self.host, self.port))
        Timer(5, self.setup_matlab_path).start()

    def run_code(self, lines):
        code = ','.join(lines)

        num_retry = 0
        while num_retry < 3:
            try:
                self.sock.sendall(code + "\n")
                logger.log.info(code)
                break
            except Exception as ex:
                logger.log.error(ex)
                self.connect_to_server()
                num_retry += 1
                time.sleep(1)

    def setup_matlab_path(self):
        mpath = find_plugin_matlab_path()
        self.run_code(["addpath(genpath('{}'));".format(mpath)])

    def open_in_matlab_editor(self, path):
        self.run_code(["edit {};".format(path)])

    def open_workspace(self):
        self.run_code(["workspace;"])

    def openvar(self, name):
        self.run_code(["openvar {};".format(name)])

    def help_command(self, name):
        self.run_code(["help {};".format(name)])

    def send_ctrl_c(self):
        self.sock.sendall("cancel\n")
