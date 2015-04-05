import os
import datetime
import errno
import re

import neovim

from matlab_gui_controller import MatlabGuiController
from matlab_cli_controller import MatlabCliController
from python_vim_utils import PythonVimUtils as vim_helper
import python_vim_utils


__created__ = 'Mar 01, 2015'
__license__ = 'MPL 2.0'
__author__ = 'Daeyun Shin'
__email__ = "daeyun@daeyunshin.com"
__version__ = '0.1'

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

@neovim.plugin
class VimMatlab(object):
    def __init__(self, vim):
        self.vim = vim
        python_vim_utils.vim = vim
        self.gui_controller = None
        self.cli_controller = None

        self.function_name_pattern = \
            re.compile(r'((?:^|\n[ \t]*)(?!%)[ \t]*(?:function(?:[ \t]|\.\.\.'
                       r'[ \t]*\n)(?:[^\(\n]|\.\.\.[ \t]*\n)*?|classdef(?:[ \t]'
                       r'|\.\.\.[ \t]*\n)(?:[^\<\n]|\.\.\.[ \t]*\n)*?))('
                       r'[a-zA-Z]\w*)((?:[ \t]|\.\.\.[ \t]*\n)*(?:\(|\<|\n|$))')

    @neovim.command('MatlabPrintCellLines', sync=True)
    def run_print_cell_lines(self):
        lines = vim_helper.get_current_matlab_cell_lines(
            ignore_matlab_comments=True)
        vim_helper.echo_text("\n".join(lines))

    @neovim.command('MatlabCliRunSelection', sync=True)
    def run_selection_in_matlab_cli(self):
        if self.cli_controller is None:
            self.activate_cli()

        lines = vim_helper.get_selection(ignore_matlab_comments=True)
        self.cli_controller.run_code(lines)

    @neovim.command('MatlabCliRunCell', sync=True)
    def run_cell_in_matlab_cli(self):
        if self.cli_controller is None:
            self.activate_cli()

        lines = vim_helper.get_current_matlab_cell_lines(
            ignore_matlab_comments=True)
        self.cli_controller.run_code(lines)

    @neovim.command('MatlabCliActivateControls', sync=True)
    def activate_cli(self):
        if self.cli_controller is not None:
            return
        self.cli_controller = MatlabCliController()

    @neovim.command('MatlabCliViewVarUnderCursor', sync=True)
    def view_var_under_cursor(self):
        if self.cli_controller is None:
            self.activate_cli()
        var = vim_helper.get_variable_under_cursor()
        if var:
            self.cli_controller.run_code(['printVarInfo({});'.format(var)])

    @neovim.command('MatlabCliViewSelectedVar', sync=True)
    def view_selected_var(self):
        if self.cli_controller is None:
            self.activate_cli()
        var = vim_helper.get_selection()
        if var:
            self.cli_controller.run_code(['printVarInfo({});'.format(var)])

    @neovim.command('MatlabCliCancel', sync=True)
    def view_selected_var(self):
        if self.cli_controller is None:
            self.activate_cli()
        self.cli_controller.send_ctrl_c()

    @neovim.command('MatlabGuiActivateControls', sync=True)
    def activate(self):
        if self.gui_controller is not None:
            return
        self.gui_controller = MatlabGuiController()
        self.gui_controller.activate_vim_window()

    @neovim.command('MatlabGuiDeativateControls', sync=True)
    def deactivate(self):
        if self.gui_controller is None:
            return
        self.gui_controller.close()
        self.gui_controller = None

    @neovim.command('MatlabGuiRestartControls', sync=True)
    def restart(self):
        self.deactivate()
        self.activate()

    @neovim.command('MatlabGuiRunSelection', sync=True)
    def run_selection_in_matlab(self):
        if self.gui_controller is None:
            self.activate()

        lines = vim_helper.get_selection()
        self.gui_controller.run_commands(lines)
        self.gui_controller.activate_vim_window()

    @neovim.command('MatlabGuiOpenInEditor', sync=True)
    def open_in_matlab(self):
        if self.gui_controller is None:
            self.activate()

        vim_helper.save_current_buffer()
        filename = vim_helper.get_current_file_path()
        row, col = vim_helper.get_cursor()
        self.gui_controller.move_cursor(row, col, filename)
        self.gui_controller.activate_command_window()
        self.gui_controller.activate_editor_window()

    @neovim.command('MatlabGuiRunCell', sync=True)
    def run_matlab_cell(self):
        if self.gui_controller is None:
            self.activate()

        vim_helper.save_current_buffer()
        filename = vim_helper.get_current_file_path()
        row, col = vim_helper.get_cursor()
        self.gui_controller.run_cell_at(row, col, filename)

    @neovim.command('MatlabOpenTempScript', sync=True, nargs='*')
    def open_temp_matlab_script(self, args):
        dirname = os.path.join(os.path.expanduser('~'), '.vim-matlab/scratch/')
        if not os.path.exists(dirname):
            try:
                os.makedirs(dirname)
            except OSError as ex:
                # In case of a race condition
                if ex.errno != errno.EEXIST:
                    raise
        timestamp = datetime.datetime.now().strftime("%Y_%m_%d_%H_%M_%S")
        if len(args) > 0:
            filename = "{}_{}.m".format(timestamp, args[0])
        else:
            filename = "{}.m".format(timestamp)
        self.vim.command('edit {}'.format(os.path.join(dirname, filename)))

    @neovim.command('MatlabRename', sync=True, nargs='1')
    def rename(self, args):
        self.fix_name(args)

    @neovim.command('MatlabFixName', sync=True, nargs='*')
    def fix_name(self, args):
        curr_file = vim_helper.get_current_file_path()
        modified = os.path.getmtime(curr_file)
        changed = os.path.getctime(curr_file)
        head_lines = self.vim.current.buffer[:100]
        head_string = '\n'.join(head_lines)

        def get_basename_ext(path):
            filename = os.path.basename(path)
            return os.path.splitext(filename)

        def rename_function(name):
            new_head = self.function_name_pattern.sub(
                r"\1{}\3".format(name), head_string).split('\n')
            for i, line in enumerate(new_head):
                if line != head_lines[i]:
                    self.vim.current.buffer[i] = line

        basename, ext = get_basename_ext(curr_file)

        if len(args) > 0:
            new_name, new_ext = get_basename_ext(args[0])
            new_ext = new_ext if len(new_ext) > 0 else ext
            rename_function(new_name)
            self.vim.command("Rename {}{}".format(new_name, new_ext))
            return

        if vim_helper.is_current_buffer_modified() or changed != modified:
            match = self.function_name_pattern.search(head_string)
            if match is None:
                return
            function_name = match.group(2)
            self.vim.command("Rename {}{}".format(function_name, ext))
        else:
            rename_function(basename)

    @neovim.autocmd('VimLeave', pattern='*', sync=True)
    def vim_leave(self):
        if self.gui_controller is not None:
            self.gui_controller.close()

    @neovim.autocmd('BufEnter', pattern='*.m', sync=True)
    def buf_enter(self):
        pass


