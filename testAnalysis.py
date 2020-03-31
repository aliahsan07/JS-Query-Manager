import ast as astReader
import json
import re


def generatePtsOfInterest(file):
    with open(file, 'r') as content_file:
        content = content_file.read()

    values = re.findall(r'groundTruth.*?=\s*(.*?);',
                        content, re.DOTALL | re.MULTILINE)

    for value in values:
        return json.loads(value)


def generateConfigFile(ptrs, testFile, tajsOn, safeOn):

    configDict = {'files': []}
    configDict['tajs'] = tajsOn
    configDict['safe'] = safeOn
    configDict['files'].append({
        "name": testFile,
    })
    currentFile = configDict['files'][0]
    currentFile['pointers'] = []

    for key, value in ptrs.items():
        ptrName, line = key.split('-')
        currentFile['pointers'].append({
            "varName": ptrName,
            "lineNumber": line,
            "pointsToSize": value
        })

    with open('config.json', 'w') as outfile:
        json.dump(configDict, outfile)
