import datetime



import time
# dates = 1692852257.003
dates = 1692062860.956
# dates='2022-10-18'
# time.strftime('%Y-%m-%d', time.localtime())
print(time.time())
print('获取当前年月日时分秒：',datetime.datetime.now())
print('获取今年月日-------：',datetime.date.today())
print('转换时间元组-------：',time.strptime(str(datetime.date.today()), "%Y-%m-%d"))
print('时间戳转2023-11-30：',datetime.datetime.fromtimestamp(dates).strftime("%Y-%m-%d %H:%m:%S"))
print('2023-11-30转时间戳：',time.mktime(time.strptime(str(datetime.date.today()), "%Y-%m-%d")))
# 1682438400
# if isinstance(dates, int):
#     print(time.localtime())
    # futher = time.strftime('%Y-%m', time.localtime(futher/1000))
