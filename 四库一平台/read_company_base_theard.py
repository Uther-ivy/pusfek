import datetime
import logging
import os
import sys
import threading
import time
import traceback
from multiprocessing import Process

from spider.sikuyipingminspider import read_file
from spider.sikuyipingminspider import MinSpider
from spider.sql import searchdb


def get_company_base_cert_readfile(fil,files):
    try:
        reads = read_file(files)
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
                continue
        if len(company_list)==0:
            print('company_list is',company_list)
            sys.exit()
        spider = MinSpider(fil)
        spider.replace_ip()
        print(type(company_list), len(company_list), company_list)
        while True:
            if spider.booltime():  # is true wating 1h
                print('wait1h......')
                time.sleep(3600)
            threads = []
            if len(company_list) >= 5:
                rangenum = 5
            elif 0 < len(company_list) < 5:
                rangenum = len(company_list)
            else:
                break
            for n in range(rangenum):
                companybase=company_list.pop()
                cname = companybase[0].replace('\n', '')
                cid = companybase[1]
                scthread = threading.Thread(target=spider.run_search_base_cert, args=(cid, fil, cname),)
                scthread.start()
                threads.append(scthread)
            for thread in threads:
                thread.join()
            spider.companyset.clear()
            spider.randomtime()
    except Exception as e:
        logging.error(f"get_company_base_cert 获取失败{e}\n{traceback.format_exc()}")
        print(files)
def theard_reads():
    fil = str(datetime.datetime.today().strftime('%Y-%m-%d'))
    process = []
    osdir=os.listdir('./READS_C')
    for a in osdir:
        ostxt = os.listdir(f'./READS_C/{a}')
        for t in ostxt:
            print(f'./READS_C/{a}/{t}')
            files=f'./READS_C/{a}/{t}'
            p = Process(target=get_company_base_cert_readfile, args=(fil,files))
            print(p.name)
            p.start()
            p.join()
            # process.append(p)
        # for pro in process:
        #     pro.join()
    print('采集完成')


if __name__ == '__main__':
    theard_reads()