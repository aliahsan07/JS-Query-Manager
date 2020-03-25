from subprocess import Popen, PIPE, STDOUT
from classes.Analysis import Analysis
from utils.readTool import readToolOutput


class Safe(Analysis):

    def __init__(self, t=[]):
        super().__init__(t)

    def run(self):
        print(">>>>> Running Safe on JS Program <<<<< ")
        safeOutput = Popen(['safe', 'analyze', '-analyzer:ptrSetFile=' + self.outputFile,
                            self.analysisFile], stdout=PIPE, stderr=STDOUT)

        return readToolOutput(safe=True)
