%%
disp('One');
a = a+2;
%%
disp('Two');
a = a+4;
%%
disp('Three');
a = a+3;
%%
disp('Four');
if all([a b c d e f] == [61 55 113 59 174 62])
    disp('Test successful.');
else
    error('Assertion failed.');
end
clear 'a' 'b' 'c' 'd' 'e' 'f';