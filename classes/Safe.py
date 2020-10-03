from subprocess import Popen, PIPE, STDOUT
from classes.Analysis import Analysis
from utils.readTool import readToolOutput
import time


class Safe(Analysis):

    def __init__(self, config=None):
        super().__init__([])
        heapBuilder = config["heapBuilder"] if config else None
        self.loopDepth = heapBuilder["loopDepth"] if heapBuilder and "loopDepth" in heapBuilder else 10
        self.loopIter = heapBuilder["loopIter"] if heapBuilder and "loopIter" in heapBuilder else 100
        self.callsiteSensitivity = heapBuilder["callsiteSensitivity"] if heapBuilder and "callsiteSensitivity" in heapBuilder else 20
        self.recencyAbstraction = heapBuilder["recency"] if heapBuilder and "recency" in heapBuilder else False
        self.baseCommand = ['safe', 'analyze',
                            '-analyzer:ptrSetFile=' + self.outputFile]
        self.timeTaken = 0.0

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

        if self.recencyAbstraction:
            command.append('-heapBuilder:recency')

    def run(self, *flags):
        print(">>>>> Running Safe on JS Program <<<<< ")
        command = self.baseCommand.copy()
        self.appendHeapBuilderFlags(command)
        for arg in flags:
            command.append(arg)
        command.append(self.analysisFile)
        tic = time.perf_counter()
        safeOutput = Popen(command, stdout=PIPE, stderr=STDOUT)
        toc = time.perf_counter()
        self.timeTaken = toc - tic
        print(f"Safe performed analysis in {toc - tic:0.4f} seconds")
        pipeOutput = safeOutput.communicate()[0][:9].decode()
        if pipeOutput == 'Exception':
            print("Safe didn't terminate, resulted in exception")
            return
        return readToolOutput(safe=True)
