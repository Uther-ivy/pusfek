import datetime
import logging
import random
import threading
import time
import traceback
from multiprocessing import Process
import schedule
from read_company_base import get_company_base_cert_readfile
from spider.redis_company import company_four, company_four_over
from spider.sikuyipingminspider import MinSpider, wirte_file
from spider.sql import searchdb, serch_siku_id


def get_redis_company_id_base_cert():
    try:
        spider = MinSpider()
        spider.replace_ip()
        while True:
            times=str(datetime.date.today())
            fil=f'company_id{times}.txt'
            if spider.booltime(times):  # is true wating 1h
                print('waiting1h......')
                wirte_file(fil,data=1)
                get_company_base_cert_readfile()
            companys = set()
            for n in range(10):
                cname=company_four()
                # psnum = searchdb(cname)
                # print(cname, psnum)
                # if not psnum:
                companys.add(cname)
            print(companys)
            # time.sleep(2222)
            threads_name_id = []#遍历获取 name id
            for companyname in companys:
                print(companyname)
                threadid = threading.Thread(target=spider.get_company_id, args=(companyname, fil))
                threadid.start()
                threads_name_id.append(threadid)
            for thread in threads_name_id:
                thread.join()
            threads_base_cert = []#遍历获取 base cert
            for base in spider.companyset:
                companybase=eval(base.replace('\n', ''))
                print(companybase)
                cname = companybase[0]
                if not searchdb(cname):
                    cid = companybase[1]
                    scthread = threading.Thread(target=spider.run_search_base_cert, args=(cid, cname),)
                    scthread.start()
                    threads_base_cert.append(scthread)
            for thread in threads_base_cert:
                thread.join()
            for cname in companys:
                company_four_over(cname)
            spider.companyset.clear()
            spider.randomtime()
    except Exception as e:
        logging.error(f"def get_redis_company_id_base_cert 获取失败{e}\n{traceback.format_exc()}")

def run2():
    process = []
    for a in range(10):
        p = Process(target=get_redis_company_id_base_cert)
        print(p.name)
        p.start()
        process.append(p)
    for pro in process:
        pro.join()
    print('采集完成')


if __name__ == '__main__':

    # print('after waiting 1h ,start timer..... ')
    # schedule.every().day.at("01:19:00").do(run2)
    while True:
        run2()
        # schedule.run_pending()
        # print('after waiting 1h ,start timer..... ')
        time.sleep(1000*random.random() * 500)
