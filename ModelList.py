import pymysql
import os

con = pymysql.connect(host="127.0.0.1", port=3306, user="root", password="123456", db="webmodel")


def createTabel():
    cursor = con.cursor()
    sql = '''CREATE TABLE `ModelList` (
                 `logo` varchar(10),
                 `type` varchar(20) ,
                 `context` text(100000)
               ) ENGINE=InnoDB DEFAULT CHARSET=utf8;
               '''
    cursor.execute(sql)
    cursor.close()
    con.close()


def createTabel2():
    cursor = con.cursor()
    sql = '''CREATE TABLE `ResultData` (
                 `clogo` varchar(10),
                 `ctype` varchar(20) ,
                 `plogo` varchar(10),
                 `ptype` varchar(20) ,
                 `miss`  varchar(10),
                 `logosim` varchar(10),
                 `websim` varchar(10)
               ) ENGINE=InnoDB DEFAULT CHARSET=utf8;
               '''
    cursor.execute(sql)
    cursor.close()
    con.close()


def insertWebModel():
    webModelList = open("webModelList","r",encoding="utf8")
    lines = webModelList.readlines()
    webModelList.close()
    command = "java -cp vips/vips-noImage.jar org.fit.vips.VipsTester "
    sql = "insert into ModelList(logo,type,context) value(%s,%s,%s)"
    cursor = con.cursor()
    for line in lines:

        parts = line.split(" ")
        logo = parts[0].strip()
        type = parts[1].strip()
        url  = parts[2].strip().replace("&","^&")
        os.system(command+str(url))
        structureFile = open("VIPSResult.xml","r",encoding="utf8")
        structureString = "".join(structureFile.readlines())
        try:
            cursor.execute(sql,(logo,type,structureString))
        except:
            print("插入web模板问题"+logo+"  "+type+"  "+url)
            continue
    con.commit()
    print("提交完成")
    cursor.close()
    structureFile.close()


def selectModel(logo):
    sql = "select * from ModelList where logo = %s"
    cursor = con.cursor()
    try:
        cursor.execute(sql,(logo))
    except:
        print("获取模板错误")
    result = cursor.fetchall()
    return result


def insertPatch(result):
    #TODO
    sql = "insert into ResultData(clogo,ctype,plogo,ptype,miss,logosim,websim) value(%s,%s,%s,%s,%s,%s,%s)"
    cursor = con.cursor()
    try:
     cursor.executemany(sql,result)
    except:
      print ("patchInsert error ")
    cursor.close()
    con.commit()
    print("提交成功")

    return
if __name__ == '__main__':

  #  createTabel2()
  # createTabel()
   insertWebModel()
  # resultList = selectModel("taobao")
  # for result_1 in resultList:
  #     print(result_1)
