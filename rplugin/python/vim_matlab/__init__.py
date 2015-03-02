import neovim
from matlab_controller import MatlabController
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
        self.controller = None

    @neovim.command('ActivateMatlabControls', sync=True)
    def activate_matlab_controls(self):
        if self.controller is not None:
            return
        self.controller = MatlabController()
        self.controller.activate_vim_window()

    @neovim.command('DeactivateMatlabControls', sync=True)
    def deactivate_matlab_controls(self):
        if self.controller is None:
            return
        self.controller.close()
        self.controller = None

    @neovim.command('RestartMatlabControls', sync=True)
    def restart_matlab_controls(self):
        self.deactivate_matlab_controls()
        self.activate_matlab_controls()

    @neovim.command('RunSelectionInMatlab', sync=True)
    def run_selection_in_matlab(self):
        if self.controller is None:
            self.activate_matlab_controls()

        lines = vim_helper.get_selection()
        self.controller.run_commands(lines)
        self.controller.activate_vim_window()

    @neovim.command('OpenInMatlab', sync=True)
    def open_in_matlab(self):
        if self.controller is None:
            self.activate_matlab_controls()

        vim_helper.save_current_buffer()
        filename = vim_helper.get_filename()
        row, col = vim_helper.get_cursor()
        self.controller.move_cursor(row, col, filename)
        self.controller.activate_editor_window()

    @neovim.command('RunMatlabCell', sync=True)
    def run_matlab_cell(self):
        if self.controller is None:
            self.activate_matlab_controls()

        vim_helper.save_current_buffer()
        filename = vim_helper.get_filename()
        row, col = vim_helper.get_cursor()
        self.controller.run_cell_at(row, col, filename)

    @neovim.command('TestMatlabControls', sync=True)
    def test_matlab_controls(self):
        if self.controller is None:
            self.activate_matlab_controls()

        self.controller.run_tests()

    @neovim.autocmd('VimLeave', pattern='*', sync=True)
    def vim_leave(self):
        if self.controller is not None:
            self.controller.close()

    @neovim.autocmd('BufEnter', pattern='*', sync=True)
    def buf_enter(self):
        self.vim.command('nnoremap <silent> gm :OpenInMatlab<CR>')
        self.vim.command('nnoremap <silent> <CR> :RunMatlabCell<CR>')
        self.vim.command(
            'vnoremap <silent> <CR> <ESC>:RunSelectionInMatlab<CR>')
