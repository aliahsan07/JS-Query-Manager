import argparse
from subprocess import Popen, PIPE, STDOUT
import ast
import yaml
import json
import os
import sys
from classes.TAJS import TAJS
from classes.Safe import Safe
from utils.StringUtils import parseKeys
from testAnalysis import generatePtsOfInterest, generateConfigFile


def comparePrecision(actualSetLen, outputSet):
    try:
        precision = (actualSetLen/len(outputSet))
    except ZeroDivisionError:
        if actualSetLen == 0 and len(outputSet) == 0:
            precision = 1.0
        else:
            precision = 0
    return precision


def loadConfig():

    with open('config.json', 'r') as f:
        config = json.load(f)

    return config

# writeTAJStoYAML needs refining


def writeTAJStoYAML(tajsOutput, jsonObj):

    refinedOutput = {}
    for key in tajsOutput.keys():
        keyAsStr = str(parseKeys(key))
        refinedOutput[keyAsStr] = tajsOutput[key]

    files = jsonObj['files']
    for file in files:
        for pointers in file['pointers']:
            varName = pointers['varname']
            if '.' in varName:
                varName = varName.split('.')[-1]
            key = file['filename'] + '-' + varName + \
                '-' + str(pointers['lineNumber'])
            pointsTo = []
            try:
                pointsTo = ast.literal_eval(refinedOutput[key])
            except:
                pass
            pointers['tajs'] = {}
            pointers['tajs']['output'] = pointsTo
            pointers['tajs']['precision'] = comparePrecision(
                pointers['groundTruth'], pointsTo)
            pointers['tajs']['pointsToSize'] = len(pointsTo)

    return jsonObj


def writeSafetoYAML(safeOutput, jsonObj):

    refinedOutput = {}
    for key in safeOutput.keys():
        keyAsStr = str(parseKeys(key))
        refinedOutput[keyAsStr] = safeOutput[key]

    files = jsonObj['files']
    for file in files:
        for pointers in file['pointers']:
            varName = pointers['varname']
            if '.' in varName:
                varName = varName.split('.')[-1]
            key = file['filename'] + '-' + varName + \
                '-' + str(pointers['lineNumber'])
            pointsTo = []
            try:
                pointsTo = ast.literal_eval(refinedOutput[key])
            except:
                pass
            pointers['safe'] = {}
            pointers['safe']['output'] = pointsTo
            pointers['safe']['precision'] = comparePrecision(
                pointers['groundTruth'], pointsTo)
            pointers['safe']['pointsToSize'] = len(pointsTo)

    return jsonObj


def outputYAML(files, tajsOutput, safeOutput):
    cumulativeOutput = {}

    cumulativeOutput['files'] = []
    for file in files:
        cumulativeOutput['files'].append(
            {
                'filename': file['name']
            }
        )
        cumulativeOutput['files'][-1]['pointers'] = []
        for ptr in file['pointers']:
            cumulativeOutput['files'][-1]['pointers'].append(
                {
                    'varname': ptr['varName'],
                    'lineNumber': int(ptr['lineNumber']),
                    'groundTruth': int(ptr['pointsToSize'])
                }
            )

    final = cumulativeOutput
    if tajsOutput is not None:
        final = writeTAJStoYAML(tajsOutput, final)
    if safeOutput is not None:
        final = writeSafetoYAML(safeOutput, final)
    print(">>>>> Outputting to output.yaml file <<<<< ")
    with open('output.yaml', 'w') as f:
        data = yaml.dump(final, f)


def deleteOldFiles():
    try:
        os.remove("output.json")
    except:
        pass

    try:
        os.remove("safeOutput.json")
    except:
        pass


def main(testFile, tajsOn, safeOn):

    pointers = generatePtsOfInterest(testFile)
    generateConfigFile(pointers, testFile, tajsOn, safeOn)
    # load config
    config = loadConfig()
    deleteOldFiles()

    # parse and make API calls
    files = config['files']
    tajs = TAJS()
    safe = Safe()
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
        # safeOutput = safe.run()
        safeOutput = safe.runWithRecencyAbstraction()

    # output to YAML
    outputYAML(files, tajsOutput, safeOutput)


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
    main(args.test, args.tajs, args.safe)
