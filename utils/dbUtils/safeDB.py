import sqlite3


def getSafeDataFromDB(analysisFile):
    conn = None
    try:
        conn = sqlite3.connect('safe.db')
    except sqlite3.Error as error:
        print(error)

    cursor = conn.cursor()
    cursor.execute(f""" 
            select variable_name, line_number, callsite, loopdepth, loopiter, groundtruth, output, points_to_size from record 
            where filename='{analysisFile}';
        """)

    rows = cursor.fetchall()

    return rows
