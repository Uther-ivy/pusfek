import datetime
import logging
import os
import random
import threading
import time
import traceback

import schedule

from spider.sikuyipingminspider import read_file
from spider.sikuyipingminspider import MinSpider
from spider.sql import searchdb


def get_company_base_cert_readfile():
    try:
        times = str(datetime.date.today())
        # times='2023-06-25'
        fil = f'company_id{times}.txt'
        # fil = '2023-02-14'
        reads = read_file(fil)
        company_list = []
        for n in reads:
            try:
                companybase = eval(n)
                print(companybase)
                cname = companybase[0].replace('\n', '')
                psnum = searchdb(cname)
                print(cname, psnum)
                if psnum == None:
                    company_list.append(companybase)
            except:
                print()
                continue
        if len(company_list)>0:
            spider = MinSpider()
            spider.replace_ip()
            print(type(company_list), len(company_list), company_list)
            while True:
                threads = []
                if len(company_list) >= 10:
                    rangenum = 10
                elif 0 < len(company_list) < 10:
                    rangenum = len(company_list)
                else:
                    break
                for n in range(rangenum):
                    companybase=company_list.pop()
                    cname = companybase[0].replace('\n', '')
                    cid = companybase[1]
                    scthread = threading.Thread(target=spider.run_search_base_cert, args=(cid, cname,times),)
                    scthread.start()
                    threads.append(scthread)
                for thread in threads:
                    thread.join()
                spider.companyset.clear()
                spider.randomtime()

        else:
            print('company_list is []')
        os.remove(fil)
    except Exception as e:
        logging.error(f"get_company_base_cert 获取失败{e}\n{traceback.format_exc()}")




if __name__ == '__main__':

    get_company_base_cert_readfile()

    # print(' 23:40:00 start timer..... ')
    # schedule.every().day.at("23:40:00").do(get_company_base_cert_readfile)
    # print(' 23:40:00 start timer..... ')
    # while True:
    #     schedule.run_pending()
    #     time.sleep(random.random() * 2)
    # get_company_base_cert_readfile()
