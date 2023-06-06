import json
import os
import random
import time

import schedule

data_dict={}
def times_(date=None):
    if date:
        data_dict['time'] = date
        # print(date)
    else:
        date = time.strftime('%Y-%m-%d', time.localtime())
        data_dict['time'] = date
        # print(date)
def files_(fil):
    fil = fil.split('.')[0]
    file = f'./cgyxdata/{fil}.txt'
    data_dict['file'] = file
    # print(file)

def pages_( page):
    data_dict['page'] = page
    # print(page)


def job():
    times = time.time()
    print(times)
    files = os.listdir('./cgyxbase')
    # files = ['beijingcgyxspider.py']
    for file in files:
        if '__pycache__' not in file:
            times_()
            files_(file)
            pages_(20)
            # print(data_dict)
            f = open('unit.txt', 'w')
            f.write(json.dumps(data_dict))
            f.close()
            time.sleep(3 + random.random() * 2)
            # print(base.data_dict)
            os.system(f'python ./cgyxbase/{file}')
    print(time.time() - times)

if __name__ == '__main__':
    print("everyday to run in 9 12 18 23")
    schedule.every().day.at("23:30:00").do(job)
    schedule.every().day.at("09:12:00").do(job)
    schedule.every().day.at("10:00:00").do(job)
    schedule.every().day.at("12:00:00").do(job)
    schedule.every().day.at("15:00:00").do(job)
    schedule.every().day.at("20:00:00").do(job)
    while True:
        schedule.run_pending()
        time.sleep(random.random() * 2)

    # print(file)
