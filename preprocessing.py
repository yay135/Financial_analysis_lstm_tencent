import dateparser as parser
import pandas as pd

from datetime import timedelta
from datetime import datetime
from pandas import Timestamp

import os

allSeries = {}
for file in os.listdir('.'):
    if file.endswith('.txt'):
        data = pd.read_csv(file, thousands=',', sep=' ', engine='python')
        data.columns = ['Date', 'BaiduIndex']
        m = int(data['BaiduIndex'].mean())
        gdate = None
        vals = []
        dates = []
        for index, row in data.iterrows():
            date = parser.parse(row['Date'])
            if gdate == None:
                gdate = date
            else:
                while gdate != date:
                    Stamp = Timestamp(gdate)
                    dates.insert(0, Stamp)
                    vals.insert(0, m)
                    gdate = gdate - timedelta(days=1)

            timeStamp = Timestamp(date)
            dates.insert(0, timeStamp)
            vals.insert(0, row['BaiduIndex'])
            gdate = gdate - timedelta(days=1)

        series = pd.Series(data=vals, index=dates)
        series.sort_index()

        key = './{a}.csv'.format(a=file.split('.')[0])
        allSeries[key] = series

    if file.startswith('^HSI') or file.startswith('TCEHY'):
        sdata = pd.read_csv(file)
        avgPrice = []
        Dates = []
        gdate = None
        Last = None
        for index, row in sdata.iterrows():
            timestamp = Timestamp(row['Date'])
            if gdate == None:
                gdate = timestamp
            else:
                while gdate != timestamp:
                    Dates.append(gdate)
                    avgPrice.append(Last)
                    gdate = gdate + timedelta(days=1)
            Dates.append(timestamp)
            avg = (row['Open'] + row['High'] + row['Low']) / 3
            avgPrice.append(avg)

            Last = avg

            gdate = gdate + timedelta(days=1)

        stocks = pd.Series(data=avgPrice, index=Dates)

        Key = './{a}.csv'.format(a=file.split('.')[0])
        allSeries[Key] = stocks

begin = parser.parse('1800-01-01')
end = datetime.now()
for key, se in allSeries.items():
    count = 0
    for index, val in se.iteritems():
        if count == 0:
            da = index.to_pydatetime()
            if da > begin:
                begin = da
        elif count == len(se) - 1:
            da = index.to_pydatetime()
            if da < end:
                end = da

        count += 1

for key, se in allSeries.items():
    for index, val in se.iteritems():
        if index in se.index and (index > end or index < begin):
            se.drop(labels=index, inplace=True)

for key, series in allSeries.items():
    gdate = None
    for index, val in series.iteritems():
        date = index.to_pydatetime()
        if gdate == None:
            gdate = date
        else:
            if gdate != date:
                print("failed")
                break
        gdate = gdate + timedelta(days=1)
    print("success")

for key, se in allSeries.items():
    se.to_csv(path=key, encoding='utf-8')
