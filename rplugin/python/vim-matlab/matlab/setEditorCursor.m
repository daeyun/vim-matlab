function setEditorCursor(row, col)
activeEditor = matlab.desktop.editor.getActive();
activeEditor.reload();
activeEditor.goToPositionInLine(row, col);
