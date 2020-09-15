import argparse
from subprocess import Popen, PIPE, STDOUT
import ast
import json
import os
import sys
import time
from classes.TAJS import TAJS
from classes.Safe import Safe
from utils.FileUtils import deleteOldFiles, outputToFile
from utils.ConfigUtils import loadPointersOfInterest, generateConfigFile, loadConfig
from configs.safeConfig import SafeConfig


def runTool(tajsOn=False, safeOn=False, tajs=None, safe=None):
    output = None
    if tajsOn:
        tic = time.perf_counter()
        output = tajs.run()
        toc = time.perf_counter()
        print(f"TAJS performed analysis in {toc - tic:0.4f} seconds")
        return output
        # tajsOutput = tajs.runWithDeterminacy()
        # tajsOutput = tajs.runWithDeterminacyAndUneval()
        #tajsOutput = tajs.runBlendedAnalysis()
    elif safeOn:
        tic = time.perf_counter()
        output = safe.run()
        toc = time.perf_counter()
        print(f"Safe performed analysis in {toc - tic:0.4f} seconds")
        # safeOutput = safe.runWithRecencyAbstraction()
        return output


def main(testFile, tajsOn, safeOn):

    # load pointers from the test file
    pointers = loadPointersOfInterest(testFile)
    # flush configuration to config.json
    generateConfigFile(pointers, testFile, tajsOn, safeOn)

    # load configuration
    config = loadConfig()
    deleteOldFiles()

    # load all files. Its a nested object that contains all the ptrs we need
    files = config['files']

    # TODO: depending on which object is selected load its object
    tajs = TAJS()
    safe = Safe()

    # add file, pointers to each tool
    for file in files:
        tajs.selectFile(file['name'])
        safe.selectFile(file['name'])
        pointers = file['pointers']

        for tuple in pointers:
            var = tuple['varName']
            line = tuple['lineNumber']
            tajs.addCombo(var, line)
            safe.addCombo(var, line)

    # outputs the pointers to data.txt
    tajs.mkComboFile()
    safe.mkComboFile()

    # make API call to tajs and safe
    tajsOutput, safeOutput = None, None
    if tajsOn:
        tajsOutput = runTool(tajsOn=True, tajs=tajs)
    if safeOn:
        safeOutput = runTool(safeOn=True, safe=safe)

    # output to YAML
    outputToFile(files, tajsOutput, safeOutput)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--test", help="test file for analysis"
    )
    parser.add_argument(
        "--tajs", help="perform analysis with tajs", action="store_true")
    parser.add_argument(
        "--safe", help="perform analysis with safe", action="store_true")
    args = parser.parse_args()
    safeConfig = SafeConfig()
    main(args.test, args.tajs, args.safe)
