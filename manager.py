# Libraries
import os
import os.path
import sys
import argparse
import ast
import json
import os
import sys
import yaml
from classes.TAJS import TAJS
from classes.Safe import Safe
from utils.FileUtils import deleteOldFiles, outputToFile
from utils.ConfigUtils import loadPointersOfInterest, generateConfigFile, loadConfig
from configs.safeConfig import SafeConfig


def runTool(tajsOn=False, safeOn=False, tajs=None, safe=None):
    output = None
    if tajsOn:
        output = tajs.run()
        return output
        # tajsOutput = tajs.runWithDeterminacy()
        # tajsOutput = tajs.runWithDeterminacyAndUneval()
        #tajsOutput = tajs.runBlendedAnalysis()
    elif safeOn:
        output = safe.run()
        # safeOutput = safe.runWithRecencyAbstraction()
        return output


def run(testFile, tajsOn, safeOn):
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
    # add time taken by each tool in one object
    timers = {
        'tajsTime': tajs.timeTaken,
        'safeTime': safe.timeTaken
    }
    # output data to yaml file
    outputToFile(files, tajsOutput, safeOutput, timers)


def runAllTestCases(tajsOn, safeOn):

    with open(r'info.yaml') as file:
        # The FullLoader parameter handles the conversion from YAML
        # scalar values to Python the dictionary format
        fileLoaded = yaml.load(file, Loader=yaml.FullLoader)

    testSuite = fileLoaded["tests"]

    for module in testSuite:
        print("\n")
        print(f"Running tests for {module}")
        for test in testSuite[module]:
            print(f"Testing {test['name']}...")
            testCase = test['path']
            run(testCase, tajsOn, safeOn)
            print(f"\u2713 Succesfully tested {test['name']} ")
            print("<=========================================================>\n")


def main(testFile, tajsOn, safeOn, watch):

    if not tajsOn and not safeOn:
        raise Exception(
            "No flags passed for tools to run. Pass either --tajs or --safe or both to run the tools")
    if watch:
        runAllTestCases(tajsOn, safeOn)
    else:
        run(testFile, tajsOn, safeOn)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--test", help="test file for analysis"
    )
    parser.add_argument(
        "--tajs", help="perform analysis with tajs", action="store_true")
    parser.add_argument(
        "--safe", help="perform analysis with safe", action="store_true")
    parser.add_argument(
        "--watch", help="run on all test cases", action="store_true")
    args = parser.parse_args()
    # safeConfig = SafeConfig() # TODO
    main(args.test, args.tajs, args.safe, args.watch)
