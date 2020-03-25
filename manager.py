from subprocess import Popen, PIPE, STDOUT
import ast
import yaml
import json
from classes.TAJS import TAJS
from classes.Safe import Safe
from utils.StringUtils import parseKeys


def comparePrecision(actualSetLen, outputSet):

    precision = (actualSetLen/len(outputSet)) * 100
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
            pointsTo = ast.literal_eval(refinedOutput[key])
            pointers['tajs'] = {}
            pointers['tajs']['output'] = pointsTo
            pointers['tajs']['precision'] = comparePrecision(
                pointers['groundTruth'], pointsTo)

    return jsonObj


def outputYAML(files, tajsOutput):
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
                    'groundTruth': ptr['pointsToSize'],
                }
            )

    final = writeTAJStoYAML(tajsOutput, cumulativeOutput)
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

    # make API call to TAJS
    tajs.mkComboFile()
    safe.mkComboFile()
    # make API call to safe
    tajsOutput = tajs.run()

    # safe.run()

    # output to YAML
    outputYAML(files, tajsOutput)


if __name__ == "__main__":
    main()
