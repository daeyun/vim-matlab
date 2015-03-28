#!/usr/bin/env python2

__author__ = 'daeyun'

from subprocess import Popen, PIPE
import signal
import os
import SocketServer
import time
import random
import string


class Matlab:
    def __init__(self):
        self.proc = self.launch_process()

    def launch_process(self):
        self.kill()
        return Popen(["matlab", "-nosplash", "-nodesktop"], stdin=PIPE,
                     shell=True, close_fds=True, preexec_fn=os.setsid)

    def kill(self):
        try:
            os.killpg(self.proc.pid, signal.SIGTERM)
        except:
            pass

    def run_code(self, code, run_timer=True):
        num_retry = 0
        rand_var = ''.join(
            random.choice(string.ascii_uppercase) for _ in range(12))
        while num_retry < 3:
            try:
                if run_timer:
                    self.proc.stdin.write(
                        "{}=tic;{},toc({});\n".format(rand_var, code.strip(),
                                                      rand_var))
                else:
                    self.proc.stdin.write(
                        "{}\n".format(code.strip()))
                self.proc.stdin.flush()
                break
            except Exception as ex:
                print ex
                self.proc = self.launch_process()
                num_retry += 1
                time.sleep(1)


class TCPHandler(SocketServer.StreamRequestHandler):
    def handle(self):
        print "New connection: {}".format(self.client_address)

        while True:
            msg = self.rfile.readline()
            print (msg[:74] + '...') if len(msg) > 74 else msg
            if not msg:
                break
            msg = msg.strip()
            options = {
                'kill': self.server.matlab.kill,
                'restart': self.server.matlab.launch_process,
            }

            if msg in options:
                options[msg]()
            else:
                self.server.matlab.run_code(msg)
        print 'Connection closed: {}'.format(self.client_address)


def main():
    host, port = "localhost", 43889
    SocketServer.TCPServer.allow_reuse_address = True
    server = SocketServer.TCPServer((host, port), TCPHandler)
    server.matlab = Matlab()

    print "Started server: {}".format((host, port))
    server.serve_forever()


if __name__ == "__main__":
    main()
