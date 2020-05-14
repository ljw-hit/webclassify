import pymysql
#import matplotlib.pyplot as plt

con = pymysql.connect(host="127.0.0.1", port=3306, user="root", password="123456", db="webmodel")

def drawData():
    cursor = con.cursor()
    sql = "SELECT count(*) from resultdata;"
    cursor.execute(sql)
    sum = cursor.fetchone()[0]
    sql = "SELECT count(*) from resultdata WHERE clogo = plogo;"
    cursor.execute(sql)
    logosum = cursor.fetchone()[0]
    sql = "SELECT count(*) from resultdata WHERE ctype = ptype;"
    cursor.execute(sql)
    typesum = cursor.fetchone()[0]

    print(logosum)
    print(typesum)
    print(sum)

    sql = "SELECT count(*) from resultdata WHERE ctype = ptype and clogo = plogo;"
    cursor.execute(sql)
    allsum = cursor.fetchone()[0]
    print(allsum)

    sql = "select clogo,count(*) FROM resultdata WHERE clogo = plogo GROUP BY clogo"
    cursor.execute(sql)
    clogo = cursor.fetchall()
    clogoT = list(map(list, zip(*clogo)))
    print(clogoT)


    sql = "select clogo,count(*) FROM resultdata GROUP BY clogo"
    cursor.execute(sql)
    clogosum = cursor.fetchall()
    clogosumT = list(map(list, zip(*clogosum)))
    print(clogosumT)

    sql = "select ctype,count(*) FROM resultdata WHERE ctype = ptype GROUP BY ctype"
    cursor.execute(sql)
    ctype = cursor.fetchall()
    ctypeT = list(map(list, zip(*ctype)))
    print(ctypeT)


    sql = "select ctype,count(*) FROM resultdata GROUP BY ctype"
    cursor.execute(sql)
    ctypesum = cursor.fetchall()
    ctypesumT = list(map(list, zip(*ctypesum)))
    print(ctypesumT)

    sql = "SELECT miss,COUNT(*) FROM resultdata WHERE clogo = plogo AND ctype = ptype GROUP BY miss;"
    cursor.execute(sql)
    cmiss = cursor.fetchall()
    cmissT = list(map(list, zip(*cmiss)))
    print(cmissT)

    sql = "SELECT miss,COUNT(*) FROM resultdata GROUP BY miss;"
    cursor.execute(sql)
    misssum = cursor.fetchall()
    misssumT = list(map(list, zip(*misssum)))
    print(misssumT)

    cursor.close()
    con.close()

if __name__ == '__main__':
    drawData()