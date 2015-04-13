nnoremap <silent> <leader>gm :MatlabGuiOpenInEditor<CR>
nnoremap <silent> ,m :MatlabGuiRunCell<CR>
nnoremap <silent> <leader>fn :MatlabFixName<CR>
nnoremap <leader>rn :MatlabRename
vnoremap <silent> ,m <ESC>:MatlabGuiRunSelection<CR>
vnoremap <silent> <C-m> <ESC>:MatlabCliRunSelection<CR>
nnoremap <silent> <C-m> <ESC>:MatlabCliRunCell<CR>
nnoremap <silent> ,i <ESC>:MatlabCliViewVarUnderCursor<CR>
vnoremap <silent> ,i <ESC>:MatlabCliViewSelectedVar<CR>
nnoremap <silent> ,h <ESC>:MatlabCliHelp<CR>
nnoremap <silent> ,e <ESC>:MatlabOpenInMatlabEditor<CR>
nnoremap <silent> <leader>c :MatlabCliCancel<CR>

set shortmess+=A