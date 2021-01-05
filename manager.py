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
from classes.WALA import WALA
from utils.FileUtils import deleteOldFiles, outputToFile
from utils.ConfigUtils import loadPointersOfInterest, generateConfigFile, loadConfig, loadToolConfig


def runTool(tajsOn=False, safeOn=False, walaOn=False, tajs=None, safe=None, wala=None):
    output = None
    if tajsOn:
        output = tajs.run()
    elif safeOn:
        output = safe.run()
    elif walaOn:
        output = wala.run()
    return output


def run(testFile, tajsOn, safeOn, walaOn, tajsConfig=None, safeConfig=None, walaConfig=None):
    # load pointers from the test file
    pointers = loadPointersOfInterest(testFile)
    # flush configuration to config.json
    generateConfigFile(pointers, testFile, tajsOn, safeOn, walaOn)

    # load configuration
    config = loadConfig()
    deleteOldFiles()

    # load all files. Its a nested object that contains all the ptrs we need
    files = config['files']

    # TODO: depending on which object is selected load its object
    tajs = TAJS(tajsConfig)
    safe = Safe(safeConfig)
    wala = WALA(walaConfig)

    # add file, pointers to each tool
    for file in files:
        tajs.selectFile(file['name'])
        safe.selectFile(file['name'])
        wala.selectFile(file['name'])
        pointers = file['pointers']

        for tuple in pointers:
            var = tuple['varName']
            line = tuple['lineNumber']
            if tajsOn:
                tajs.addCombo(var, line)
            if safeOn:
                safe.addCombo(var, line)
            if walaOn:
                wala.addCombo(var, line)

    # outputs the pointers to data.txt
    if tajsOn:
        tajs.mkComboFile()
    if safeOn:
        safe.mkComboFile()
    if walaOn:
        wala.mkComboFile

    # make API call to tajs and safe
    tajsOutput, safeOutput, walaOutput = None, None, None
    if tajsOn:
        tajsOutput = runTool(tajsOn=True, tajs=tajs)
    if safeOn:
        safeOutput = runTool(safeOn=True, safe=safe)
    if walaOn:
        walaOutput = runTool(walaOn=True, wala=wala)

    # output to YAML
    # add time taken by each tool in one object
    timers = {
        'tajsTime': tajs.timeTaken,
        'safeTime': safe.timeTaken,
        'walaTime': wala.timeTaken,
    }
    # output data to yaml file
    outputToFile(files, tajsOutput, safeOutput, walaOutput, timers)


def runAllTestCases(tajsOn, safeOn, walaOn, tajsConfig, safeConfig, walaConfig):

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
            run(testCase, tajsOn, safeOn, tajsConfig, safeConfig)
            print(f"\u2713 Succesfully tested {test['name']} ")
            print("<=========================================================>\n")


def main(testFile, tajsOn, safeOn, walaOn, watch, tajsConfig, safeConfig, walaConfig):

    if not tajsOn and not safeOn and not walaOn:
        raise Exception(
            "No flags passed for tools to run. Pass either --tajs or --safe or both to run the tools")
    if safeOn and safeConfig is not None:
        safeConfig = loadToolConfig(safeConfig)
    if tajsOn and tajsConfig is not None:
        tajsConfig = loadToolConfig(tajsConfig)
    if walaOn and walaConfig is not None:
        walaConfig = loadToolConfig(walaConfig)
    if watch:
        runAllTestCases(tajsOn, safeOn, walaOn,
                        tajsConfig, safeConfig, walaConfig)
    else:
        if testFile.split('.')[-1] == "json":
            print(
                f"{testFile} is a JSON File passed as source file. Do you mean to pass the js file instead?")
            return
        run(testFile, tajsOn, safeOn, walaOn,
            tajsConfig, safeConfig, walaConfig)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--test", help="test file for analysis"
    )
    parser.add_argument(
        "--tajs", help="perform analysis with TAJS", action="store_true")
    parser.add_argument(
        "--safe", help="perform analysis with Safe", action="store_true")
    parser.add_argument(
        "--wala", help="perform analysis with WALA", action="store_true")
    parser.add_argument(
        "--tajsConfig", help="Configuration file for TAJS"
    )
    parser.add_argument(
        "--safeConfig", help="Configuration file for Safe"
    )
    parser.add_argument(
        "--walaConfig", help="Configuration file for WALA"
    )
    parser.add_argument(
        "--watch", help="run on all test cases", action="store_true")
    args = parser.parse_args()
    main(args.test, args.tajs, args.safe, args.wala, args.watch,
         args.tajsConfig, args.safeConfig, args.walaConfig)
