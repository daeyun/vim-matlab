import hashlib
import os
import datetime
import errno
import re
import time
import collections

import neovim

from . import matlab_cli_controller
from matlab_cli_controller import MatlabCliController
from python_vim_utils import PythonVimUtils as vim_helper
import python_vim_utils


__created__ = 'Mar 01, 2015'
__license__ = 'MPL 2.0'
__author__ = 'Daeyun Shin'
__email__ = "daeyun@daeyunshin.com"

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
        self.buffer_state = collections.defaultdict(dict)

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

        self.matlab_write_function_files()

        lines = vim_helper.get_selection(ignore_matlab_comments=True)
        self.cli_controller.run_code(lines)

    @neovim.command('MatlabCliRunLine', sync=True)
    def run_current_line(self):
        if self.cli_controller is None:
            self.activate_cli()

        self.matlab_write_function_files()

        line = [vim_helper.get_current_matlab_line()]
        self.cli_controller.run_code(line)

    @neovim.command('MatlabCliRunCell', sync=True)
    def run_cell_in_matlab_cli(self):
        if self.cli_controller is None:
            self.activate_cli()

        self.matlab_write_function_files()

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
    def matlab_cli_cancel(self):
        if self.cli_controller is None:
            self.activate_cli()
        self.cli_controller.send_ctrl_c()

    @neovim.command('MatlabCliOpenInMatlabEditor', sync=True)
    def matlab_cli_open_in_matlab_editor(self):
        if self.cli_controller is None:
            self.activate_cli()
        path = vim_helper.get_current_file_path()
        self.cli_controller.open_in_matlab_editor(path)

    @neovim.command('MatlabCliOpenWorkspace', sync=True)
    def matlab_cli_open_workspace(self):
        if self.cli_controller is None:
            self.activate_cli()
        self.cli_controller.open_workspace()

    @neovim.command('MatlabCliHelp', sync=True)
    def matlab_cli_help(self):
        if self.cli_controller is None:
            self.activate_cli()
        var = vim_helper.get_variable_under_cursor()
        self.cli_controller.help_command(var)

    @neovim.command('MatlabCliOpenVar', sync=True)
    def matlab_cli_open_var(self):
        if self.cli_controller is None:
            self.activate_cli()
        var = vim_helper.get_variable_under_cursor()
        self.cli_controller.openvar(var)

    @neovim.command('MatlabWriteFunctionFiles', sync=True)
    def matlab_write_function_files(self):
        options = vim_helper.get_options()
        if 'split' in options:
            group_name = options['split'][0]
        else:
            return

        dir_path = os.path.join(
            os.path.dirname(vim_helper.get_current_file_path()), group_name)
        if not os.path.exists(dir_path):
            os.mkdir(dir_path)

        existing_filenames = [name for name in os.listdir(dir_path) if
                              name.endswith('.m')]

        function_blocks = vim_helper.get_function_blocks()
        new_filenames = [name + '.m' for name in function_blocks.keys()]

        unused_filenames = list(set(existing_filenames) - set(new_filenames))
        for name in unused_filenames:
            try:
                os.remove(os.path.join(dir_path, name))
            except:
                pass

        added_filenames = list(set(new_filenames) - set(existing_filenames))
        for name in added_filenames:
            content = function_blocks[os.path.splitext(name)[0]].strip()
            with open(os.path.join(dir_path, name), 'w') as f:
                f.write(content)

        common_filenames = set.intersection(
            *[set(existing_filenames), set(new_filenames)])
        for name in common_filenames:
            content = function_blocks[os.path.splitext(name)[0]].strip()
            code_hash = hashlib.md5(content).hexdigest()
            with open(os.path.join(dir_path, name), 'r+') as f:
                file_hash = hashlib.md5(f.read().strip()).hexdigest()
                f.seek(0)
                if code_hash != file_hash:
                    f.write(content)
                    f.truncate()


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

    @neovim.autocmd('InsertEnter', pattern='*.m')
    def insert_enter(self):
        self.refresh_buffer()

    @neovim.autocmd('BufEnter', pattern='*.m')
    def buf_enter(self):
        self.set_last_written()

    @neovim.autocmd('BufDelete', pattern='*.m')
    def buf_delete(self):
        path = vim_helper.get_current_file_path()
        self.buffer_state.pop(path, None)

    @neovim.autocmd('BufWrite', pattern='*.m', sync=True)
    def buf_write(self):
        self.set_last_written()
        self.matlab_write_function_files()

    def set_last_written(self):
        path = vim_helper.get_current_file_path()
        self.buffer_state[path]['last_written'] = time.time()

    def refresh_buffer(self):
        path = vim_helper.get_current_file_path()
        last_written = self.buffer_state[path]['last_written']
        if time.time() - last_written < 1 or not os.path.isfile(path):
            return

        modified = os.stat(path).st_mtime

        if modified > last_written + 8:
            row_col = vim_helper.get_cursor()
            vim_helper.edit_file(path)
            vim_helper.set_cursor(row_col)

