from parseXML import ParseXML,VisualBlock
from config import coordinateThreshold,lwThreshold,webThreshold
from  ModelList import selectModel

def test():

    xmlFile = open("xmls/wy2.xml","r",encoding="utf8")
    xmlString = "".join(xmlFile.readlines())
    xml = ParseXML()
    VisualBlockList = []
    xml.parseString(xmlString)
    targetDomRoot = xml.root
    targetVisualBlockRoot = VisualBlock()
    targetVisualBlockRoot.toVisualBlock(targetDomRoot)
    targetVisualBlockRoot.allNode(VisualBlockList)
    xmlFile = open("xmls/jd1.xml", "r", encoding="utf8")
    xmlString = "".join(xmlFile.readlines())
    # resultList =  selectModel("qqmusic")
    #
    # for result_1 in resultList:
    #
    #     sim = WebPageSim(VisualBlockList,result_1[2])
    #     print(str(result_1[0])+" "+str(result_1[1])+" "+str(sim))
    sim = WebPageSim(VisualBlockList, xmlString)
    print(sim)


def WebPageSim(sourceVisualBlockList,targetWebXML):
    xml = ParseXML()
    targetVisualBlockList = []
    xml.parseString(targetWebXML)
    targetDomRoot = xml.root
    targetVisualBlockRoot = VisualBlock()
    targetVisualBlockRoot.toVisualBlock(targetDomRoot)
    targetVisualBlockRoot.allNode(targetVisualBlockList)

    #计算相似度
    SIM = 0
    MIM = max(len(targetVisualBlockList),len(sourceVisualBlockList))
    for node1 in sourceVisualBlockList:
        for node2 in targetVisualBlockList:
            gx,gy,gl,gw = node1.x,node1.y,node1.height,node1.width
            tx,ty,tl,tw = node2.x,node2.y,node2.height,node2.width
            x = abs(int(gx)-int(tx))
            y = abs(int(gy)-int(ty))
            l = abs(int(gl)-int(tl))
            w = abs(int(gw)-int(tw))

            if x<= coordinateThreshold and y<=coordinateThreshold and l <= lwThreshold and w<= lwThreshold:
                 gFontSize,tFontSize = node1.FontSize,node2.FontSize
                 glink,tlink = node1.LinkTextLen,node2.LinkTextLen
                 gColor,tColor = node1.BgColor,node2.BgColor
                 gImage,tImage = node1.ContainImg,node2.ContainImg

                 #视觉特征占权重比
                 weight = 1

                 if gFontSize == tFontSize:
                     weight = weight+0.5
                 if glink is not 0 and tlink is not 0:
                     weight = weight+0.5
                 if gColor == tColor:
                     weight = weight+0.25
                 if gImage == tImage:
                     weight = weight+0.25

                 SIM = SIM+1*weight
                 MIM = MIM-1+1*weight

                 targetVisualBlockList.remove(node2)
                 continue


    similarity = float(SIM/MIM)
    return similarity


if __name__ == '__main__':
    test()