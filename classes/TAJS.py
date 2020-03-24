from subprocess import Popen, PIPE, STDOUT


class TAJS:

    def __init__(self, t=[]):
        self.tuples = t
        self.fileName = None

    def selectFile(self, file):
        self.fileName = file

    def addCombo(self, varName, lineNumber):
        print(self)
        self.tuples.append((varName, lineNumber))

    def mkComboFile(self):
        f = open("data.txt", "w")

        for var, line in self.tuples:
            f.write(var + '\n')
            f.write(line + '\n')

    # its not working???
    def __str__(self):
        tuples = " " if len(self.tuples) == 0 else ", Tuples: ".join(
            str(v) for v in self.tuples)
        return "{ File: " + self.fileName + tuples + " }"

    # def run():
    #     print(">>>>> Running TAJS on JS Program <<<<< ")
    #     tajsOutput = Popen(['java', '-jar', '../TAJS/TAJS-run/dist/tajs-all.jar',
    #                         '-pointer', self., '-line', lineNumber, jsSourceFile], stdout=PIPE, stderr=STDOUT)
