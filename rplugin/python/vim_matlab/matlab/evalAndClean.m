function evalAndClean(expression)
try
    evalc(expression);
    numQuotes = sum(expression=='''');
    argLen = length(expression);
    funcNameLen = numel(mfilename);
    printBackspace(argLen + funcNameLen + numQuotes + 9);
catch ex
    rethrow(ex)
end