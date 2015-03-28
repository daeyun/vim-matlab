import subprocess
import threading

import logger


__author__ = 'daeyun'


class TimeoutError(Exception):
    pass


class Command(object):
    def __init__(self, cmd):
        self.cmd = cmd
        self.process = None
        self.stdout = None
        self.stderr = None

    def run(self, timeout=None):
        def target():
            self.process = subprocess.Popen(self.cmd, shell=True,
                                            close_fds=True,
                                            stdout=subprocess.PIPE,
                                            stderr=subprocess.PIPE)
            self.stdout, self.stderr = self.process.communicate()

        thread = threading.Thread(target=target)
        thread.start()

        thread.join(timeout)
        if thread.is_alive():
            self.process.terminate()
            thread.join()
            logger.log.error('Timeout: ' + self.cmd)
            raise TimeoutError('Timeout: ' + self.cmd + ' ' + logger.log_path)
        return self.stdout, self.stderr, self.process.returncode
