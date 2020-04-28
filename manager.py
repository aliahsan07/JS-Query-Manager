import argparse
from subprocess import Popen, PIPE, STDOUT
import ast
import yaml
import json
from mdutils import MdUtils
import os
import os.path
import sys
from classes.TAJS import TAJS
from classes.Safe import Safe
from utils.StringUtils import parseKeys
from testAnalysis import generatePtsOfInterest, generateConfigFile
from configs.safeConfig import SafeConfig
from utils.FileUtils import makeNewFileName


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


def outputSafeStats(safeConfig, globalConfig, safeOutput):
    fileName = makeNewFileName()
    # output stats to out file
    # hacky, fix this
    analysisFile = globalConfig['files'][0]
    analysisFileName = analysisFile['filename']
    mdFile = MdUtils(file_name=fileName,
                     title="File Analyzed: " + analysisFileName)
    callSiteSen = str(safeConfig['callSiteSensitivity'])
    mdFile.new_paragraph('Call-Site Sensitivity: ' +
                         callSiteSen, bold_italics_code='bi', color='purple')
    mdFile.new_paragraph(
        'Loop Depth: ' + str(safeConfig['loopDepth']), bold_italics_code='bi', color='purple')
    mdFile.new_paragraph(
        'Loop Iter: ' + str(safeConfig['loopIter']), bold_italics_code='bi', color='purple')

    mdFile.new_header(level=3, title="Analysis results")
    for pointer in analysisFile['pointers']:
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

    c = {'callSiteSensitivity': 1, 'loopIter': 100, 'loopDepth': 10}
    outputSafeStats(c, jsonObj, refinedOutput)
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
    safeConfig = SafeConfig()
    main(args.test, args.tajs, args.safe)
