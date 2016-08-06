command! MatlabNormalModeCreateCell :execute "normal! :set paste<CR>m`O%%<ESC>``:set nopaste<CR>"
command! MatlabVisualModeCreateCell :execute "normal! gvD:set paste<CR>O%%<CR>%%<ESC>P:set nopaste<CR>"
command! MatlabInsertModeCreateCell :execute "normal! I%% "

nnoremap <buffer>         <leader>rn :MatlabRename
nnoremap <buffer><silent> <leader>fn :MatlabFixName<CR>
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

nnoremap <buffer><silent> <C-l> :MatlabNormalModeCreateCell<CR>
vnoremap <buffer><silent> <C-l> :<C-u>MatlabVisualModeCreateCell<CR>
inoremap <buffer><silent> <C-l> <C-o>:MatlabInsertModeCreateCell<CR>
