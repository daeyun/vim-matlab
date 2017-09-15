vim-matlab
===========

An alternative to Matlab's default editor for Vim users.

### FAQ

##### How do I run code cells (`%%` blocks)?

In Normal mode, press `<Enter>` or `<C-m>`. The editor will parse the code in the current cell and send to MATLAB for evaluation.

##### What if I need MATLAB's GUI features?

Most MATLAB windows can be launched through commands; even in `-nodisplay` mode. For example, [workspace](https://www.mathworks.com/help/matlab/ref/workspace.html) command opens the Workspace browser.

<img width="400" alt="screenshot 2016-08-18 20 57 56" src="https://cloud.githubusercontent.com/assets/1250682/17795452/82df34fe-6586-11e6-8049-6fc6712c9b0e.png">

If you need to access the debugger, use [edit](https://www.mathworks.com/help/matlab/ref/edit.html) to open the default GUI editor.


### Usage

`vim-matlab` works by remotely controlling a CLI Matlab instance (launched by `vim-matlab-server.py`).

Run

```
./scripts/vim-matlab-server.py
```

This will start a Matlab REPL and redirect commands received from Vim to Matlab. When Matlab crashes (e.g. segfault during MEX development), it will launch another process.

Then open Vim in another terminal and start editing .m files.

Alternatively, launch a server instance from Vim using `:MatlabLaunchServer`. The server will be launched either in a Neovim terminal buffer or a tmux split (see [g:matlab_server_launcher](#configuration)).

- `:MatlabCliCancel` (\<leader\>c) tells the server to send SIGINT to Matlab, canceling current operation.

- `:MatlabCliRunSelection` executes the highlighted Matlab code.

- `:MatlabCliRunCell` executes code in the current cell — i.e. `%%` blocks. Similar to Ctrl-Enter in the Matlab editor.

- `:MatlabCliOpenInEditor` (,e) opens current buffer in a Matlab editor window. e.g. to access the debugger.

- `:MatlabCliHelp` (,h) prints help message for the word under the cursor.

- `:MatlabNormalModeCreateCell` (C-l) inserts a cell marker above the current line.

- `:MatlabVisualModeCreateCell` (C-l) inserts cell markers above and below the visual selection.

- `:MatlabInsertModeCreateCell` (C-l) inserts a cell marker at the beginning of the current line.

- `:MatlabLaunchServer` launches a server instance in a Vim or tmux split.

See [this file](rplugin/python/vim_matlab/__init__.py) for a list of available commands, and [vim-matlab.vim](ftplugin/matlab/vim-matlab.vim) for default key bindings.

![Screenshot](/docs/images/screenshot.png)


### Installation

1. Install the python3 client for Neovim:

```
pip3 install neovim
```

2. Add to `.vimrc` (or `~/.config/nvim/init.vim`). e.g. using [vim-plug](https://github.com/junegunn/vim-plug):

```
Plug 'daeyun/vim-matlab'
```

3. Register the plugin inside Neovim:

```
:UpdateRemotePlugins
```

4. Optionally install [SirVer/ultisnips](https://github.com/honza/vim-snippets) to use the snippets.


### Configuration

Use `g:matlab_auto_mappings` to control whether the plugin automatically generates key mappings (default = 1).

```vim
let g:matlab_auto_mappings = 0 "automatic mappings disabled
let g:matlab_auto_mappings = 1 "automatic mappings enabled
```

Use `g:matlab_server_launcher` to control whether `:MatlabLaunchServer` uses a Vim or tmux split (default = `'vim'`).

```vim
let g:matlab_server_launcher = 'vim'  "launch the server in a Neovim terminal buffer
let g:matlab_server_launcher = 'tmux' "launch the server in a tmux split
```

Use `g:matlab_server_split` to control whether `:MatlabLaunchServer` uses a vertical or horizontal split (default = `'vertical'`).

```vim
let g:matlab_server_split = 'vertical'   "launch the server in a vertical split
let g:matlab_server_split = 'horizontal' "launch the server in a horizontal split
```


### Development

Set up a symlink so that the plugin directory points to your repository.

```
git clone git@github.com:daeyun/vim-matlab.git
rm -r ~/.vim/plugged/vim-matlab
ln -nsf $(pwd)/vim-matlab ~/.vim/plugged/
```

After changing the code, run `scripts/reload-vim.sh` (optionally pass in a file to open) to reload.

For testing, install [pytest](https://github.com/pytest-dev/pytest/) and run `scripts/run-tests.sh`.


### Recommended Plugins

- [MatlabFilesEdition](http://www.vim.org/scripts/script.php?script_id=2407)
- [matchit.zip](http://www.vim.org/scripts/script.php?script_id=39)
