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


def writeTAJStoYAML(tajsOutput, jsonObj):

    refinedOutput = {}
    for key in tajsOutput.keys():
        keyAsStr = str(parseKeys(key))
        refinedOutput[keyAsStr] = tajsOutput[key]

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
                print("why am i here")
                pass
            pointers['safe'] = {}
            pointers['safe']['output'] = pointsTo
            pointers['safe']['precision'] = comparePrecision(
                pointers['groundTruth'], pointsTo)
            pointers['safe']['pointsToSize'] = len(pointsTo)

    return jsonObj


def outputToFile(files, tajsOutput, safeOutput):
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
