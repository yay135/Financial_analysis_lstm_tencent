import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os
import math
import torch
import torch.nn as nn
import torch.optim as optim

from pandas import Timestamp
from sklearn import preprocessing

modename = 'model.pth.tar'
sf = 20
allSeries = {}
for file in os.listdir('.'):
    if file.endswith('.csv'):
        with open(".\\{a}".format(a=file)) as f:
            raw = pd.read_csv(f, encoding='utf-8')
            dates = []
            vals = []
            raw.columns = ['dates','vals']
            for index,row in raw.iterrows():
                dates.append(Timestamp(row['dates']))
                vals.append(row['vals'])
            series = pd.Series(data=vals,index=dates)
            allSeries[file.split('.')[0]] = series


axs = None
for key,series in allSeries.items():
    axs = series.plot(label=key,ax = axs)

plt.show()

seq = ['王者荣耀','微信','英雄联盟','HSI','TCEHY']

tmp = []
scalers = []

for Str in seq:
    for key,vals in allSeries.items():
        if Str in key:
            tmp.append(vals.values)


def shiftData(seq ,shifts):
    if len(seq) == 0 or shifts <1 or shifts >= len(seq[0]):
        return []
    target = seq[-1].tolist()[:]
    ans = []
    ans.append(target)
    for ls in seq:
        for i in range(1,shifts+1):
            rs = ls.tolist()[:]
            for j in range(0,i):
                rs.insert(0,-1)
            ans.insert(0,rs)
    i = shifts
    while i>0:
        for arr in ans:
            arr.pop(0)
        i-=1

    minL = 10000000
    for arr in ans:
        minL = min(minL,len(arr))
    for arr in ans:
        while len(arr)>minL:
            arr.pop(-1)

    return ans

tmp = shiftData(tmp,sf)
tmp = np.array(tmp)
print(tmp.shape)

for i in range(0,len(tmp)):
    arr = np.array(tmp[i,:])
    arr = np.reshape(arr,(-1,1))
    min_max_scaler = preprocessing.MinMaxScaler(feature_range=(0, 1))
    scaled = min_max_scaler.fit_transform(arr)
    for j in range(0,len(arr)):
        tmp[i,j] = scaled[j,0]

tmp = np.rot90(tmp)
np.random.shuffle(tmp)

trainTestSplit = int(len(tmp)*0.8)

print(tmp.shape)

class Sequence(nn.Module):
    def __init__(self):
        super(Sequence,self).__init__()
        self.lstm1 = nn.LSTM(5,20,1)
        self.linear1 = nn.Linear(20,5)
        self.linear2 = nn.Linear(5,1)

    def forward(self, input):
        output,(h_n,c_n) = self.lstm1(input)
        x = self.linear1(h_n)
        x = self.linear2(x)
        return x

model = Sequence()
loss = nn.MSELoss()
optimizer = optim.SGD(model.parameters(), lr = 0.001, momentum=0.89)

def prepareData(arr,sf):
    ans =[]
    raw = arr[0:-1]
    Lsq = 0
    while Lsq < sf:
        word = []
        idx = Lsq
        while idx < len(raw):
            num = raw[idx] if not math.isnan(raw[idx]) else 0.5
            word.append(num)
            idx += sf
        Lsq += 1
        ans.append([word])
        t = arr[-1] if not math.isnan(arr[-1]) else 0.5
    return (np.array(ans),np.array([[[t]]]))



if os.path.exists('./{a}'.format(a=modename)):
    model.load_state_dict(torch.load('./{a}'.format(a=modename)))
    model.eval()
else:
    for epoch in range(3):
        print("training epoch {a}".format(a=epoch))
        i = 0
        while i<trainTestSplit:
            model.zero_grad()
            print("training epoch{a},sample{b}".format(a=epoch,b=i))
            featuresShaped,Target = prepareData(tmp[i],sf)

            input = torch.tensor(featuresShaped,dtype=torch.float)
            TargetOut = torch.tensor(Target,dtype=torch.float)
            output = model(input)

            Loss = loss(output,TargetOut)
            Loss.backward()
            optimizer.step()

            i+=1

    torch.save(model.state_dict(), modename)

print("finished training.")

TestData = tmp[trainTestSplit:]

predict = []
actual = []
for i in range(0,len(TestData)):
    input,TruthOut = prepareData(TestData[i],sf)
    input = torch.tensor(input,dtype=torch.float)
    out = model(input)
    v = out.item()
    predict.append(v)
    actual.append(TestData[i][-1])

s0 = pd.Series(data=actual,index=range(0,len(actual)))
s1 = pd.Series(data=predict,index=range(0,len(predict)))

axs=s0.plot(color='r')
s1.plot(color='blue',ax=axs)

plt.show()







