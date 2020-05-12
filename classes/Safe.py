from subprocess import Popen, PIPE, STDOUT
from classes.Analysis import Analysis
from utils.readTool import readToolOutput
import http.client
import json
import socket
import sqlite3
import os
import os.path

API_ENDPOINT = "http://localhost:8081/safe"


class Safe(Analysis):

    def __init__(self, t=[], loopDepth=10, loopIter=100, callsiteSensitivity=20, ptrs=None):
        super().__init__(t)
        self.baseCommand = ['safe', 'analyze',
                            '-analyzer:ptrSetFile=' + self.outputFile]
        self.loopDepth = loopDepth
        self.loopIter = loopIter
        self.callsiteSensitivity = callsiteSensitivity
        self.ptrs = ptrs

    def setPointers(self, ptrs):
        self.ptrs = ptrs

    def createDB(self):
        sqliteConnection = sqlite3.connect('safe.db')
        cursor = sqliteConnection.cursor()

        query = """
            CREATE TABLE "record" (
            "id"	INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
            "filename"	TEXT NOT NULL,
            "callsite"	INTEGER NOT NULL,
            "loopiter"	INTEGER NOT NULL,
            "loopdepth"	INTEGER NOT NULL,
            "line_number" INTEGER NOT NULL,
            "variable_name" TEXT NOT NULL,
            "groundtruth"	INTEGER NOT NULL,
            "output"	TEXT,
            "points_to_size"	INTEGER
            )
        """

        count = cursor.execute(query)
        sqliteConnection.commit()
        cursor.close()

    def writeToDB(self, output):
        try:

            if not os.path.isfile('safe.db'):
                self.createDB()

            sqliteConnection = sqlite3.connect('safe.db')
            cursor = sqliteConnection.cursor()
            for key, value in output.items():
                varName, lineNumber = key.split('-')

                query = f"""
                    INSERT INTO record(filename, callsite, loopiter, loopdepth, 
                    line_number, variable_name, groundtruth, output, points_to_size)
                    VALUES
                    ('{self.analysisFile}', {self.callsiteSensitivity}, {self.loopIter}, 
                    {self.loopDepth}, '{lineNumber}', '{varName}', 1, {value}, 1)
                """

                count = cursor.execute(query)
                sqliteConnection.commit()
                print("Record inserted successfully ", cursor.rowcount)
            cursor.close()

        except sqlite3.Error as error:
            print("Failed to insert data into sqlite table", error)
        finally:
            if (sqliteConnection):
                sqliteConnection.close()
                print("The SQLite connection is closed")

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

    def constructPayload(self):
        with open(self.analysisFile) as f:
            lines = f.readlines()
        lines = """{}""".format("".join(lines))

        data = {
            "command": "analyze",
            "ptrSetFile": str(self.ptrs),
            "loopDepth": "-heapBuilder:loopDepth=" + str(self.loopDepth),
            "loopIter": "-heapBuilder:loopIter=" + str(self.loopIter),
            "callSiteSen": "-heapBuilder:callsiteSensitivity=" + str(self.callsiteSensitivity),
            "analysisFile": lines
        }

        return data

    def run(self, *flags):
        print(">>>>> Running Safe on JS Program <<<<< ")
        # command = self.baseCommand.copy()
        # self.appendHeapBuilderFlags(command)
        # for arg in flags:
        #     command.append(arg)
        # command.append(self.analysisFile)
        # safeOutput = Popen(command, stdout=PIPE, stderr=STDOUT)
        # pipeOutput = safeOutput.communicate()[0][:9].decode()
        # if pipeOutput == 'Exception':
        #     print("Safe didn't terminate, resulted in exception")
        #     return
        # return f"Processing Done for callSiteSen:{self.callsiteSensitivity}, loopIter:{self.loopIter} and loopDepth:{self.loopDepth}"
        # return readToolOutput(safe=True)

        data = self.constructPayload()
        hostname = socket.gethostbyname('localhost')
        connection = http.client.HTTPConnection(hostname + ':8081')
        headers = {'Content-type': 'application/json'}
        json_foo = json.dumps(data)
        connection.request('POST', '/safe', json_foo, headers)

        response = connection.getresponse()
        response = response.read().decode()
        self.writeToDB(json.loads(response))

    def __str__(self):
        return f'Test File: {self.analysisFile}, pointers: {self.tuples}, callSite: {self.callsiteSensitivity}, loopIter: {self.loopIter}, loopDepth: {self.loopDepth}'
