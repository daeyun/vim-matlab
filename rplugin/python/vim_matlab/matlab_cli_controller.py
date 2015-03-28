import re
import time

__author__ = 'daeyun'

import socket
import logger

import python_vim_utils

class MatlabCliController:
    def __init__(self):
        self.host, self.port = "localhost", 43889
        self.connect_to_server()

    def connect_to_server(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((self.host, self.port))

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
