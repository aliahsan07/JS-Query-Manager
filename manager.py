from subprocess import Popen, PIPE, STDOUT
import ast
import yaml
import json
from classes.TAJS import TAJS
from classes.Safe import Safe
from utils.StringUtils import parseKeys


def comparePrecision(actualSetLen, outputSet):
    try:
        precision = (actualSetLen/len(outputSet)) * 100
    except ZeroDivisionError:
        precision = 'undefined'
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
            key = file['filename'] + '-' + pointers['varname'] + \
                '-' + str(pointers['lineNumber'])
            pointsTo = []
            try:
                pointsTo = ast.literal_eval(refinedOutput[key])
            except:
                pass
            pointers['tajs'] = {}
            pointers['tajs']['output'] = pointsTo
            # pointers['tajs']['precision'] = comparePrecision(
            #     pointers['groundTruth'], pointsTo)

    return jsonObj


def writeSafetoYAML(safeOutput, jsonObj):

    refinedOutput = {}
    for key in safeOutput.keys():
        keyAsStr = str(parseKeys(key))
        refinedOutput[keyAsStr] = safeOutput[key]

    files = jsonObj['files']
    for file in files:
        for pointers in file['pointers']:
            key = file['filename'] + '-' + pointers['varname'] + \
                '-' + str(pointers['lineNumber'])
            pointsTo = []
            try:
                pointsTo = ast.literal_eval(refinedOutput[key])
            except:
                pass
            pointers['safe'] = {}
            pointers['safe']['output'] = pointsTo
            # pointers['safe']['precision'] = comparePrecision(
            #     pointers['groundTruth'], pointsTo)

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
                    'lineNumber': ptr['lineNumber'],
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


def main():

    # load config
    config = loadConfig()

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
    safeOutput = None
    if config['safe']:
        safeOutput = safe.run()

    # output to YAML
    outputYAML(files, tajsOutput, safeOutput)


if __name__ == "__main__":
    main()
