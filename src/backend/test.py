# import json
# from time import sleep
# f = open('../../data/data.json', 'r')
# a = json.load(f)
# start, o, h, l, c, v = a['chart']['data'][-1]
# f.close()
# for i in range(100):
#     sleep(1)
#     start = start + 1e6
#     o+=5
#     h+=5
#     l+=5
#     c+=5
#     v+=5
#     data = {"candle": "[{},{},{},{},{},{}]".format(start, o, h, l, c, v)}
#     print(data['candle'])


import datetime
ms = 1554185600000.0
print(datetime.datetime.fromtimestamp(ms/1000.0))
