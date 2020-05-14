from parseXML import  ParseXML,VisualBlock
from ModelList import selectModel,insertPatch
from loadModel import load,startPredict,cutLogo
from webpageSim import WebPageSim
import os
import sys
filelist = []
def vips(url):
    url = url.replace("&","^&")
    command = "java -cp vips/vips-onlyLogo-outFolder.jar org.fit.vips.VipsTester "+url
    print(command)
    out = os.popen(command)
    lines = out.readlines()
    print(lines)
    folderPath = ".\\"+lines[-1].strip()
    #folderPath.replace("\\","\\\\")
    filelist.append(folderPath)

def vipsPatch(fileName):
    command = "java -cp vips/vips-onlyLogo-outFolder-filename.jar org.fit.vips.VipsTester "+fileName
    print(command)
    out = os.popen(command)
    print(out)




def indentifyLogo(Path):
    g = os.walk(Path)
    for path, dir_list, file_list in g:
        for file_name in file_list:
            if "logo" in file_name:
                logoFile = os.path.join(path,file_name)
                logo, acc, miss = startPredict(logoFile)
                #print(logo)
                break
        else:
            continue
        break
    else:
        logoPath = cutLogo(Path)
        logo, acc, miss = startPredict(logoPath)
    return logo,acc,miss

def webSimilarity(Path,logoList):
    xml = ParseXML()
    sourceXmlFile = open(Path+"\\VIPSResult.xml", "r", encoding="utf8")
    sourceWebXML = "".join(sourceXmlFile.readlines())
    #将页面
    sourceVisualBlockList = []
    xml.parseString(sourceWebXML)
    sourceDomRoot = xml.root
    sourceVisualBlockRoot = VisualBlock()
    sourceVisualBlockRoot.toVisualBlock(sourceDomRoot)
    sourceVisualBlockRoot.allNode(sourceVisualBlockList)

    #获取 满足条件的所有模板
    modelList = []
    for logo in logoList:
        modelList.extend(selectModel(logo));
    logo = ""
    type = ""
    sim = 0
    for model in modelList:
        tempSim =WebPageSim(sourceVisualBlockList,model[2])
       # print(model[0]+" "+model[1]+" "+str(tempSim))
        if tempSim > sim:
            logo = model[0]
            type = model[1]
            sim = tempSim

    return  logo,type,sim

def main(url):
    load()
    vips(url)
    for path in filelist:
        logoList = indentifyLogo(path)
        truple = webSimilarity(path,logoList)
        print(truple)


def testWebList():
    result = []
    #vipsPatch("testWebList")
    g = os.walk("result")
    load()
    for path, dir_list, file_list in g:
        for file_name in dir_list:

            parts = file_name.split("_")
            if len(parts) <3:
                break
            c_logo,c_type = parts[1],parts[2]

            filepath = os.path.join(path,file_name)
            logo, acc, miss = indentifyLogo(filepath)

            p_logo, p_type, sim = webSimilarity(filepath,logo)
            index = logo.index(p_logo)
            p_logo_percent = acc[index]
            r=[c_logo,c_type,p_logo,p_type,miss.__str__(),p_logo_percent.item().__str__()[:6],sim.__str__()[:6]]
            print(r)
            result.append(r)

    insertPatch(result)

import os
def filename(path):
    for file in os.listdir(path):
        newfile = ""
        if "缃戣喘" in file:
            newfile = file.replace("缃戣喘","wg")
        elif "鏂伴椈" in file:
            newfile = file.replace("鏂伴椈","xw")
        elif "鎷涜仒" in file:
            newfile = file.replace("鎷涜仒","zp")
        else:
            continue
        print(newfile)
        os.rename(path+'\\'+file,path+'\\'+newfile)


if __name__ == '__main__':
    #print(vips("https://www.taobao.com"))
    #indentifyLogo("F:\LogoClassify\\test")
    #main("https://item.jd.com/100006153412.html")
    testWebList()
    #filename("result")
