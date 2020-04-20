from subprocess import Popen, PIPE, STDOUT
from classes.Analysis import Analysis
from utils.readTool import readToolOutput
import itertools
import os


class TAJS(Analysis):

    def __init__(self, t=[]):
        super().__init__(t)
        self.baseCommand = ['java', '-jar', '../TAJS/TAJS-run/dist/tajs-all.jar',
                            '-ptrSetFile', self.outputFile]
        self.flags = ["-uneval", "-determinacy",
                      ("-blended-analysis", "logFile"), ("-unsound", "X")]
        self.combinations = []
        for L in range(0, len(self.flags)+1):
            for subset in itertools.combinations(self.flags, L):
                self.combinations.append(subset)

    def runAllCombinations(self):
        for combination in self.combinations:
            self.run(*combination)

    def run(self, *flags):
        print(">>>>> Running TAJS on JS Program <<<<< ")
        command = self.baseCommand.copy()
        for arg in flags:
            if isinstance(arg, tuple):
                if arg[0] == '-blended-analysis':
                    f = arg[1]
                    if not os.path.isfile(f):
                        print("Error: log file not found for blended analysis")
                        continue
                command.append(arg[0])
                command.append(arg[1])
            else:
                command.append(arg)

        command.append(self.analysisFile)
        tajsOutput = Popen(command, stdout=PIPE, stderr=STDOUT)
        print(command)
        return readToolOutput(tajs=True)
