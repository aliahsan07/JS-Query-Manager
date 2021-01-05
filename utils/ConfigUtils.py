import ast as astReader
import json
import re


def loadConfig():
    with open('config.json', 'r') as f:
        config = json.load(f)

    return config


def loadToolConfig(filename):
    with open(filename, 'r') as f:
        config = json.load(f)

    return config


def loadPointersOfInterest(file):
    pointerDataFile = file.split('.')[:-1][0] + '.ground.json'
    with open(pointerDataFile, 'r') as f:
        return json.load(f)["pointers"]


def generateConfigFile(ptrs, testFile, tajsOn, safeOn, walaOn):

    configDict = {'files': []}
    configDict['tajs'] = tajsOn
    configDict['safe'] = safeOn
    configDict['wala'] = walaOn
    configDict['files'].append({
        "name": testFile,
    })
    currentFile = configDict['files'][0]
    currentFile['pointers'] = []

    for ptr in ptrs:
        varName = ptr['variable']
        line = ptr['lineNumber']
        pointsToSize = ptr['groundTruth']

        currentFile['pointers'].append({
            "varName": varName,
            "lineNumber": line,
            "pointsToSize": pointsToSize
        })

    with open('config.json', 'w') as outfile:
        json.dump(configDict, outfile)
