from subprocess import Popen, PIPE, STDOUT
import ast
import yaml
import json
from classes.TAJS import TAJS


def loadConfig():

    with open('config.json', 'r') as f:
        config = json.load(f)

    return config


def main():
    # load config
    config = loadConfig()

    # parse and make API calls
    files = config['files']
    tajs = TAJS()
    for file in files:
        # make calls for every file?
        tajs.selectFile(file['name'])
        pointers = file['pointers']

        for tuple in pointers:
            var = tuple['varName']
            line = tuple['lineNumber']
            tajs.addCombo(var, line)

    print(tajs)


def toDo():
    while True:
        jsSourceFile = 'example.js'
        sourceVariable = input(
            "Enter the variable you want to query for pointsTo Info: ")
        lineNumber = input("Enter the corresponding line number: ")

        # TAJS
        print(">>>>> Running TAJS on JS Program <<<<< ")
        tajsOutput = Popen(['java', '-jar', '../TAJS/TAJS-run/dist/tajs-all.jar',
                            '-pointer', sourceVariable, '-line', lineNumber, jsSourceFile], stdout=PIPE, stderr=STDOUT)

        cumulativeOutput = {}
        cumulativeOutput['query'] = {
            'file': jsSourceFile,
            'variable': sourceVariable,
            'lineNumber': lineNumber,
            'groundTruth': {
                'pointsToSize': 2,  # hard-coded
            }
        }

        for line in tajsOutput.stdout:
            decodedLine = line.decode('ascii')[16:-2]
            pointsToSet = decodedLine.split(', ')

        cumulativeOutput['pointsTo'] = {}
        cumulativeOutput['pointsTo']['TAJS'] = []
        for absLoc in pointsToSet:
            cumulativeOutput['pointsTo']['TAJS'].append(absLoc)

        # safe
        print(">>>>> Running Safe on JS Program <<<<< ")
        safeOutput = Popen(['safe', 'analyze', '-analyzer:pointer=' + sourceVariable,
                            '-analyzer:line=' + lineNumber, jsSourceFile], stdout=PIPE, stderr=STDOUT)

        for line in safeOutput.stdout:
            decodedLine = line.decode('ascii')[20:-2]
            pointsToSet = decodedLine.split(', ')

        cumulativeOutput['pointsTo']['Safe'] = []
        for absLoc in pointsToSet:
            cumulativeOutput['pointsTo']['Safe'].append(absLoc)
        # WALA

        # how do we know ground truth

        # output as yaml file
        print(">>>>> Outputting to output.yaml file <<<<< ")
        with open('output.yaml', 'w') as f:
            data = yaml.dump(cumulativeOutput, f)


if __name__ == "__main__":
    main()
