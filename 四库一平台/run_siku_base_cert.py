import datetime
import logging
import random
import sys
import threading
import time
import traceback
from multiprocessing import Process

from params_setting import get_params
from run_siku_person import run_person
from run_siku_project import run_project
from spider.sikuyipingminspider import MinSpider, read_file, wirte_file
from spider.sql import serch_siku, searchdb


def get_company_base_cert(company_base_cert_list):
    try:
        print(company_base_cert_list)
        spider = MinSpider()
        spider.replace_ip()
        print(type(company_base_cert_list),len(company_base_cert_list),company_base_cert_list)
        while True:
            times = str(datetime.date.today())
            if spider.booltime(times):  # is true wating 1h
                print('waiting1h......')
                time.sleep(3600)
            threads = []
            if len(company_base_cert_list) >= 10:
                rangenum = 10
            elif 0 <len(company_base_cert_list) < 10:
                rangenum = len(company_base_cert_list)
            else:
                break
            companys =set()
            for n in range(rangenum):
                companybase = company_base_cert_list.pop()
                print(companybase)
                cname = companybase[0].replace('\n', '')
                cid = companybase[1]
                companys.add(cname)
                print(cname, cid)
                scthread = threading.Thread(target=spider.run_search_base_cert, args=(cid,cname,times), )
                scthread.start()
                threads.append(scthread)
            for thread in threads:
                thread.join()
            spider.companyset.clear()
            spider.randomtime()
    except Exception as e:
        logging.error(f"get_company_base_cert 获取失败{e}\n{traceback.format_exc()}")

def run_base(params):
    company_list = list(serch_siku())
    print(len(company_list))
    # time.sleep(222)
    lists = []
    start = params[0]
    for a in range(params[1]):
        end = start + params[2]
        if int(datetime.datetime.now().day) % 2 == 0:
            lists.append(company_list[start:end])
        else:
            lists.append(company_list[end:start:-1])
        start = end
    process = []
    for companies in lists:
        p = Process(target=get_company_base_cert, args=(companies,))
        print(p.name)
        p.start()
        process.append(p)
    for pro in process:
        pro.join()
    print('采集完成')






if __name__ == '__main__':
    # get_company_base_cert_readfile(fil)
    # get_redis_company_id_base_cert(fil)

    while True:
         for  param in  get_params():
            print(param)
            run_base(param)#params[0]开始数  params[1] 迭代次数 params[2]增加个数
            print('获取base_cert')
            run_person(param)
            print('获取person')
            run_project(param)
            print('获取project')
            print(datetime.datetime.now())
         time.sleep(random.random()*300)

        # run2()
    # while True:
    #     spider = MinSpider(fil)
    #     print(spider.booltime())
    # get_company_base_cert_readfile()
    # ls = os.listdir('企业名称')
    # print(ls)
    # for i in ls[1:30]:
    #     print(i)
        # for n in read_file(f'企业名称/{i}'):
        #     n.replace('\n','')
