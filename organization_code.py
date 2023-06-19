import datetime
import logging
import threading
import time
import traceback
from multiprocessing import Process

from spider.redis_company import company_four_over
from spider.sikuyipingminspider import MinSpider
from spider.sql import serch_siku, excute_mysql

# zzlb=searchzzlb(certs[0].get('certName'))['id']
#     print(zzlb)
#     if not zzlb:
#         zzlb = 0.0


def searchdb():
    sql = "select aid,zzlb ,tyshxydm,xiangmu,zizhi,rynum from yunqi_addon17;"
    data = excute_mysql(sql)
    return data

def searchzzlx(kid):
        sql = "select zzmc from yunqi_addon17_zzlx where (kid='{}')".format(kid)
        data = excute_mysql(sql)
        return data


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
                scthread = threading.Thread(target=spider.run_search_base_cert, args=(cid,cname), )
                scthread.start()
                threads.append(scthread)
            for thread in threads:
                thread.join()
            spider.companyset.clear()
            spider.randomtime()
    except Exception as e:
        logging.error(f"get_company_base_cert 获取失败{e}\n{traceback.format_exc()}")

def run_base():
    company_list = list(serch_siku())
    lists = []
    start = 0
    for a in range(1):
        end = start + 1
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


def search_yunqi_cai():

    sql = "select name from aid;"
    data= excute_mysql(sql)
    return data



if __name__ == '__main__':
    # get_company_base_cert_readfile(fil)
    # get_redis_company_id_base_cert(fil)

    # while True:
    #     run_base()
    #     print('获取base_cert')
    data = searchdb()
    print(data)
    qiid = set()
    if data[4] > 0:
        qiid.add(data[0])
        if data[1] < 1:
            cretname = searchzzlx(data[0])
            if len(cretname) > 0:
                print(cretname[0])
            else:
                with open('spider/', 'a', encoding='utf-8') as w:
                    w.write(cretname)
        time.sleep(222222)