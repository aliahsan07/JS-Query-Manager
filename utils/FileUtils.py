import os
import yaml
import ast
from utils.StringUtils import parseKeys


def comparePrecision(actualSetLen, outputSet):
    try:
        precision = (actualSetLen/len(outputSet))
    except ZeroDivisionError:
        if actualSetLen == 0 and len(outputSet) == 0:
            precision = 1.0
        else:
            precision = 0
    return precision


def writeTAJStoYAML(tajsOutput, cumulativeOutput, runtime=0.0):

    refinedOutput = {}
    for key in tajsOutput.keys():
        keyAsStr = str(parseKeys(key))
        refinedOutput[keyAsStr] = tajsOutput[key]

    files = cumulativeOutput['files']
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
            pointers['tajs']['runtime'] = f"{runtime: 0.4f}"
            pointers['tajs']['output'] = pointsTo
            pointers['tajs']['precision'] = comparePrecision(
                pointers['groundTruth'], pointsTo)
            pointers['tajs']['pointsToSize'] = len(pointsTo)


def writeSafetoYAML(safeOutput, cumulativeOutput, runtime=0.0):

    refinedOutput = {}
    for key in safeOutput.keys():
        keyAsStr = str(parseKeys(key))
        refinedOutput[keyAsStr] = safeOutput[key]

    files = cumulativeOutput['files']
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
            pointers['safe']['runtime'] = f"{runtime: 0.4f}"
            pointers['safe']['output'] = pointsTo
            pointers['safe']['precision'] = comparePrecision(
                pointers['groundTruth'], pointsTo)
            pointers['safe']['pointsToSize'] = len(pointsTo)


def outputToFile(initialConfig, tajsOutput, safeOutput, timers):
    cumulativeOutput = {}  # stores the final state of the analysis after running all tools

    cumulativeOutput['files'] = []
    outputFileName = "output.yaml"
    for file in initialConfig:
        cumulativeOutput['files'].append(
            {
                'filename': file['name']
            }
        )
        # TODO get the input filename, handle error cases
        outputFileName = file['name'].split('/')[-1][:-3]
        cumulativeOutput['files'][-1]['pointers'] = []
        for ptr in file['pointers']:
            cumulativeOutput['files'][-1]['pointers'].append(
                {
                    'varname': ptr['varName'],
                    'lineNumber': int(ptr['lineNumber']),
                    'groundTruth': int(ptr['pointsToSize'])
                }
            )

    if tajsOutput is not None:
        writeTAJStoYAML(
            tajsOutput, cumulativeOutput, timers["tajsTime"])
    if safeOutput is not None:
        writeSafetoYAML(
            safeOutput, cumulativeOutput, timers["safeTime"])
    print(">>>>> Outputting to output.yaml file <<<<< ")
    with open('out/%s.yaml' % outputFileName, 'w') as f:
        data = yaml.dump(cumulativeOutput, f)


def deleteOldFiles():
    try:
        os.remove("output.json")
    except:
        pass

    try:
        os.remove("safeOutput.json")
    except:
        pass
