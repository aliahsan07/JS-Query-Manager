import json


def readToolOutput(tajs=False, safe=False):

    if tajs:
        with open('output.json', 'r') as f:
            tajsOutput = json.load(f)
            return tajsOutput

    if safe:
        with open('safeOutput.json', 'r') as f:
            safeOutput = json.load(f)
            return safeOutput
