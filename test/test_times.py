import datetime



import time
# dates = 1669823999000
# dates='2022-10-18'
# time.strftime('%Y-%m-%d', time.localtime())
# futher=datetime.datetime.fromtimestamp(dates / 1000).strftime("%Y-%m-%d")
# print(futher)
today_date= datetime.date.today()
today_str = time.strptime(str(today_date), "%Y-%m-%d")
today_str2 = int(time.mktime(today_str))
print(today_date,today_str,today_str2)
print(int(time.mktime(time.strptime(str(datetime.date.today()), "%Y-%m-%d"))))
print(datetime.datetime.now())
# 1682438400
# if isinstance(dates, int):
#     print(time.localtime())
    # futher = time.strftime('%Y-%m', time.localtime(futher/1000))
