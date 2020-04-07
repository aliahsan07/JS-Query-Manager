import json
import os
import time


def readToolOutput(tajs=False, safe=False):

    if tajs:
        while not os.path.exists("output.json"):
            time.sleep(1)

        with open('output.json', 'r') as f:
            tajsOutput = json.load(f)
            return tajsOutput

    if safe:
        while not os.path.exists("safeOutput.json"):
            time.sleep(1)
        with open('safeOutput.json', 'r') as f:
            safeOutput = json.load(f)
            return safeOutput
