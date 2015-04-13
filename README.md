vim-matlab
===========

Start vim-matlab server. It launches a CLI Matlab instance and and keeps it alive -- i.e. when Matlab crashes (e.g. segfault during MEX development), it will launch another process.
It also pipes commands from vim to Matlab.

```
./scripts/vim-matlab-server.py
```

Open Vim in another terminal, start editing .m files

- `:MatlabCliCancel` (`<leader>C`) tells the server to send SIGINT to Matlab, canceling current operation.

- `:MatlabCliRunSelection` executes the hilighted Matlab code

- `:MatlabCliRunCell` executes code in the current cell -- i.e. `%%` blocks. Similar to Ctrl-Enter in the Matlab editor.

See ./rplugin/python/vim_matlab/__init__.py for a list of available commands
