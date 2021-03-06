class DataStore():

    def __init__(self, tuples={}, outputFile="data.txt"):
        self.tuples = tuples
        self.outputFile = outputFile

    def createPointersDataSet(self):
        f = open(self.outputFile, "w")
        pointers = ""
        for key, value in self.tuples.items():
            var, line = key
            if '.' in var:
                var = var.split('.')[-1]
            concatStr = var + " " + str(line) + "\n"
            f.write(concatStr)
            pointers += concatStr
        return pointers

    def appendTuple(self, var, line, pointsToSize):
        self.tuples[(var, line)] = pointsToSize

    def getGroundTruth(self):
        return self.tuples
