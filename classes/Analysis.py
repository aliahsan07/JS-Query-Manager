class Analysis:

    def __init__(self, t=[]):
        self.tuples = t
        self.analysisFile = None
        self.outputFile = "data.txt"

    def selectFile(self, file):
        self.analysisFile = file

    def addCombo(self, varName, lineNumber):
        self.tuples.append((varName, lineNumber))

    def mkComboFile(self):
        f = open(self.outputFile, "w")

        for var, line in self.tuples:
            if '.' in var:
                var = var.split('.')[-1]
            f.write(var + " " + str(line) + "\n")

    # its not working???
    def __str__(self):
        tuples = " " if len(self.tuples) == 0 else ", Tuples: ".join(
            str(v) for v in self.tuples)
        return "{ File: " + self.analysisFile + tuples + " }"
