source("../shared/qmls.py")

def verifyNextLineIndented(editorArea, expectedIndentation):
    type(editorArea, "<Down>")
    rawLine = str(lineUnderCursor(editorArea))
    indentedLine = rawLine.rstrip()
    # handle special case if line has only whitespaces inside
    if not indentedLine:
        indentedLine = rawLine
    unindentedLine = indentedLine.lstrip()
    numSpaces = len(indentedLine) - len(unindentedLine)
    # verify if indentation is valid (multiply of 4) and if has correct depth level
    test.compare(numSpaces % 4, 0, "Verifying indentation spaces")
    test.compare(numSpaces / 4, expectedIndentation, "Verifying indentation level")

def verifyIndentation(editorArea):
    #verify indentation
    if not placeCursorToLine(editorArea, "id: rect"):
        invokeMenuItem("File", "Save All")
        invokeMenuItem("File", "Exit")
        return False
    type(editorArea, "<Up>")
    expectedIndentations = [1,1,1,2,2,2,2,3,3,3,4,3,3,2,1]
    for indentation in expectedIndentations:
        verifyNextLineIndented(editorArea, indentation)
    return True

def main():
    editorArea = startQtCreatorWithNewAppAtQMLEditor(tempDir(), "SampleApp")
    if not editorArea:
        return
    # prepare code for test - insert unindented code
    lines = ['id: rect', 'property bool random: true', 'Text{',
             'anchors.bottom:parent.bottom', 'text: rect.random ? getRandom() : "I\'m fixed."',
             '', 'function getRandom(){', 'var result="I\'m random: ";',
             'var chars="ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789";',
             'for(var i=0;i<8;++i)', 'result += chars.charAt(Math.floor(Math.random() * chars.length));',
             'return result + ".";']
    if not placeCursorToLine(editorArea, "Rectangle {"):
        invokeMenuItem("File", "Exit")
        return
    type(editorArea, "<Return>")
    typeLines(editorArea, lines)
    # verify default indentation
    if not verifyIndentation(editorArea):
        return
    # cancel indentation
    type(editorArea, "<Ctrl+A>")
    for i in range(5):
        type(editorArea, "<Shift+Backtab>")
    # select unindented block
    type(editorArea, "<Ctrl+A>")
    # do indentation
    type(editorArea, "<Ctrl+I>")
    # verify invoked indentation
    if not verifyIndentation(editorArea):
        return
    # save and exit
    invokeMenuItem("File", "Save All")
    invokeMenuItem("File", "Exit")
