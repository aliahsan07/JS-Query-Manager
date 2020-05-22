# Libraries
import os
import os.path
import sys
import argparse
import ast
import concurrent.futures
from multiprocessing import Lock
import time
# yaml, json, md file handlers
import yaml
import json
from mdutils import MdUtils
# Classes
from classes.TAJS import TAJS
from classes.Safe import Safe
from classes.DataStore import DataStore
# Utils
from utils.StringUtils import parseKeys
from testAnalysis import generatePtsOfInterest, generateConfigFile
from configs.safeConfig import SafeConfig
from utils.FileUtils import makeNewFileName, countFiles, cleanup
from utils.API.SafeAPI import copyFilesToSafeServer
from utils.dbUtils.safeDB import getSafeDataFromDB


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


def writeTAJStoYAML(tajsOutput, jsonObj):

    refinedOutput = {}
    for key in tajsOutput.keys():
        keyAsStr = str(parseKeys(key))
        refinedOutput[keyAsStr] = tajsOutput[key]

    file = jsonObj
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


def writeSafetoYAML(filename):
    result = getSafeDataFromDB(filename)
    jsonData = {}
    jsonData['fileName'] = filename
    jsonData['results'] = {}
    for row in result:
        varName = row[0]
        lineNumber = str(row[1])
        callSite = row[2]
        loopDepth = row[3]
        loopIter = row[4]
        groundTruth = row[5]
        output = row[6]
        dictOutput = jsonData['results']
        if str(varName + " " + lineNumber) not in dictOutput:
            # hacky, make this reusable and elegant
            dictOutput[varName + " " + lineNumber] = []

        dictOutput[varName + " " + lineNumber].append(
            {
                'callSiteSensitivity': callSite,
                'loopDepth': loopDepth,
                'loopIter': loopIter,
                'output': output
            }
        )

    return jsonData


def outputYAML(filename, tajsOutput, safeOutput):

    if tajsOutput is not None:
        final = writeTAJStoYAML(tajsOutput)
    if safeOutput is not None:
        final = writeSafetoYAML(filename)
    print(">>>>> Outputting to output.yaml file <<<<< ")
    with open('output.yaml', 'w') as f:
        data = yaml.dump(final, f)


def runSafe(callSiteSen, loopDepth, loopIter, config, ptrsList, groundTruth):
    safe = Safe(callsiteSensitivity=callSiteSen,
                loopDepth=loopDepth, loopIter=loopIter, ptrs=ptrsList, groundTruth=groundTruth)
    safe.selectFile(config['name'])
    output = safe.run()
    return output


def bootSafe(config, ptrsList, groundTruth):
    percentages = safeConfig.options
    callSiteSensOptions = [safeConfig.calculateCallSiteSen(
        percentage) for percentage in percentages]

    callSiteSensOptions = [
        item for sublist in callSiteSensOptions for item in sublist]

    options = safeConfig.makeHeapBuilderCombos()
    fileName = config['name']
    resp = copyFilesToSafeServer(fileName, ptrsList)
    if not resp:
        print("Encountered error in sending files to SAFE Server. Exiting!!!")
        return
    start = time.perf_counter()
    with concurrent.futures.ThreadPoolExecutor() as executor:
        results = [executor.submit(runSafe, opt, safeConfig.loopDepth, safeConfig.loopIter,
                                   config, ptrsList, groundTruth) for opt in callSiteSensOptions]
    #     # results = [executor.submit(runSafe, opt[0], opt[1], opt[2], config, ptrsList, groundTruth)
    #     #            for opt in options]  # for all variants

        for future in concurrent.futures.as_completed(results):
            print(future.result())

    end = time.perf_counter()
    print(f'Finished in {end-start} seconds')


def main(testFile, tajsOn, safeOn):

    pointers = generatePtsOfInterest(testFile)
    generateConfigFile(pointers, testFile, tajsOn, safeOn)
    # load config
    config = loadConfig()
    filename = config['name']
    pointers = config['pointers']
    # parse and make API calls
    tajs = TAJS()
    tajs.selectFile(config['name'])

    for tuple in pointers:
        var = tuple['varName']
        line = tuple['lineNumber']
        pointsToSize = tuple['pointsToSize']
        dataStore.appendTuple(var, line, pointsToSize)

    pointersList = dataStore.createPointersDataSet()
    groundTruthData = dataStore.getGroundTruth()
    bootSafe(config, pointersList, groundTruthData)

    # TODO move TAJS and SAFE to client-server model
    tajsOutput = None
    if config['tajs']:
        tajsOutput = tajs.run()
        # tajsOutput = tajs.runWithDeterminacy()
        # tajsOutput = tajs.runWithDeterminacyAndUneval()
        # tajsOutput = tajs.runBlendedAnalysis()
    outputYAML(filename, tajsOutput, safeOn)


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
    safeConfig = SafeConfig()  # Use as global variable
    dataStore = DataStore()
    mutex = Lock()
    main(args.test, args.tajs, args.safe)
