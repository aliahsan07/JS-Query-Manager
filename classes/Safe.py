from subprocess import Popen, PIPE, STDOUT
from classes.Analysis import Analysis
from utils.readTool import readToolOutput


class Safe(Analysis):

    def __init__(self, t=[], loopDepth=10, loopIter=100, callsiteSensitivity=20):
        super().__init__(t)
        self.baseCommand = ['safe', 'analyze',
                            '-analyzer:ptrSetFile=' + self.outputFile]
        self.loopDepth = loopDepth
        self.loopIter = loopIter
        self.callsiteSensitivity = callsiteSensitivity

    def runWithRecencyAbstraction(self):
        return self.run('-heapBuilder:recency')

    def setCallsiteSensitivity(self, n):
        self.callsiteSensitivity = n

    def setLoopIter(self, n):
        self.loopIter = n

    def setloopDepth(self, n):
        self.loopDepth = n

    def appendHeapBuilderFlags(self, command):
        if self.callsiteSensitivity is not None:
            command.append('-heapBuilder:callsiteSensitivity=' +
                           str(self.callsiteSensitivity))

        if self.loopDepth is not None:
            command.append('-heapBuilder:loopDepth=' + str(self.loopDepth))

        if self.loopIter is not None:
            command.append('-heapBuilder:loopIter=' + str(self.loopIter))

    def run(self, *flags):
        print(">>>>> Running Safe on JS Program <<<<< ")
        command = self.baseCommand.copy()
        self.appendHeapBuilderFlags(command)
        for arg in flags:
            command.append(arg)
        command.append(self.analysisFile)
        safeOutput = Popen(command, stdout=PIPE, stderr=STDOUT)
        pipeOutput = safeOutput.communicate()[0][:9].decode()
        if pipeOutput == 'Exception':
            print("Safe didn't terminate, resulted in exception")
            return
        return readToolOutput(safe=True)
