"""
Author Fengyao Yan/University of South Carolina
All Rights Reserved
This file train predict a peroid of sf > sft
"""

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
from sklearn.metrics import mean_squared_error as MSE

# model config, change it only if you know what you are doing
config = {
    "history": 30,
    "lstm": (5, 15, 1),
    "linear1": (15, 7),
    "linear2": (10, 7),
}

# modename to save after training if the folder exits this save model file then will skip training process
modename = 'model23'
# training config, change it only if you know what you are doing
sf = config["history"]
sft = 6

# read in all the need data
allSeries = {}
for file in os.listdir('.'):
    if file.endswith('.csv'):
        with open(".\\{a}".format(a=file)) as f:
            raw = pd.read_csv(f, encoding='utf-8')
            dates = []
            vals = []
            raw.columns = ['dates', 'vals']
            for index, row in raw.iterrows():
                dates.append(Timestamp(row['dates']))
                vals.append(row['vals'])
            series = pd.Series(data=vals, index=dates)
            allSeries[file.split('.')[0]] = series

# plot raw data
axs = None
for key, series in allSeries.items():
    axs = series.plot(label=key, ax=axs)
plt.show()

# define the data sequence
seq = ['王者荣耀', '微信', '英雄联盟', 'HSI', 'TCEHY']

# tempory data storage
tmp = []

# storage for normalizer
scalers = []

# format data in the defined sequence above
for Str in seq:
    for key, vals in allSeries.items():
        if Str in key:
            tmp.append(vals.values)
if len(tmp) != len(seq):
    print("Missing data!\nCheck list:\n王者荣耀.csv\n微信.csv\n英雄联盟.csv\nHSI.csv\nTCEHY.csv\n")
    exit()


# shift data to create historical data for a specific date
def shiftDataHistory(seq, shifts):
    if len(seq) == 0 or shifts < 1 or shifts >= len(seq[0]):
        return []
    target = seq[-1].tolist()[:]
    ans = []
    ans.append(target)
    for ls in seq:
        for i in range(1, shifts + 1):
            rs = ls.tolist()[:]
            for j in range(0, i):
                rs.insert(0, -1)
            ans.insert(0, rs)
    i = shifts
    while i > 0:
        for arr in ans:
            arr.pop(0)
        i -= 1
    minL = 10000000
    for arr in ans:
        minL = min(minL, len(arr))
    for arr in ans:
        while len(arr) > minL:
            arr.pop(-1)
    return ans


# shift data to create a series of continuous date after a specific date who's daily prices will be predicted
def shiftDataFuture(seq, sft):
    shape = seq.shape
    if len(shape) != 2 or shape[0] < 1 or shape[1] < 1:
        return
    if sft >= shape[1]:
        return
    ts = seq.tolist()[:][:]
    for _ in range(0, sft):
        rs = ts[-1][:]
        rs.pop(0)
        ts.append(rs)
    leng = len(ts[-1])
    for i in range(0, len(ts)):
        while len(ts[i]) > leng:
            ts[i].pop(-1)
    return np.array(ts)


# format data
tmp = shiftDataHistory(tmp, sf)
tmp = np.array(tmp)
tmp = shiftDataFuture(tmp, sft)
tmp = np.array(tmp)

# normalize data
for i in range(0, len(tmp)):
    arr = np.array(tmp[i, :])
    arr = np.reshape(arr, (-1, 1))
    min_max_scaler = preprocessing.MinMaxScaler(feature_range=(0, 1))
    scalers.append(min_max_scaler)
    scaled = min_max_scaler.fit_transform(arr)
    for j in range(0, len(arr)):
        tmp[i, j] = scaled[j, 0]

# shuffle training and testing samples
tmp = np.rot90(tmp)
np.random.shuffle(tmp)

# train test split
trainTestSplit = int(len(tmp) * 0.8)


# define a model using data config on the head
class Sequence(nn.Module):
    def __init__(self):
        super(Sequence, self).__init__()
        self.lstm1 = nn.LSTM(config['lstm'][0], config["lstm"][1], config["lstm"][2])
        self.linear1 = nn.Linear(config["linear1"][0], config["linear1"][1])
        # self.linear2 = nn.Linear(config["linear2"][0],config["linear2"][1])

    def forward(self, input):
        output, (h_n, c_n) = self.lstm1(input)
        x = self.linear1(h_n)
        # x = self.linear2(x)
        return x


model = Sequence()
# define other necessary things
loss = nn.MSELoss()
optimizer = optim.SGD(model.parameters(), lr=0.001, momentum=0.89)


# prepare data to feed in to the model
def prepareData(arr, sf, sft):
    ans = []
    raw = arr[0:sf * 5]
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
    res = []
    for j in range(len(arr)-sft-1, len(arr)):
        res.append(arr[j] if not math.isnan(arr[j]) else 0.5)
    return (ans, [[res]])


# examine the folder to see whether the model has been trained, in particular it will look for modelname.pth.tar
if os.path.exists('./{a}.pth.tar'.format(a=modename)):
    model.load_state_dict(torch.load('./{a}.pth.tar'.format(a=modename)))
    model.eval()
else:
    # train the model
    for epoch in range(10):
        i = 0
        while i < trainTestSplit:
            model.zero_grad()
            if i % 30 == 0:
                print("training epoch{a},sample{b}".format(a=epoch, b=i))
            featuresShaped, Target = prepareData(tmp[i], sf, sft)
            input = torch.tensor(featuresShaped, dtype=torch.float)
            TargetOut = torch.tensor(Target, dtype=torch.float)
            output = model(input)
            Loss = loss(output, TargetOut)
            Loss.backward()
            optimizer.step()
            i += 1
    # save the model
    torch.save(model.state_dict(), "{a}.pth.tar".format(a=modename))

print("finished training.")
TestData = tmp[trainTestSplit:]


# function for denomalize data
def deNormalize(scaler, data):
    data = np.reshape(data, (-1, 1))
    data = scaler.inverse_transform(data)
    data = np.reshape(data, (1, -1))
    return data[0]


# predict and calculate mse for TestData, if you want to plot while predicting, decomment the code bellow
mse = 0
for j in range(0, len(TestData)):
    Input, TruthOut = prepareData(TestData[j], sf, sft)
    Input = torch.tensor(Input, dtype=torch.float)
    out = model(Input)
    data0 = TruthOut[0][0]
    data1 = out.detach().numpy()[0][0]

    data0 = deNormalize(scalers[-1], data0)
    data1 = deNormalize(scalers[-1], data1)

    # s0 = pd.Series(data=data0)
    # s1 = pd.Series(data=data1)

    # axs = s0.plot(color='red')
    # s1.plot(color='blue', ax=axs)
    # plt.show()

    mse += MSE(data0, data1)

mse /= len(TestData)
f = open('{a}.txt'.format(a=modename), 'w+')
for key, val in config.items():
    f.write("{a}:{b}\n".format(a=key, b=val))
f.write('avg mse:{a}'.format(a=mse))
f.close()

print("avg mse:{a}".format(a=mse))
