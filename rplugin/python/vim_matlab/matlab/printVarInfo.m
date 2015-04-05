function printVarInfo(varname)

sz = mat2str(size(varname));
type = class(varname);

fprintf('%s %s\n', sz, type);

if numel(varname) < 5
    fprintf('var: %s\n', mat2str(varname));
else
    u = unique(varname(:));
    fprintf('var(1:5): %s\nunique(1:5): %d\n', mat2str(varname(1:5)), mat2str(u(1:min(5, numel(u)))));
end
