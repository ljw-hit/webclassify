
#logo对应的下标
logo_dic = {0:"alibaba",1:"jd",2:"mt",3:"netease",4:"pdd",5:"qqmusic",6:"sina",7:"taobao",8:"tencent",9:"tm"}

#定义一些超参数
batchSize=100
learningRate=0.005
epoch=130
#模型识别完前top3作为备选logo

top1Thresold = 99

top2Thresold = 90

top3Thresold = 67

modelPath = "./model/resNet_param"

#网页视觉相似度的一些参数
coordinateThreshold = 190
lwThreshold = 180
webThreshold = 0.45

#logo可能在网页的位置
x = 0
y = 0
width = 300
height = 100