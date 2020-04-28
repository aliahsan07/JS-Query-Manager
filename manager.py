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


def outputSafeStats(globalConfig, safeOutput):
    fileName = makeNewFileName()
    analysisFileName = globalConfig['filename']
    mdFile = MdUtils(file_name=fileName,
                     title="File Analyzed: " + analysisFileName)
    callSiteSen = str(safeConfig.callSiteSensitivity)
    mdFile.new_paragraph('Call-Site Sensitivity: ' +
                         callSiteSen, bold_italics_code='bi', color='purple')
    mdFile.new_paragraph(
        'Loop Depth: ' + str(safeConfig.loopDepth), bold_italics_code='bi', color='purple')
    mdFile.new_paragraph(
        'Loop Iter: ' + str(safeConfig.loopIter), bold_italics_code='bi', color='purple')

    mdFile.new_header(level=3, title="Analysis results")
    for pointer in globalConfig['pointers']:
        varName = pointer['varname']
        lineNumber = pointer['lineNumber']
        groundTruth = pointer['groundTruth']
        if '.' in varName:
            varName = varName.split('.')[-1]
        key = analysisFileName + '-' + varName + \
            '-' + str(pointer['lineNumber'])
        pointsTo = []
        try:
            pointsTo = ast.literal_eval(safeOutput[key])
        except:
            pass
        mdFile.new_paragraph('variable name: ' + varName)
        mdFile.new_paragraph('line number: ' + str(lineNumber))
        mdFile.new_paragraph('Ground Truth: ' + str(groundTruth))
        safeResult = pointer['safe']
        mdFile.new_paragraph('points-to set: ' + str(safeResult['output']))
        mdFile.new_paragraph('points-to set size: ' +
                             str(safeResult['pointsToSize']))
        mdFile.new_paragraph('precision: ' + str(safeResult['precision']))

        mdFile.new_paragraph('-------------------------------------')
    mdFile.create_md_file()


def writeSafetoYAML(safeOutput, jsonObj):

    refinedOutput = {}
    for key in safeOutput.keys():
        keyAsStr = str(parseKeys(key))
        refinedOutput[keyAsStr] = safeOutput[key]

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
        pointers['safe'] = {}
        pointers['safe']['output'] = pointsTo
        pointers['safe']['precision'] = comparePrecision(
            pointers['groundTruth'], pointsTo)
        pointers['safe']['pointsToSize'] = len(pointsTo)

    outputSafeStats(jsonObj, refinedOutput)
    return jsonObj


def outputYAML(config, tajsOutput, safeOutput):
    cumulativeOutput = {}

    cumulativeOutput['filename'] = config['name']
    cumulativeOutput['pointers'] = []
    for ptr in config['pointers']:
        cumulativeOutput['pointers'].append(
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

    try:
        cleanup()
    except:
        pass


def runSafe(callSiteSen, config):
    safe = Safe(callsiteSensitivity=callSiteSen,
                loopDepth=safeConfig.loopDepth, loopIter=safeConfig.loopIter)
    safe.selectFile(config['name'])

    mutex.acquire()
    fileNumber = countFiles()
    safe.setFileNumber(fileNumber)
    fileName = makeNewFileName()
    mutex.release()

    analysisFileName = config['name']
    mdFile = MdUtils(file_name=fileName,
                     title="File Analyzed: " + analysisFileName)
    mdFile.create_md_file()
    output = safe.run()
    return output


def bootSafe(config):
    percentages = safeConfig.options
    callSiteSensOptions = [safeConfig.calculateCallSiteSen(
        percentage) for percentage in percentages]

    callSiteSensOptions = [
        item for sublist in callSiteSensOptions for item in sublist]

    # options = safeConfig.makeHeapBuilderCombos()
    start = time.perf_counter()
    with concurrent.futures.ThreadPoolExecutor() as executor:
        results = [executor.submit(runSafe, opt, config)
                   for opt in callSiteSensOptions]

        for future in concurrent.futures.as_completed(results):
            print(future.result())

    end = time.perf_counter()
    print(f'Finished in {end-start} seconds')


def main(testFile, tajsOn, safeOn):

    pointers = generatePtsOfInterest(testFile)
    generateConfigFile(pointers, testFile, tajsOn, safeOn)
    # load config
    config = loadConfig()
    deleteOldFiles()

    # parse and make API calls
    tajs = TAJS()
    # safe = Safe()
    # safe = Safe(callsiteSensitivity=0, loopDepth=0, loopIter=0)

    tajs.selectFile(config['name'])
    # safe.selectFile(config['name'])  # change this
    pointers = config['pointers']

    for tuple in pointers:
        var = tuple['varName']
        line = tuple['lineNumber']
        # tajs.addCombo(var, line)
        dataStore.appendTuple(var, line)

    dataStore.createPointersDataSet()
    bootSafe(config)

    # make API call to tajs and safe
    tajsOutput = None
    if config['tajs']:
        tajsOutput = tajs.run()
        # tajsOutput = tajs.runWithDeterminacy()
        # tajsOutput = tajs.runWithDeterminacyAndUneval()
        #tajsOutput = tajs.runBlendedAnalysis()
    safeOutput = None
    # if config['safe']:
    #     safeOutput = safe.run()
    # safeOutput = safe.runWithRecencyAbstraction()

    # output to YAML
    outputYAML(config, tajsOutput, safeOutput)


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
