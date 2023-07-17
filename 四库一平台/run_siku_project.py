import datetime
import logging
import threading
import time
import traceback
from multiprocessing import Process

from params_setting import get_params
from spider.sikuyipingminspider import MinSpider
from spider.sql import serch_siku
from spider.sql import searchdb




def get_company_project(get_company_project):
    try:
        spider = MinSpider()
        spider.replace_ip()
        while True:
            times = str(datetime.date.today())
            if spider.booltime(times):  # is true wating 1h
                print('waiting1h......')
                time.sleep(3600)
            if len(get_company_project) >= 10:
                rangenum = 10
            elif 0 < len(get_company_project) < 10:
                rangenum = len(get_company_project)
            else:
                break
            threads = []
            for n in range(rangenum):
                companybase = get_company_project.pop()
                cname = companybase[0].replace('\n','')
                cid = companybase[1]
                project=searchdb(cname)
                print(cname ,cid, project)
                # time.sleep(2222)
                if project :
                    if project[2]>0:
                        scthread = threading.Thread(target=spider.get_project_info1,args=(project[2],cid,cname), )
                        scthread.start()
                        threads.append(scthread)
            for thread in threads:
                thread.join()
            spider.companyset.clear()
            spider.randomtime()
    except Exception as e:
        logging.error(f"get_company_base_cert 获取失败{e}\n{traceback.format_exc()}")


def run_project(param):
    company_list = list(serch_siku())
    lists = []
    start = param[0]  # person_params[0]开始数  person_params[1] 迭代次数 person_params[2]增加个数
    for a in range(param[1]):
        end = start + param[2]
        print(start, end)
        if int(datetime.datetime.now().day) % 2 == 0:
            lists.append(company_list[start:end])
        else:
            lists.append(company_list[end:start:-1])
        start = end
    process = []
    for companies in lists:
        # get_company_base_cert(fil,companies)
        print(companies)
        p = Process(target=get_company_project, args=(companies,))
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
             # params[0]开始数  params[1] 迭代次数 params[2]增加个数

            run_project(param)
            print('获取project')
        print('完成，休息25分继续')
        time.sleep(1500)

