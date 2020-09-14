import argparse
from subprocess import Popen, PIPE, STDOUT
import ast
import json
import os
import sys
from classes.TAJS import TAJS
from classes.Safe import Safe
from utils.FileUtils import deleteOldFiles, outputToFile
from testAnalysis import loadPointersOfInterest, generateConfigFile
from configs.safeConfig import SafeConfig


def loadConfig():

    with open('config.json', 'r') as f:
        config = json.load(f)

    return config


def main(testFile, tajsOn, safeOn):

    pointers = loadPointersOfInterest(testFile)
    generateConfigFile(pointers, testFile, tajsOn, safeOn)

    # load config
    config = loadConfig()
    deleteOldFiles()

    # parse and make API calls
    files = config['files']

    tajs = TAJS()
    # safe = Safe()
    safe = Safe(callsiteSensitivity=0, loopDepth=0, loopIter=0)

    for file in files:
        tajs.selectFile(file['name'])
        safe.selectFile(file['name'])
        pointers = file['pointers']

        for tuple in pointers:
            var = tuple['varName']
            line = tuple['lineNumber']
            tajs.addCombo(var, line)
            safe.addCombo(var, line)

    tajs.mkComboFile()
    safe.mkComboFile()

    # make API call to tajs and safe
    tajsOutput = None

    if config['tajs']:
        tajsOutput = tajs.run()
        # tajsOutput = tajs.runWithDeterminacy()
        # tajsOutput = tajs.runWithDeterminacyAndUneval()
        #tajsOutput = tajs.runBlendedAnalysis()
    safeOutput = None
    if config['safe']:
        safeOutput = safe.run()
        # safeOutput = safe.runWithRecencyAbstraction()

    # output to YAML
    outputToFile(files, tajsOutput, safeOutput)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--test", help="test file for analysis"
    )
    parser.add_argument(
        "--tajs", help="enable analysis with tajs", action="store_true")
    parser.add_argument(
        "--safe", help="enable analysis with safe", action="store_true")
    args = parser.parse_args()
    safeConfig = SafeConfig()
    main(args.test, args.tajs, args.safe)
