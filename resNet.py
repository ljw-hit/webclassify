import torch
from torch.utils import data
from torch import nn
import torchvision
from torchvision import  transforms
from torch.autograd import Variable
from CutOut import Cutout
from visdom import Visdom
from config import *
import os
dirRoot = "F:\LogoClassify\logo"

#窗口类实例化
viz = Visdom(env="acc_loss_10")

data_tf=transforms.Compose([
    transforms.Scale((128, 128), 1),
    #transforms.RandomCrop(32,padding=4),
    Cutout(6),
    transforms.RandomHorizontalFlip(),
    #transforms.RandomVerticalFlip(),
    transforms.ToTensor(),
    transforms.Normalize((0.5, 0.5, 0.5), (0.5, 0.5, 0.5))
])


models = torchvision.models.resnet34(num_classes=10)
#models = torchvision.models.AlexNet(num_classes=8)

trainDataset = torchvision.datasets.ImageFolder(
    root= os.path.join(dirRoot,"train"),
    transform = data_tf
)

trainLoader = data.DataLoader(
    trainDataset,
    batch_size=batchSize,
    shuffle=True,
    num_workers=0
)

testDataset = torchvision.datasets.ImageFolder(
    root= os.path.join(dirRoot,"test"),
    transform = data_tf
)

testLoader = data.DataLoader(
    testDataset,
    batch_size=batchSize,
    shuffle=True,
    num_workers=0
)

#optimizer = torch.optim.SGD(models.parameters(),lr=learningRate,momentum=1.0)
optimizer =torch.optim.Adam(models.parameters(),lr=learningRate)
criterion = nn.CrossEntropyLoss()
if torch.cuda.is_available():
    models = models.cuda()
#print(models)


for i in range(1,epoch+1):
    models.train()
    #train--------------------------------
    total = 0
    running_loss = 0.0
    running_correct = 0
    print("epoch {}/{}".format(i, epoch))
    print("-" * 10)
    for data in trainLoader:
        img, label = data
        # img=img.view(img.size(0),-1)
        img = Variable(img)
        if torch.cuda.is_available():
            img = img.cuda()
            label = label.cuda()
            #print(label)
        else:
            img = Variable(img)
            label = Variable(label)
            #print(label)
        out = models(img)  # 得到前向传播的结果
        loss = criterion(out, label)  # 得到损失函数
        print_loss = loss.data.item()
        optimizer.zero_grad()  # 归0梯度
        loss.backward()  # 反向传播
        optimizer.step()  # 优化
        running_loss += loss.item()
        #
        total += label.size(0)
        _, predicted = torch.max(out.data, 1)
        running_correct += (predicted == label).sum()
        if i % 5 == 0:
            learningRate = learningRate* (0.1 ** (i // 5))
            print('train epoch:{},loss:{:.4f}'.format(i, print_loss))
            viz.line([float(loss.data.item())],[i],win="train_loss",name='train_loss',update='append',opts=dict(title="train_loss"))
        #i += 1

   # print(predicted)

    acc = 100 * running_correct / total
    viz.line([float(acc)], [i],win="train_acc" ,name='train_acc', update='append',opts=dict(title="train_acc"))
    print('第%d个epoch train 的识别准确率为：%d%%' % (i, (acc)))

    #evalution------------------------------------
    models.eval()
    test_correct = 0
    testtotal = 0
    testloss = 0.
    testacc = 0.
    for testdata in testLoader:
        testimg,testlabel = data
        testimg = Variable(testimg)
        if torch.cuda.is_available():
            testimg = testimg.cuda()
            testlabel = testlabel.cuda()
            #print(label)
        else:
            testimg = Variable(testimg)
            testlabel = Variable(testlabel)
        testout = models(testimg)
        testloss = criterion(testout,testlabel)
        tprint_loss=testloss.data.item()
        _, predicted = torch.max(testout.data, 1)
        testtotal += testlabel.size(0)
        test_correct+=(predicted==testlabel).sum()
        if i % 5 == 0:
            print('test epoch:{},loss:{:.4f}'.format(i, testloss))
            viz.line([float(loss.data.item())],[i],win='test_loss',name='loss',update='append',opts=dict(title="test_loss"))


    testacc = 100*test_correct / testtotal
    viz.line([float(testacc)], [i], win='test_acc', name='acc', update='append',opts=dict(title="test_acc"))
    print('第%d个epoch test 的识别准确率为：%f%%' % (i, (testacc)))
    print("loss "+str(float(tprint_loss)))
    if float(running_loss) < 0.05:
        print("模型训练完成")
        break

torch.save(models.state_dict(),modelPath)


