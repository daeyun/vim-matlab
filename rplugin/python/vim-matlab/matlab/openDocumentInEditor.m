function openDocumentInEditor(filename)

if ~matlab.desktop.editor.isOpen(filename)
    numMaxFiles = 10;
    openEditors = matlab.desktop.editor.Document.getAllOpenEditors;
    numOpenFiles = numel(openEditors);
    if numOpenFiles >= numMaxFiles
        openEditors(1:(numOpenFiles-numMaxFiles+1)).closeNoPrompt();
    end
end
matlab.desktop.editor.openDocument(filename);
pause(0.05);
for i = 1:10
    if matlab.desktop.editor.isOpen(filename) && ...
            matlab.desktop.editor.isEditorAvailable()
        break
    end
    pause(0.1);
end