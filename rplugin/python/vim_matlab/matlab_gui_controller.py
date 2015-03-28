import multiprocessing
from subprocess import check_output
import socket
import os
import re

import pyperclip

from input_controller import disable_input
from xdotool import Xdotool


__author__ = 'Daeyun Shin'

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.


class MatlabGuiController():
    @disable_input
    def __init__(self):
        self.device_ids = self.find_device_ids()
        self.xdotool = Xdotool()
        self.vim_window_id = self.xdotool.get_active_window_id()
        self.find_matlab_window_ids()
        self.__setup_matlab_path()
        self.__launch_key_request_process()

    def __del__(self):
        self.close()

    def close(self):
        try:
            self.key_handler.terminate()
            self.sock.close()
        except:
            pass

    @disable_input
    def run_cell_at(self, row, col, filename):
        """
        Open file, move cursor to (row, col), and run cell.
        :param row, col: new cursor position in the MATLAB editor. 1-indexed.
        :param filename: absolute path to target file.
        """
        for _ in range(self.key_handler_queue.qsize()):
            self.key_handler_queue.get(False)
        self.move_cursor(row, col, filename, 'perform-run-cell')
        self.key_handler_queue.get(True, 5)

    @disable_input
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

    @disable_input
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
        self.command_window_id = self.xdotool. \
            find_windows('^Command Window', 'com-mathworks-util-PostVMInit')[0]

        self.editor_window_id = self.xdotool. \
            find_windows('^Editor', 'com-mathworks-util-PostVMInit')[0]

        return self.editor_window_id, self.command_window_id

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

    @disable_input
    def activate_vim_window(self):
        self.xdotool.activate_window(self.vim_window_id)

    @disable_input
    def activate_editor_window(self):
        self.xdotool.activate_window(self.editor_window_id)

    @disable_input
    def activate_command_window(self):
        self.xdotool.activate_window(self.command_window_id)

    def find_mfile_path(self):
        return os.path.abspath(os.path.join(__file__, '../matlab'))

    def __launch_key_request_process(self):
        """
        Pick an unused port and start a TCP server. MATLAB will send callback
        requests through this socket.
        :return: port
        """
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.bind(('localhost', 0))
        _, self.key_handler_port = self.sock.getsockname()

        self.key_handler_queue = multiprocessing.Queue()
        self.key_handler = multiprocessing.Process(
            target=self.__key_request_handler,
            args=(self.sock,
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
                self.xdotool.activate_window(window_ids[0])
                self.xdotool.activate_window(window_ids[1])
                self.xdotool.enter_keys(['Ctrl+KP_Enter'])
                self.xdotool.activate_window(window_ids[2])
                queue.put(True)
            client_sock.close()
        sock.close()

    @disable_input
    def __type_in_window(self, window_id, string):
        pyperclip.copy(string)
        self.xdotool.enter_keys(['Ctrl+y'], window_id)

    @disable_input
    def __setup_matlab_path(self):
        mpath = self.find_mfile_path()
        self.run_commands(["addpath(genpath('{}'))".format(mpath)], False)
