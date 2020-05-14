from xml.dom.minidom import parse,parseString
import sys
import chardet

class ParseXML():
    def __init__(self):
        self.root = ""
        self.collection = ""

    def parse(self,path):
        domTree = parse(path)
        self.collection = domTree.documentElement
        self.root = domTree.getElementsByTagName("VIPSPage")[0]

    def parseString(self,String):
        try:
            String = str(String.encode('utf-8'), encoding = "utf-8")
            domTree = parseString(String)
        except:
            String = String.encode('utf-8').decode('gb2312','ignore')

            domTree = parseString(String)

        self.collection = domTree.documentElement
        self.root = domTree.getElementsByTagName("VIPSPage")[0]



class VisualBlock():
    def __init__(self):
        self.type = ""
        #layout Node attribute
        self.BgColor = ""
        self.ContainImg =""
        self.ContainP =""
        self.ContainTable =""
        self.DOMCldNum = ""
        self.DoC =""
        self.FontSize=""
        self.FontWeight=""
        self.FrameSourceIndex=""
        self.ID=""
        self.IsImg = ""
        self.LinkTextLen=""
        self.order = ""
        self.TextLen=""

        #vipspage Node attribute
        self.PageTitle = ""
        self.Url = ""
        self.WindowHeight = ""
        self.WindowWidth = ""


        #structure
        self.x = ""
        self.y = ""
        self.width=""
        self.height=""

        self.childNodes = []

    def toVisualBlock(self,node):
        if node.nodeName == "LayoutNode":
            self.type = "LayoutNode"
            self.BgColor = node.getAttribute("BgColor")
            self.ContainImg = node.getAttribute("ContainImg")
            self.ContainP = node.getAttribute("ContainP")
            self.ContainTable = node.getAttribute("ContainTable")
            self.DOMCldNum = node.getAttribute("DOMCldNum")
            self.DoC = node.getAttribute("DoC")
            self.FontSize = node.getAttribute("FontSize")
            self.FontWeight = node.getAttribute("FontWeight")
            self.FrameSourceIndex = node.getAttribute("FrameSourceIndex")
            self.ID = node.getAttribute("ID")
            self.IsImg = node.getAttribute("IsImg")
            self.LinkTextLen = node.getAttribute("LinkTextLen")
            self.x = node.getAttribute("ObjectRectLeft")
            self.y = node.getAttribute("ObjectRectTop")
            self.width = node.getAttribute("ObjectRectWidth")
            self.height = node.getAttribute("ObjectRectHeight")
            self.TextLen = node.getAttribute("TextLen")
            self.order = node.getAttribute("order")

        if node.nodeName == "VIPSPage":
            self.type = "VIPSPage"
            self.height = node.getAttribute("PageRectHeight")
            self.x = node.getAttribute("PageRectLeft")
            self.y = node.getAttribute("PageRectTop")
            self.width = node.getAttribute("PageRectWidth")
            self.PageTitle = node.getAttribute("PageTitle")
            self.Url = node.getAttribute("Url")
            self.WindowHeight = node.getAttribute("WindowHeight")
            self.WindowWidth = node.getAttribute("WindowWidth")
            self.order = node.getAttribute("order")

        #targetVisualBlockList.append(self)

        if len(node.childNodes)  > 0:
            for node in node.childNodes:

                if node.nodeName == "#text":
                    continue
                vbc = VisualBlock()
                vbc.toVisualBlock(node)
                self.childNodes.append(vbc)

    def allNode(self,list):
        list.append(self)

        if self.childNodes.__sizeof__() is not 0:
            for child in self.childNodes:
                child.allNode(list)


    def __str__(self):
            return ("order:%s  x:%s  y:%s  width:%s  height:%s" % (self.order, self.x, self.y, self.width, self.height))

