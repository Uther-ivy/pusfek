import datetime
import json
import logging
import os
import re
import sys
import threading
import time
import traceback
from urllib.parse import quote

from pypinyin import lazy_pinyin

# from spider.redis_company import company_four
from spider.redis_company import company_four
from spider.sikuyipingminspider import MinSpider, read_file
from spider.sql import search_yunqi_cai, search_cai, del_cname, serch_siku, serch_siku_id, searchdb, insert_base


def excute_company():
    try:
        times = str(datetime.date.today())
        fil = f'company_id{times}.txt'
        spider = MinSpider()
        spider.replace_ip()
        companylist = read_file('errorcompany2023-06-27.txt')
        # companylist = read_file('./test_siku/companyname/errorname2.txt')
        # companylist=[
        #     # '东营格瑞电子科技有限公司','泰安市恒泰消防工程有限公司','山东中优建设工程有限公司',
        #     '新疆华博建筑工程有限公司',
        #     '西藏曲协建设工程有限公司',
        #     '广州晟开工程有限公司',
        #     '西藏添宝建筑工程有限公司',
        #     '中交（三沙）开发建设有限公司',
        #     '青海平垣建设工程有限公司',
        #     '西藏斯巴尔建设有限公司',
        #     '新疆毫美建筑工程有限责任公司',
        #     '新疆百诚建筑工程有限公司',
        #     '西藏桥穆玉日建筑工程有限责任公司',
        #     '新疆振峰工程建设有限公司',
        #
        # ]#
        print(companylist)
        while True:
            threads = []
            if len(companylist)>=10:
                rangenum=10
            elif len(companylist)<10 and len(companylist)>0:
                rangenum=len(companylist)
            else:
                break
            for n in range(rangenum):
                companyname = companylist.pop()
                if companyname:
                    print(companyname)

                    threadid = threading.Thread(target=spider.get_company_id, args=(companyname, fil), )
                    threadid.start()
                    threadid.join()
                else:
                    print('companyname 执行完毕')
                    break
            print(spider.companyset)
            for company in spider.companyset:
                companybase=eval(company)
                print(companybase)
                cid=companybase[1]
                cname=companybase[0]
                # scthread = threading.Thread(target=spider.companysearch, args=(cid, cname,times), )
                scthread = threading.Thread(target=spider.run_search_base_cert, args=(cid, cname,times), )
                print('*' * 20, scthread.getName(), '*' * 20)
                scthread.start()
                threads.append(scthread)
            for thread in threads:
                thread.join()
            spider.companyset.clear()
            spider.randomtime()
    except Exception as e:
        logging.error(f"excute_companyid获取失败{e}\n{traceback.format_exc()}")
def get_redis_company_id_base_cert():
    try:
        spider = MinSpider()
        spider.replace_ip()
        # while True:
        companys = set()
        while True:
            for n in range(10):
                company=company_four()
                # print(company)
                companys.add(company)
            print(companys)
            threads_name_id = []#遍历获取 name id
            for companyname in companys:
                threadid = threading.Thread(target=spider.get_company_id, args=(companyname, fil), )
                threadid.start()
                threads_name_id.append(threadid)
            for thread in threads_name_id:
                thread.join()
            threads_base_cert = []#遍历获取 base cert
            for base in spider.companyset:
                companybase=eval(base.replace('\n', ''))
                print(companybase)
                cname = companybase[0]
                cid = companybase[1]
                # time.sleep(2222)
                # scthread = threading.Thread(target=spider.companysearch, args=(cid, fil, cname),)
                scthread = threading.Thread(target=spider.run_search_base_cert, args=(cid, fil, cname),)
                scthread.start()
                threads_base_cert.append(scthread)
            for thread in threads_base_cert:
                thread.join()
            else:
                companys.clear()
                spider.companyset.clear()
                spider.randomtime()
    except Exception as e:
        logging.error(f"def get_redis_company_id_base_cert 获取失败{e}\n{traceback.format_exc()}")
def excute_company_read_file():
    times = str(datetime.date.today())
    # get_redis_company_id_base_cert(fil)
    spider = MinSpider()
    spider.replace_ip()
    company_list = read_file('errorcompany2023-06-27.txt')

    threads = []
    for company in company_list:
        # print(type(eval(company)),company)
        company = eval(company)
        cname = company[0]
        cid = company[1]
        scthread = threading.Thread(target=spider.run_search_base_cert, args=(cid, cname,times), )
        scthread.start()
        threads.append(scthread)
    for thread in threads:
        thread.join()
    spider.companyset.clear()
def excute_listdir_company():
    try:
        times = str(datetime.date.today())
        spider = MinSpider()
        spider.replace_ip()
        ls=os.listdir('企业名称')[35:40]
        print(ls)
        for i in ls:
            print(i)
            companylist = read_file(f'企业名称/{i}')
            # companylist=['云南建投第六建设有限公司']#唐山怡景市政园林绿化工程有限公司
            # print(companylist)
            while True:
                threads = []
                if len(companylist)>10:
                    rangenum=10
                elif len(companylist)<10 and len(companylist)>0:
                    rangenum=len(companylist)
                else:
                    break
                for n in range(rangenum):
                    companyname = companylist.pop().replace('\n', '')
                    print(companyname)
                    threadid = threading.Thread(target=spider.get_company_id, args=(companyname, times), )
                    threadid.start()
                    threadid.join()
                print(spider.companyset)
                for company in spider.companyset:
                    companybase=eval(company)
                    # print(companybase)
                    cid=companybase.get('cid')
                    cname=companybase.get('cname')
                    scthread = threading.Thread(target=spider.companysearch, args=(cid, fil, cname), )
                    print('*' * 20, scthread.getName(), '*' * 20)
                    scthread.start()
                    threads.append(scthread)
                for thread in threads:
                    thread.join()
                spider.companyset.clear()
                spider.randomtime()
    except Exception as e:
        logging.error(f"excute_companyid获取失败{e}\n{traceback.format_exc()}")

def get_company_cid():
    try:
        spider = MinSpider()
        spider.replace_ip()
        # companylist = read_file('企业名称/5.txt')
        # companylist = read_file('./test_siku/companyname/errorname2.txt')
        companylist = ['北京国华利晓建设工程有限公司\n', '北京众成天元建筑劳务有限公司\n',
                       '圣浩宇航（天津）建设工程有限公司\n', '陕西双普建筑工程有限公司\n', '上海晟港建设有限公司\n',
                       '河北地矿建设工程集团衡水公司\n', '北京中罡建建设工程有限公司\n', '陕西恒丰基业实业有限公司\n',
                       '创领智控科技（武汉）有限公司\n', '嘉兴市泽丰工程管理有限公司\n',
                       '天津京津医药谷建设发展有限公司\n', '厦门正欣茂建设工程有限公司\n']
        print(companylist)
        while True:
            threads = []
            if len(companylist)>=10:
                rangenum=10
            elif len(companylist)<10 and len(companylist)>0:
                rangenum=len(companylist)
            else:
                break
            for n in range(rangenum):
                companyname = companylist.pop()
                print(companyname)
                if companyname:
                    threadid = threading.Thread(target=spider.get_company_id, args=(companyname, fil), )
                    threadid.start()
                    threads.append(threadid)
            for thread in threads:
                thread.join()
            spider.companyset.clear()
            spider.randomtime()
    except Exception as e:
        logging.error(f"get_company_cid {e}\n{traceback.format_exc()}")
#获取公司基础信息和资质
def get_company_base_cert():
    try:
        # company_base_cert_list = list(serch_siku())
        company_base_cert_list = [serch_siku_id('福建省旺泰建设工程有限公司')]

        spider = MinSpider()
        spider.replace_ip()
        print(type(company_base_cert_list),len(company_base_cert_list),company_base_cert_list)
        while True:
            threads = []
            if len(company_base_cert_list) >= 10:
                rangenum = 10
            elif 0 <len(company_base_cert_list) < 10:
                rangenum = len(company_base_cert_list)
            else:
                break
            for n in range(rangenum):
                companybase= company_base_cert_list.pop()
                cname = companybase[0].replace('\n','')
                cid = companybase[1]
                scthread = threading.Thread(target=spider.get_project_info1, args=(cid, cname),)
                scthread.start()
                threads.append(scthread)
            for thread in threads:
                thread.join()
            # spider.companyset.clear()
        #     spider.randomtime()
    except Exception as e:
        logging.error(f"get_company_base_cert 获取失败{e}\n{traceback.format_exc()}")
def excute_new_company():
    try:
        spider=MinSpider()
        spider.replace_ip()
        for page in range(1,6):
            spider.get_new_company_id(page,fil)
        newcompanyset=spider.new_companyset
        print(newcompanyset)
        while True:
            threads = []
            if len(newcompanyset) > 10:
                rangenum = 10
            elif len(newcompanyset) < 10 and len(newcompanyset) > 0:
                rangenum = len(newcompanyset)
            else:
                break
            for n in range(rangenum):
                companybase= eval(newcompanyset.pop().replace('\n', ''))
                cid = companybase['cid']
                cname = companybase['cname']
                scthread = threading.Thread(target=spider.companysearch, args=(cid, fil, cname),)
                scthread.start()
                threads.append(scthread)
            for thread in threads:
                thread.join()
            # spider.companyset.clear()
            spider.randomtime()
    except Exception as e:
        logging.error(f"def excute_company 获取失败{e}\n{traceback.format_exc()}")

#获取人员
def get_company_person(fil):
    try:
        company_base_cert_list = list(serch_siku())
        spider = MinSpider(fil)
        spider.replace_ip()
        print(type(company_base_cert_list), len(company_base_cert_list), company_base_cert_list)
        while True:
            threads = []
            if len(company_base_cert_list) >= 10:
                rangenum = 10
            elif 0 < len(company_base_cert_list) < 10:
                rangenum = len(company_base_cert_list)
            else:
                break
            for n in range(rangenum):
                companybase = company_base_cert_list.pop()
                cname = companybase[0]
                cid = companybase[1]
                scthread = threading.Thread(target=spider.get_person_info,args=(cname,cid, fil), )
                scthread.start()
                threads.append(scthread)
            for thread in threads:
                thread.join()
            spider.companyset.clear()
        #     spider.randomtime()
    except Exception as e:
        logging.error(f"get_company_base_cert 获取失败{e}\n{traceback.format_exc()}")
def get_company_person_readfile(fil):
    try:
        company_base_cert_list = read_file('company_id2023-04')
        spider = MinSpider(fil)
        spider.replace_ip()

        print(type(company_base_cert_list), len(company_base_cert_list), company_base_cert_list)
        # time.sleep(2222)
        while True:
            threads = []
            if len(company_base_cert_list) >= 10:
                rangenum = 10
            elif 0 < len(company_base_cert_list) < 10:
                rangenum = len(company_base_cert_list)
            else:
                break
            for n in range(rangenum):
                companybase = eval(company_base_cert_list.pop())
                cname = companybase[0].replace('\n','')
                cid = companybase[1]
                scthread = threading.Thread(target=spider.get_person_info,args=(cname,cid, fil), )
                scthread.start()
                threads.append(scthread)
            for thread in threads:
                thread.join()
            spider.companyset.clear()
            spider.randomtime()
    except Exception as e:
        logging.error(f"get_company_base_cert 获取失败{e}\n{traceback.format_exc()}")


def get_company_project_():
    try:

        get_company_project = [serch_siku_id('四川川交路桥有限责任公司')]
        print(get_company_project)
        spider = MinSpider()
        spider.replace_ip()
        while True:
            threads = []
            if len(get_company_project) >= 10:
                rangenum = 10
            elif 0 < len(get_company_project) < 10:
                rangenum = len(get_company_project)
            else:
                break
            for n in range(rangenum):
                companybase = get_company_project.pop()
                cname = companybase[0].replace('\n','')
                cid = companybase[1]
                project=searchdb(cname)
                print(cname ,cid, project)
                # time.sleep(2222)
                if project :
                    if project[2] > 0:
                        # spider.get_project_info(project[2], cid, cname)
                        scthread = threading.Thread(target=spider.get_project_info1,args=(project[2],cid,cname), )
                        scthread.start()
                        threads.append(scthread)
            for thread in threads:
                thread.join()
            spider.companyset.clear()

    except Exception as e:
        logging.error(f"get_company_base_cert 获取失败{e}\n{traceback.format_exc()}")


def excute_yunqi_cai(fil):
    try:
        companylist=list(search_yunqi_cai())
        # print(companylist)
        spider = MinSpider(fil)
        spider.replace_ip()
        while True:
            threads = []
            if len(companylist) > 10:
                rangenum = 10
            elif len(companylist) < 10 and len(companylist) > 0:
                rangenum = len(companylist)
            else:
                break
            for n in range(rangenum):
                companyname = companylist.pop()
                print(companyname)
                threadid = threading.Thread(target=spider.get_company_id, args=(companyname[0], fil), )
                threadid.start()
                threadid.join()
            for company in spider.companyset:
                companybase = eval(company)
                print(companybase)
                cid = companybase.get('cid')
                cname = companybase.get('cname')
                if search_cai(cname):#if exist ,delete companyname
                    del_cname(cname)
                scthread = threading.Thread(target=spider.companysearch, args=(cid, fil, cname), )
                print('*' * 20, scthread.getName(), '*' * 20)
                scthread.start()
                threads.append(scthread)
            for thread in threads:
                thread.join()
            spider.companyset.clear()
            spider.randomtime()
    except Exception as e:
        logging.error(f"excute_companyid获取失败{e}\n{traceback.format_exc()}")

def insertbase():
    data=0

    insert_base(data)
def testxinyongdaima(name):
    name = name.replace('\n', '')
    url = f"https://sky.mohurd.gov.cn/skyapi/api/statis/getResult?_t=0.41493411788348533&keys=corp%2Fdata_search" \
          f"%2Fpage&qyTypeCode=&aptCode=&regionNum=&pageNumber=1&pageSize=15&keyWord={quote(name)}"
    spider=MinSpider()
    resdata = json.loads(spider.jiemi_(spider.request_(url, types='cid')['data']))[0]['data']['records']
    print('get_company_id:', resdata)


if __name__ == '__main__':
    fil='2023-02-14'
    # company_list = list(serch_siku())
    # print(company_list)
    # print(len(company_list))
    # fil = str(datetime.datetime.today().strftime('%Y-%m-%d'))
    # insertbase()
    # testxinyongdaima('91610800064834709T')
    # excute_company()
    # get_company_cid()
    # get_company_project_()

    # get_company_project_(fil)
    # get_company_base_cert(fil)
    # get_redis_company_id_base_cert(fil)
    # excute_read_company(fil)
    # excute_new_company(fil)
    # excute_listdir_company(fil)
    # excute_yunqi_cai(fil)
    excute_company()
    # excute_company_read_file()

# companylist = read_file('企业名称/1.txt')[::-1]
    # print(companylist)
    # print(companylist)

    # data='IZgvAGrUV31JJr52HNx0ahGAcuOGR/CyJmx2mLq/hwARt9HRysi1vMN6pi7vyr+DCKIN8X/Sw0BpTqje/kCa7Tm6BgB2+61JA2DSEeKnC60bp32JrqTPNrn6Ug/QQaknYNs6UPHmvpHJTmzPfdhx0t1EhofhKwqEN8SKENZW1/9036mHk7kmrSYMNXMaQQO2hF9b+knEMdF2MEz2lw1sZqUcHsPPJRslS4c0p4zaqXjZ1/6J8/wUt0+jBDNBYeSOrptPPHCH0shWEMizBlW1ogCII1f6DInU2kWwUBSThELGqHNQsTN4MAypBqheg7qquonxF6MclLv/SKZz606agM2t5U3fzqFSaYCVGu9pmjnl9y5JETNdf1knqQelghbiZfF0DrZhvF+0y2ynD83aaNLHi9MykTNdZOKNSKGoi6Ud+8q/UjyRQa1Gs2JI04XVmBJyJCxrZ1PtM9CN87VNgLYNuPcvBFpOb8NvIIqfQdv6d56CxHMdI06wbDujQoi4Erayi+L49wV4qCVmZT86iwjruIfZLIOiL44auik4H2Ou8qXLmDIL42TSL+v7tyRK'
    # spider = MinSpider()
    # spider.replace_ip('person')
    # times = str(datetime.date.today())
    # fil = f'company_id{times}.txt'
    # print(spider.get_company_id('兴泰建工有限公司',fil))
    # print(spider.get_person_info('002105291240532876', {'aa':'aa'}))
    # print('昆明市晋宁县晋城镇三合、安乐片区2014年城市棚户区改造项目（一期）-301~310#(住宅）、会堂、地下室')
    # print(spider.get_safeuser('5104031601040101','project'))
    # print(spider.get_manageuser('5301222101220002','project'))
    # print(spider.get_operation('5301222101220002','project'))
    # print(spider.get_mechanics('5301222101220002','project'))
    # print(spider.get_censor('5301222101220002','project'))
    # print(spider.get_censor_user('3710811702090101','project'))
    # print(spider.get_safeuser('5301222101220002','project'))
    # print(spider.jiemi_(data))
    # spider.get_unit('3714252211010001','project')
    # spider.get_unit('3703232212270001','project')
    # print(spider.get_person_info('攀枝花市一通建筑工程有限责任公司','002105291258788267',fil))
    # print(spider.get_company_info('5118022207150001'))
    # sql_seach('2023-02-10')
    # while True:
    #     print(spider.randomtime())
    # for a in read_file('remain2023-05-13.text'):
    #     ww=eval(a)
    #     print(type(ww),len(ww))
