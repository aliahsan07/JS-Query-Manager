

def parseKeys(key):

    table = str.maketrans(dict.fromkeys("()"))
    key = key.translate(table)

    result = "-".join([x.strip() for x in key.split(',')])
    return result
