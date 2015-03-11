import random
import re
from functools import wraps
import threading
from command import Command
import sh


__author__ = 'daeyun'


class InputController():
    device_ids = None
    stack = []
    lock = threading.Lock()

    def __init__(self, timeout=3):
        if InputController.device_ids is None:
            InputController.device_ids = self.find_device_ids()
            if len(InputController.device_ids) < 1:
                raise RuntimeError('Unable to find input devices.')

    def find_device_ids(self):
        """
        :return: list of all device ids from xinput, excluding XTEST devices.
        """
        device_info = str(sh.xinput('list', '--short'))
        id_pattern = r'id=(\d+)'
        xtest_id_pattern = r'XTEST[^\n]+id=(\d+)'
        device_ids = list(set(re.findall(id_pattern, device_info)).difference(
            set(re.findall(xtest_id_pattern, device_info))))
        return device_ids

    def disable_input(self):
        with InputController.lock:
            if not InputController.stack:
                try:
                    for id in self.device_ids:
                        cmd = ';'.join(['xinput disable {}'.format(id) for id in
                                        self.device_ids])
                        Command(cmd).run(1)
                except:
                    pass

            key = random.getrandbits(64)
            InputController.stack.append(key)
        return key

    def enable_input(self, key):
        with InputController.lock:
            if key in InputController.stack:
                ind = InputController.stack.index(key)
                InputController.stack = InputController.stack[:ind]

                if not InputController.stack:
                    try:
                        cmd = ';'.join(['xinput enable {}'.format(id) for id in
                                        self.device_ids])
                        Command(cmd).run(1)
                    except:
                        pass


def disable_input(func):
    def wrapper(*args, **kwargs):
        input_controller = InputController()
        try:
            key = input_controller.disable_input()
            result = func(*args, **kwargs)
        finally:
            input_controller.enable_input(key)
        return result

    return wraps(func)(wrapper)

