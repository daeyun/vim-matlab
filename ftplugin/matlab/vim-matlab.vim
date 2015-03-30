nnoremap <silent> <leader>gm :MatlabGuiOpenInEditor<CR>
nnoremap <silent> ,mc :MatlabGuiRunCell<CR>
nnoremap <silent> <leader>fn :MatlabFixName<CR>
nnoremap <leader>rn :MatlabRename
vnoremap <silent> ,ms <ESC>:MatlabGuiRunSelection<CR>
vnoremap <silent> <C-m> <ESC>:MatlabCliRunSelection<CR>
nnoremap <silent> <C-m> <ESC>:MatlabCliRunCell<CR>
nnoremap <silent> ,i <ESC>:MatlabCliViewVarUnderCursor<CR>
vnoremap <silent> ,i <ESC>:MatlabCliViewSelectedVar<CR>
