from subprocess import Popen, PIPE, STDOUT
from classes.Analysis import Analysis
from utils.readTool import readToolOutput


class TAJS(Analysis):

    def __init__(self, t=[]):
        super().__init__(t)

    def run(self):
        print(">>>>> Running TAJS on JS Program <<<<< ")
        tajsOutput = Popen(['java', '-jar', '../TAJS/TAJS-run/dist/tajs-all.jar',
                            '-ptrSetFile', self.outputFile, self.analysisFile], stdout=PIPE, stderr=STDOUT)

        return readToolOutput(tajs=True)
