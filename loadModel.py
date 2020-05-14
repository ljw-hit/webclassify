from config import modelPath,logo_dic,top1Thresold,top2Thresold,top3Thresold
from config import  width,height
from torchvision import models,transforms
import torch
import os
from PIL import Image

model = models.resnet34(num_classes=10)
device = torch.device("cuda")
transform = transforms.Compose([
    transforms.Resize((128, 128), 1),
    transforms.ToTensor(),
    transforms.Normalize((0.5, 0.5, 0.5), (0.5, 0.5, 0.5))
])

def load():

    model.load_state_dict(torch.load(modelPath,map_location="cuda:0"))
    model.to(device)
    #print(model)
    model.eval()

def startPredict(imagePath):

    logo = []
    image = Image.open(imagePath)
    l,w = image.size[0],image.size[1]
    if l>300 or w>150:
      l = l if l<300 else 300
      w = w if w<150 else 150

    img2 = image.crop((0,0,l,w))

    try:
        image_tensor = transform(img2)
    except:
        img2 = img2.convert("RGB")
        image_tensor = transform(img2)

    image_tensor.unsqueeze_(0)
    image_tensor = image_tensor.to(device)

    out = model(image_tensor)

    percentage = torch.nn.functional.softmax(out, dim=1)[0] * 100
    max , index = torch.sort(percentage,descending = True)

    #print(max)
    #print(index)
    acc = []
    miss  = 0

    if max[0]>top1Thresold:
        logo.append(logo_dic[int(index[0])])
        acc.append(max[0])
        miss = 1
    elif max[0]>top3Thresold:
        for i in range(2): logo.append(logo_dic[int(index[i])])
        for i in range(2): acc.append(max[i])
        miss = 2
    else:
         for i in range(10): logo.append(logo_dic[int(index[i])])
         for i in range(10): acc.append(max[i])

    # print(logo)
    # print(max)
    return logo,acc,miss


def cutLogo(path):
    img = Image.open(path+"\\pageCompele.png")
    img2 = img.crop((0, 0, width,height))
    img2.save(path+"\\logo.png")
    return path+"\\logo.png"


if __name__ == '__main__':
    load()
    g = os.walk("testImage")
    for path, dir_list, file_list in g:
        for file_name in file_list:
                logoFile = os.path.join(path, file_name)
                print(file_name)
                startPredict(logoFile)
        break
