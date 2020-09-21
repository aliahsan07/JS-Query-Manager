import ast


def parseKeys(key):

    table = str.maketrans(dict.fromkeys("()"))
    key = key.translate(table)

    result = "-".join([x.strip() for x in key.split(',')])
    return result


def getResultSize(result):

    pointsTo = []
    try:
        pointsTo = ast.literal_eval(result)
        print(pointsTo)
    except:
        pass

    return len(pointsTo)
