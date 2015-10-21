nnoremap <buffer><silent> <leader>gm :MatlabGuiOpenInEditor<CR>
nnoremap <buffer><silent> ,m :MatlabGuiRunCell<CR>
nnoremap <buffer><silent> <leader>fn :MatlabFixName<CR>
nnoremap <buffer>         <leader>rn :MatlabRename
vnoremap <buffer><silent> ,m <ESC>:MatlabGuiRunSelection<CR>
vnoremap <buffer><silent> <C-m> <ESC>:MatlabCliRunSelection<CR>
nnoremap <buffer><silent> <C-m> <ESC>:MatlabCliRunCell<CR>
nnoremap <buffer><silent> ,i <ESC>:MatlabCliViewVarUnderCursor<CR>
vnoremap <buffer><silent> ,i <ESC>:MatlabCliViewSelectedVar<CR>
nnoremap <buffer><silent> ,h <ESC>:MatlabCliHelp<CR>
nnoremap <buffer><silent> ,e <ESC>:MatlabCliOpenInMatlabEditor<CR>
nnoremap <buffer><silent> <leader>c :MatlabCliCancel<CR>
nnoremap <buffer><silent> <C-h> :MatlabCliRunLine<CR>

set shortmess+=A
