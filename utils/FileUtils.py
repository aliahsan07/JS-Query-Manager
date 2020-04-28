import os
import os.path
import shutil


def getOutDirectory():
    currentDirname = os.path.dirname(__file__)
    outputDirName = os.path.join(currentDirname, '../out/safe-output')
    return outputDirName


def cleanup():
    for root, dirs, files in os.walk(getOutDirectory()):
        for f in files:
            os.unlink(os.path.join(root, f))
        for d in dirs:
            shutil.rmtree(os.path.join(root, d))


def countFiles():
    outputDirName = getOutDirectory()
    fileCount = len([name for name in os.listdir(
        outputDirName)])
    return fileCount


def makeNewFileName():
    fileCount = countFiles()
    outputDirName = getOutDirectory()
    fileName = 'out-' + str(fileCount + 1)
    return outputDirName + '/' + fileName
