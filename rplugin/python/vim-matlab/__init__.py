import neovim
from matlab_controller import MatlabController

__date__ = 'Mar 01, 2015'
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

    @neovim.command('ActivateMatlabControls', sync=True)
    def activate_matlab_controls(self):
        self.controller = MatlabController()

    @neovim.command('TestMatlabControls', sync=True)
    def test_matlab_controls(self):
        self.controller.run_tests()

    @neovim.autocmd('BufEnter', pattern='*', sync=True)
    def buf_enter(self):
        self.vim.command('nnoremap <CR> :HelloWorld<CR>')
