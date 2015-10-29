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

setlocal shortmess+=A
setlocal formatoptions-=cro

nnoremap <buffer><silent> <C-l> :set paste<CR>m`O%%<Esc>``:set nopaste<CR>
vnoremap <buffer><silent> <C-l> d:set paste<cr>O%%<cr>%%<esc>P:set nopaste<cr>
inoremap <buffer><silent> <C-l> <C-o>0%% 
