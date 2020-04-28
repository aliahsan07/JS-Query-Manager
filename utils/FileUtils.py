import os
import os.path


def makeNewFileName():
    currentDirname = os.path.dirname(__file__)
    outputDirName = os.path.join(currentDirname, '../out/safe-output')
    fileCount = len([name for name in os.listdir(
        outputDirName)])

    fileName = 'out-' + str(fileCount + 1)
    return outputDirName + '/' + fileName
