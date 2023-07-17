import datetime
import logging
import random
import sys
import threading
import time
import traceback
from multiprocessing import Process

from params_setting import get_params
from spider.sikuyipingminspider import MinSpider, read_file, wirte_file
from spider.sql import serch_siku, serch_siku_id, searchdb


def get_company_person(get_company_person):
    try:
        spider = MinSpider()
        spider.replace_ip()
        while True:
            times = str(datetime.date.today())
            if spider.booltime(times):  # is true wating 1h
                print('waiting1h......')
                time.sleep(3600)
            threads = []
            if len(get_company_person) >= 10:
                rangenum = 10
            elif 0 < len(get_company_person) < 10:
                rangenum = len(get_company_person)
            else:
                break
            for n in range(rangenum):
                companybase = get_company_person.pop()
                cname = companybase[0].replace('\n','')
                cid = companybase[1]
                psnum= searchdb(cname)
                print(cname, cid, psnum)
                # time.sleep(2222)
                if psnum:
                    if psnum[4]>0:
                        scthread = threading.Thread(target=spider.get_person_info,args=(cname,cid), )
                        scthread.start()
                        threads.append(scthread)
            for thread in threads:
                thread.join()
            spider.companyset.clear()
            spider.randomtime()
    except Exception as e:
        logging.error(f"get_company_base_cert 获取失败{e}\n{traceback.format_exc()}")

def run_person(param):
    # params[0]开始数  params[1] 迭代次数 params[2]增加个数
    company_list = list(serch_siku())
    lists = []
    start =param[0]
    for a in range(param[1]):
        end = start + param[2]
        print(start, end)
        if int(datetime.datetime.now().day)%2==0:
            lists.append(company_list[start:end])
        else:
            lists.append(company_list[end:start:-1])
        start = end
    process = []
    for companies in lists:
        print(companies)
        p = Process(target=get_company_person, args=(companies,))
        print(p.name)
        p.start()
        process.append(p)
    for pro in process:
        pro.join()
    print('采集完成')






if __name__ == '__main__':

    while True:
        for param in get_params():
            print(param)
            run_person(param)
            print('获取person')
        print('完成，休息25分继续')
        time.sleep(1500)
