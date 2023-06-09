import datetime
import logging
import random
import sys
import threading
import time
import traceback

import schedule

from spider.redis_company import company_four_over
from spider.sikuyipingminspider import MinSpider, wirte_file
from spider.sql import insert_skid, searchdb


def excute_new_company_thread():
    while True:
        try:
            times = str(datetime.date.today())
            fil=f'company_id{times}.txt'
            spider=MinSpider()
            if spider.booltime(times):  # is true wating 1h
                print('exiting......')
                wirte_file(fil, data=1)
                return
            spider.replace_ip()
            for page in range(1, 11):
                spider.get_new_company_id(page,fil)
            newcompanyset=spider.new_companyset
            companys = set()
            print(newcompanyset)
            while True:
                threads = []
                if len(newcompanyset) >= 10:
                    rangenum = 10
                elif 0 < len(newcompanyset) < 10:
                    rangenum = len(newcompanyset)
                else:
                    break
                for n in range(rangenum):
                    companybase= eval(newcompanyset.pop().replace('\n', ''))
                    cname = companybase[0]
                    companys.add(cname)
                    cid = companybase[1]
                    psnum = searchdb(cname)
                    print(cname, cid, psnum)
                    if psnum == None:
                        # scthread = threading.Thread(target=spider.run_search_base_cert, args=(cid, cname),)
                        scthread = threading.Thread(target=spider.companysearch, args=(cid, cname),)
                        scthread.start()
                        threads.append(scthread)
                for thread in threads:
                    thread.join()
                for cname in companys:
                    company_four_over(cname)
                spider.companyset.clear()
                spider.randomtime()
        except Exception as e:
            logging.error(f"def excute_new_company 获取失败{e}\n{traceback.format_exc()}")
        rand=300+random.random()*500
        print(f"waiting {rand}s")
        time.sleep(rand)

def excute_new_company():
    try:
        times = str(datetime.date.today())
        fil=f'company_id{times}.txt'
        spider=MinSpider()
        if spider.booltime(times):  # is true wating 1h
            print('waiting1h......')
            time.sleep(3600)
        spider.replace_ip()
        for page in range(1,15):
            spider.get_new_company_id(page,fil)
        newcompanyset=spider.new_companyset
        print(newcompanyset)
        while True:

            # threads = []
            if len(newcompanyset) > 10:
                rangenum = 10
            elif len(newcompanyset) < 10 and len(newcompanyset) > 0:
                rangenum = len(newcompanyset)
            else:
                break
            for n in range(rangenum):
                companybase= eval(newcompanyset.pop().replace('\n', ''))
                cname = companybase[0]
                cid = companybase[1]
                psnum = searchdb(cname)
                print(cname, cid, psnum)
                if psnum == None:
                    print(cname, cid)
                    spider.companysearch(cid,cname)
            spider.randomtime()
    except Exception as e:
        logging.error(f"def excute_new_company 获取失败{e}\n{traceback.format_exc()}")




if __name__ == '__main__':
    excute_new_company_thread()
    print('after waiting 1h ,start timer..... ')
    schedule.every().day.at("01:03:22").do(excute_new_company_thread)
    print('after waiting 1h ,start timer..... ')
    while True:
        schedule.run_pending()
        time.sleep(random.random() * 2)

