vim-matlab
===========

An alternative to Matlab's default editor for Vim users. It lets you control Matlab remotely from Vim.

### Usage

`vim-matlab-server.py` launches a CLI Matlab instance and and keeps it alive — i.e. when Matlab crashes (e.g. segfault during MEX development), it will launch another process.
It also redirects commands from Vim to Matlab.

```
./scripts/vim-matlab-server.py
```

Open Vim in another terminal, start editing .m files

- `:MatlabCliCancel` (\<leader\>C) tells the server to send SIGINT to Matlab, canceling current operation.

- `:MatlabCliRunSelection` executes the highlighted Matlab code

- `:MatlabCliRunCell` executes code in the current cell — i.e. `%%` blocks. Similar to Ctrl-Enter in the Matlab editor.

- `:MatlabCliOpenInEditor` (,e) opens current buffer in the Matlab editor. e.g. to access the debugger.

- `:MatlabCliHelp` (,h) prints help message for the word under the cursor.

See [this file](rplugin/python/vim_matlab/__init__.py) for a list of available commands, and [vim-matlab.vim](ftplugin/matlab/vim-matlab.vim) for default key bindings.

### Recommended Plugins

[MatlabFilesEdition](http://www.vim.org/scripts/script.php?script_id=2407)

[matchit.zip](http://www.vim.org/scripts/script.php?script_id=39)
