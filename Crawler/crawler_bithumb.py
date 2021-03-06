from datetime import datetime

import requests as rq
import time
import datetime
import numpy as np
from pip.compat import total_seconds

'''
Collect cryptocurrency data

parameter
- path : .csv file path that will be saved
- coins : coin list that want to collect data

returns
- none
'''
def collect_data(path, coins):
    interval = int(total_seconds(datetime.timedelta(days=14)) * 1000)
    start = datetime.datetime(year=2013, month=6, day=1, hour=0, minute=0)
    start = int(start.timestamp() * 1000)
    end = datetime.datetime.now()
    end = int(end.timestamp() * 1000)

    url = 'http://index.bithumb.com/api/coinmarketcap/localAPI.php'

    target = start
    print("Collecting coin data : ",coins)

    arr = []
    title = []  # title of columns
    title.append("time")

    for coin in coins:
        title.append(coin)

    arr.append(title)

    while (target <= end):
        json_list = []
        json_len = 0

        for coin in coins:

            if target + interval >= end:
                res = rq.get(url, params={
                    'api': 'graph',
                    'coin': 'btc',
                    'subject': 'price_usd',
                    'start': target,
                    'end': end
                })
            else:
                res = rq.get(url, params={
                    'api': 'graph',
                    'coin': 'btc',
                    'subject': 'price_usd',
                    'start': target,
                    'end': target + interval
                })

            if (coin == 'btc'):
                json_len = len(res.json())

            temp = []
            if len(res.json()) < json_len:  # add default values
                for i in range(json_len - len(res.json())):
                    temp.append([0, 0])

                temp = temp + res.json()
                json_list.append(temp)
            else:
                json_list.append(res.json())

        target = target + interval

        for i in range(json_len):
            row = []
            row.append(time.ctime(json_list[0][i][0] / 1000))  # add timestamp

            for j in range(len(json_list)):
                row.append(json_list[j][i][1])

            arr.append(row)

    np.savetxt(path, arr, delimiter=',', fmt="%s")
    print("Coin data saved in : ", path)
