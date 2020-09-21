import json
import socket
import http


def copyFilesToSafeServer(analysisFile, ptrSet):

    hostname = socket.gethostbyname('localhost')
    connection = http.client.HTTPConnection(hostname + ':8081')
    headers = {'Content-type': 'application/json'}
    with open(analysisFile) as f:
        lines = f.readlines()
    analysisFileContent = """{}""".format("".join(lines))

    ptrSetContent = str(ptrSet)

    data = {
        "analysisFile": analysisFileContent,
        "ptrSetFile": ptrSetContent
    }

    connection.request('POST', '/copyfiles', json.dumps(data), headers)

    response = connection.getresponse()
    response = response.read().decode()
    if response == '{}':
        return True
