import multiprocessing
from subprocess import check_output
import subprocess
import socket
import os
import sys
import re
import Queue

import pyperclip


__author__ = 'Daeyun Shin'

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.


class MatlabController():
    def __init__(self):
        self.device_ids = self.find_device_ids()
        self.__disable_input()

        try:
            self.find_matlab_window_ids()
            self.vim_window_id = self.__get_active_window_id()

            self.__setup_matlab_path()
            self.__launch_key_request_process()
        except:
            raise Exception("Init failed: ", sys.exc_info()[0])
        finally:
            self.__enable_input()

    def __del__(self):
        self.close()

    def close(self):
        try:
            self.key_handler.terminate()
        except:
            pass

    def run_cell_at(self, row, col, filename):
        """
        Open file, move cursor to (row, col), and run cell.
        :param row, col: new cursor position in the MATLAB editor. 1-indexed.
        :param filename: absolute path to target file.
        """
        self.__disable_input()
        try:
            for _ in range(self.key_handler_queue.qsize()):
                self.key_handler_queue.get(False)
            self.move_cursor(row, col, filename, 'perform-run-cell')
            self.key_handler_queue.get(True, 5)
        except Queue.Empty:
            self.__enable_input()
        except Exception as ex:
            self.__enable_input()
            raise Exception("run_cell_at failed: ", sys.exc_info()[0])

    def run_commands(self, commands, is_invisible=False, is_multiline=True):
        """
        :param commands: list of MATLAB commands to run in Command Window.
        :param is_invisible: insert backspaces to erase Command Window if true.
        :param is_multiline: if true, delimiter will be \n, otherwise semicolon.
        """
        if is_invisible:
            command = "evalAndClean('{};');\n".format(
                ';'.join(commands).replace("'", "''"))
        else:
            delimiter = '\n' if is_multiline else ';'
            command = "{}\n".format(delimiter.join(commands))
        return self.__type_in_window(self.command_window_id, command)

    def move_cursor(self, row, col, filename, callback_name=None):
        """
        :param row, col: new cursor position in the MATLAB editor. 1-indexed.
        :param filename: open this file before moving the cursor.
        :param callback_name: MATLAB sends this TCP message back after the
        operation completes.
        :return:
        """
        set_cursor_command = 'setEditorCursor({}, {})'.format(row, col)

        if callback_name is None:
            callback_command = ''
        else:
            callback_command = "sendTcp({}, '{}')".format(
                self.key_handler_port, callback_name)

        return self.run_commands(
            ["openDocumentInEditor('{}')".format(filename), set_cursor_command,
             callback_command], True)

    def find_matlab_window_ids(self):
        """
        :rtype : list of strings
        :return: [command widow id, editor window id]
        :raise Exception:
        """
        try:
            cmd = 'xdotool search --maxdepth 4' \
                  ' --class "com-mathworks-util-PostVMInit"'
            matlab_window_ids = check_output(cmd, shell=True).strip().split()

            window_ids = [
                ("Command Window",
                 check_output('xdotool search --name "^Command Window"',
                              shell=True).strip().split()),
                ("Editor Window",
                 check_output('xdotool search --name "^Editor"',
                              shell=True).strip().split()),
            ]

        except:
            raise Exception("xdotool command failed: ", sys.exc_info()[0])

        return_value = []
        for window_name, window_id in window_ids:
            if len(window_id) == 0:
                raise Exception('Unable to find Command Window')
            elif len(window_id) > 1:
                ids = list(set(window_id).intersection(set(matlab_window_ids)))
                if len(ids) != 1:
                    raise Exception('Unable to find Command Window')
                window_id = ids
            return_value.append(window_id[0])

        self.command_window_id, self.editor_window_id = return_value
        return return_value

    def find_device_ids(self):
        """
        :return: list of all device ids from xinput, excluding XTEST devices.
        """
        t = check_output('xinput list --short', shell=True)
        id_pattern = r'id=(\d+)'
        xtest_id_pattern = r'XTEST[^\n]+id=(\d+)'
        device_ids = list(set(re.findall(id_pattern, t)).difference(
            set(re.findall(xtest_id_pattern, t))))
        return device_ids

    def run_tests(self):
        """
        "Test successful." should appear in MATLAB command window after this
        completes.
        """
        mpath = self.__find_mfile_path()
        self.run_commands(['a=42'])
        self.run_cell_at(7, 1, os.path.join(mpath, 'testVimMatlab.m'))
        self.run_cell_at(4, 1, os.path.join(mpath, 'testVimMatlab.m'))
        self.run_cell_at(1, 1, os.path.join(mpath, 'testVimMatlab.m'))
        self.run_cell_at(1, 1, os.path.join(mpath, 'testVimMatlab.m'))
        self.run_commands(['a=a+1', 'b=a+1'])
        self.run_cell_at(4, 1, os.path.join(mpath, 'testVimMatlab.m'))
        self.run_commands(['c=a+b', 'd=a+1'])
        self.run_cell_at(7, 1, os.path.join(mpath, 'testVimMatlab.m'))
        self.run_commands(['e=a+c', 'f=a+1'])
        self.run_cell_at(10, 1, os.path.join(mpath, 'testVimMatlab.m'))

    def activate_vim_window(self):
        self.__go_to_window(self.vim_window_id)

    def activate_editor_window(self):
        self.__go_to_window(self.editor_window_id)

    def activate_command_window(self):
        self.__go_to_window(self.command_window_id)

    def __launch_key_request_process(self):
        """
        Pick an unused port and start a TCP server. MATLAB will send callback
        requests through this socket.
        :return: port
        """
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.bind(('localhost', 0))
        _, self.key_handler_port = sock.getsockname()

        self.key_handler_queue = multiprocessing.Queue()
        self.key_handler = multiprocessing.Process(
            target=self.__key_request_handler,
            args=(sock,
                  [self.command_window_id,
                   self.editor_window_id,
                   self.vim_window_id],
                  self.key_handler_queue)
        )
        self.key_handler.start()
        self.key_handler_queue.get(True, 5)
        return self.key_handler_port

    def __key_request_handler(self, sock, window_ids, queue):
        """
        Routine for a process that handles key press requests from MATLAB.
        :param port:
        :param window_ids: [command window, editor window, vim window]
        :param queue:
        """
        sock.listen(1)
        queue.put(True)
        while True:
            client_sock, _ = sock.accept()
            msg = client_sock.recv(1024).strip()
            if msg == 'perform-run-cell':
                self.__go_to_window(window_ids[0])
                self.__go_to_window(window_ids[1])
                self.__enter_keys(['Ctrl+KP_Enter'])
                self.__go_to_window(window_ids[2])
                self.__enable_input()
                queue.put(True)
            client_sock.close()
        sock.close()

    def __disable_input(self):
        try:
            check_output(
                ';'.join(
                    ["xinput disable {}".format(id) for id in self.device_ids]),
                shell=True, stderr=subprocess.STDOUT)
        except:
            pass

    def __enable_input(self):
        try:
            check_output(
                ';'.join(
                    ["xinput enable {}".format(id) for id in self.device_ids]),
                shell=True, stderr=subprocess.STDOUT)
        except:
            pass

    def __go_to_window(self, window_id):
        cmd = 'xdotool windowactivate --sync {};'.format(window_id)
        return check_output(cmd, shell=True, stderr=subprocess.STDOUT)

    def __enter_keys_in_window(self, window_id, keys):
        cmd = "xdotool windowactivate --sync " \
              "{} key --clearmodifiers {};".format(window_id, ' '.join(
            [("'{}'".format(w)) for w in keys]))
        try:
            result = check_output(cmd, shell=True, stderr=subprocess.STDOUT)
        except subprocess.CalledProcessError as ex:
            if ex.returncode == 1 and 'BadWindow' in ex.output:
                raise ValueError('Invalid window ID.')
            result = None
        return result

    def __enter_keys(self, keys):
        cmd = 'xdotool key --clearmodifiers {};'.format(
            ' '.join([("'{}'".format(w)) for w in keys]))
        return check_output(cmd, shell=True, stderr=subprocess.STDOUT)

    def __type_in_window(self, window_id, string):
        pyperclip.copy(string)
        return self.__enter_keys_in_window(window_id, ['Ctrl+y'])

    def __get_active_window_id(self):
        return check_output('xdotool getactivewindow', shell=True).strip()

    def __setup_matlab_path(self):
        mpath = self.__find_mfile_path()
        self.run_commands(["addpath(genpath('{}'))".format(mpath)], False)

    def __find_mfile_path(self):
        return os.path.abspath(os.path.join(__file__, '../matlab'))
