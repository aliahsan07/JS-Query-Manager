from subprocess import Popen, PIPE, STDOUT
from classes.Analysis import Analysis
from utils.readTool import readToolOutput
from utils.StringUtils import getResultSize
import http.client
import json
import socket
import sqlite3
import os
import os.path


class Safe(Analysis):

    def __init__(self, t=[], loopDepth=10, loopIter=100, callsiteSensitivity=20, ptrs=None, groundTruth={}):
        super().__init__(t)
        self.loopDepth = loopDepth
        self.loopIter = loopIter
        self.callsiteSensitivity = callsiteSensitivity
        self.ptrs = ptrs
        self.groundTruth = groundTruth

    def setPointers(self, ptrs):
        self.ptrs = ptrs

    def setGroundTruth(self, groundTruth):
        self.groundTruth = groundTruth

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

    def refineValueSet(self, output):
        splitOnComma = output.split(',')[0::2]
        size = len(splitOnComma)
        refinedOutput = list(map(lambda x: x[1:x.find(':')], splitOnComma))
        refinedOutput = ''.join('"{0}"'.format(w) for w in refinedOutput)
        return (refinedOutput, size)

    def writeToDB(self, output):
        try:

            if not os.path.isfile('safe.db'):
                self.createDB()

            sqliteConnection = sqlite3.connect('safe.db')
            cursor = sqliteConnection.cursor()
            for key, value in output.items():
                varName, lineNumber = key.split('-')
                groundTruth = self.groundTruth[(varName, lineNumber)]
                if not value:
                    value = '" "'
                # refine values here
                value, pointsToSize = self.refineValueSet(value)
                query = f"""
                    INSERT INTO record(filename, callsite, loopiter, loopdepth, 
                    line_number, variable_name, groundtruth, output, points_to_size)
                    VALUES
                    ('{self.analysisFile}', {self.callsiteSensitivity}, {self.loopIter}, 
                    {self.loopDepth}, '{lineNumber}', '{varName}', '{groundTruth}', {value}, {pointsToSize})
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

    def constructPayload(self):

        data = {
            "command": "analyze",
            "loopDepth": "-heapBuilder:loopDepth=" + str(self.loopDepth),
            "loopIter": "-heapBuilder:loopIter=" + str(self.loopIter),
            "callSiteSen": "-heapBuilder:callsiteSensitivity=" + str(self.callsiteSensitivity),
        }

        return data

    def run(self, *flags):
        print(">>>>> Running Safe on JS Program <<<<< ")
        data = self.constructPayload()
        hostname = socket.gethostbyname('localhost')
        connection = http.client.HTTPConnection(hostname + ':8081')
        headers = {'Content-type': 'application/json'}
        data = json.dumps(data)
        connection.request('POST', '/safe', data, headers)

        response = connection.getresponse()
        response = response.read().decode()
        self.writeToDB(json.loads(response))

    def __str__(self):
        return f'Test File: {self.analysisFile}, pointers: {self.tuples}, callSite: {self.callsiteSensitivity}, loopIter: {self.loopIter}, loopDepth: {self.loopDepth}'
