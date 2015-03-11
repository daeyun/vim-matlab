%%
disp('One');
a = a + 1;
%%
disp('Two');
a = a + 1;
a = a + 1;
%%
disp('Three');
a = a + 1;
a = a + 1;
a = a + 1;
%%
assert(a==6);
clear 'a';
%%
assert(a==5);
clear 'a';
disp('Test successful');