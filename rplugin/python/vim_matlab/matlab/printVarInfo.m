function printVarInfo(varname)

sz = mat2str(size(varname);
type = class(varname);

fprintf('%s %s', sz, type);