from subprocess import Popen, PIPE, STDOUT
from classes.Analysis import Analysis
from utils.readTool import readToolOutput
import itertools
import os


class TAJS(Analysis):

    def __init__(self, t=[]):
        super().__init__(t)
        self.baseCommand = ['java', '-jar', '../TAJS/TAJS-run/dist/tajs-all.jar',
                            '-ptrSetFile', self.outputFile, '-quiet']
        self.flags = ["-uneval", "-determinacy",
                      ("-blended-analysis", "-generate-log", "-log-file", "log-file.log"), ("-unsound", "X")]
        self.combinations = []
        for L in range(0, len(self.flags)+1):
            for subset in itertools.combinations(self.flags, L):
                self.combinations.append(subset)

    def runAllCombinations(self):
        for combination in self.combinations:
            self.run(*combination)

    def runWithDeterminacy(self):
        return self.run('-determinacy')

    def runWithDeterminacyAndUneval(self):
        return self.run('-determinacy', '-uneval')

    def runBlendedAnalysis(self):
        return self.run(self.flags[2])

    def run(self, *flags):
        print(">>>>> Running TAJS on JS Program <<<<< ")
        command = self.baseCommand.copy()
        for arg in flags:
            if isinstance(arg, tuple):
                for a in arg:
                    command.append(a)
            else:
                command.append(arg)

        command.append(self.analysisFile)
        tajsOutput = Popen(command, stdout=PIPE, stderr=STDOUT)
        pipeOutput = tajsOutput.communicate()[0][:9].decode()
        if pipeOutput == 'Exception':
            print("TAJS didn't terminate, resulted in exception")
            return
        return readToolOutput(tajs=True)
