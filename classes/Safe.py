from subprocess import Popen, PIPE, STDOUT
from classes.Analysis import Analysis
from utils.readTool import readToolOutput


class Safe(Analysis):

    def __init__(self, t=[]):
        super().__init__(t)
        self.baseCommand = ['safe', 'analyze',
                            '-analyzer:ptrSetFile=' + self.outputFile]

    def runWithRecencyAbstraction(self):
        return self.run('-heapBuilder:recency')

    def run(self, *flags):
        print(">>>>> Running Safe on JS Program <<<<< ")
        command = self.baseCommand.copy()
        for arg in flags:
            command.append(arg)
        command.append(self.analysisFile)
        safeOutput = Popen(command, stdout=PIPE, stderr=STDOUT)
        pipeOutput = safeOutput.communicate()[0][:9].decode()
        if pipeOutput == 'Exception':
            print("Safe didn't terminate, resulted in exception")
            return
        return readToolOutput(safe=True)
