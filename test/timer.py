import json
import os
import random
import sys
import time

import schedule

data_dict={}




def run_job():
    os.system(f'python ./os_test.py')

if __name__ == '__main__':
    print("everyday to run in 9 12 18 23")
    schedule.every().day.at("6:03:20").do(run_job)

    while True:
        schedule.run_pending()
        time.sleep(random.random() * 2)

    # print(file)
