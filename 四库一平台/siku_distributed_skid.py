import datetime
import logging
import os
import threading
import traceback
from multiprocessing import Process

from spider.redis_company import company_four
from spider.sikuyipingminspider import MinSpider, read_file
from spider.sql import search_yunqi_cai, search_cai, del_cname, serch_siku_id, serch_siku


def get_company_cid1(fil):
    try:
        spider = MinSpider()
        spider.replace_ip()
        # companylist = read_file(fil)
        # companylist = read_file('./test_siku/companyname/errorname2.txt')
        companylist=[
            '山西德宇工程管理咨询有限公司',
            # '吉林亿北建设工程有限公司','攀枝花市一通建筑工程有限责任公司','内蒙古万兴建设有限公司',
        #     '贵州德亨环境科技工程有限公司','集安市清云市政设计有限公司','河北建设集团卓诚路桥工程有限公司','徐闻县第一建筑工程总公司',
        #     '青岛海洋工程勘察设计研究院','海南壹鼎建筑工程有限公司','广西巍海消防工程有限公司','广西好气派装饰有限公司',
        #     '西藏征程钢结构工程有限公司','新疆新烨建设工程有限公司','广西远邕建筑有限公司','华润混凝土（澄迈金江）有限公司',
        #     '中国十九冶集团（防城港）设备结构有限公司','唐山怡景市政园林绿化工程有限公司','新疆渝江建筑安装工程有限公司铁门关市分公司','新疆峰臻商贸有限公司',
        #     '沙湾耀能能源有限公司','铁门关市久远园林绿化工程有限公司','新疆尚坤建设工程有限责任公司','华夏子弟科技(新疆)有限公司',
        #     '铁门关市鑫泉商贸有限责任公司','新疆玖鑫商贸有限公司','铁门关市双博科技有限公司','铁门关市帮达商贸有限公司',
        #     '新疆运丰棉业机械有限公司','新疆中如新材料有限责任公司','新疆久泰钢结构工程有限公司','铁门关市中意新材料有限公司'
        ]#
        print(companylist)
        while True:
            threads = []
            if len(companylist)>10:
                rangenum=10
            elif len(companylist)<10 and len(companylist)>0:
                rangenum=len(companylist)
            else:
                break
            for n in range(rangenum):
                companyname = companylist.pop()
                print(companyname)
                if companyname:
                    threadid = threading.Thread(
                        target=spider.get_company_id, args=(companyname, fil), )
                    threadid.start()
                    threads.append(threadid)
            for thread in threads:
                thread.join()
            spider.companyset.clear()
            spider.randomtime()
    except Exception as e:
        logging.error(f"get_company_cid {e}\n{traceback.format_exc()}")

def run1():
    fil = str(datetime.datetime.today().strftime('%Y-%m-%d'))

    prolist=[]
    for ls in os.listdir('企业名称')[0:30]:
        fil='企业名称/'+ls
        print(fil)
        get_company_cid(fil)
    p = Process(target=get_company_cid, args=(fil,))
    print(p.name)
    p.start()
    prolist.append(p)
    for proces in prolist:
        proces.join()
    print('采集完成')

def get_company_cid(fil):
    try:
        spider = MinSpider()
        spider.replace_ip()
        while True:
            companylist = []
            for n in range(10):
                company=company_four()
                companylist.append(company)
            threads = []
            for n in range(len(companylist)):
                    companyname = companylist.pop()
                    # print(companyname)
                    if companyname:
                        threadid = threading.Thread(
                            target=spider.get_company_id, args=(companyname, fil), )
                        threadid.start()
                        threads.append(threadid)
            for thread in threads:
                thread.join()
            print(companylist)
            # spider.companyset
            # spider.companyset.clear()
            # companylist.clear()
            spider.randomtime()
    except Exception as e:
        logging.error(f"get_company_cid {e}\n{traceback.format_exc()}")

if __name__ == '__main__':
    # fil='2023-02-14'
    fil = str(datetime.datetime.today().strftime('%Y-%m-%d'))

    # get_company_cid(fil)
    get_company_cid1(fil)

    print('采集完成')


    # excute_new_company(fil)
    # excute_listdir_company(fil)
    # excute_yunqi_cai(fil)
    # excute_company(fil)
    # companylist = read_file('企业名称/1.txt')[::-1]
    # print(companylist)
    # print(companylist)

    # data='IZgvAGrUV31JJr52HNx0ahGAcuOGR/CyJmx2mLq/hwARt9HRysi1vMN6pi7vyr+DCKIN8X/Sw0BpTqje/kCa7Tm6BgB2+61JA2DSEeKnC60bp32JrqTPNrn6Ug/QQaknYNs6UPHmvpHJTmzPfdhx0t1EhofhKwqEN8SKENZW1/+/ALm/DXwXhHBhKIWImNRUYiQlAtMGa/JV1s0Zhmhrf7J4J4vIL/1cauF3dySedqV2ZhASFubpjDmr+av9DHa/EIXkS/LzGIarYeMz+0YnSwdSYp6A7C9uG4V3tB0PewpN0KLQl7UQzAtSeo6aEPbT10YQurL5qlcLvUOWodPPBq+Q6xaijUJOpYowLq1XDo4mVO+Nr2JxmDmZeJC6K8RIGU/4BxL1503qNJ9HAAQD1bLnUYN61dUIovwoD99+2HIT/z1LYKINX/4LuewulHDqb+IBRW/DwF1BhpijSvbnOEExJKiyEN9TIOaythCa/YPC8SMn9RqwCxVV+rwHizyuSY3M54VBBg704Uk6ROaUNdDHzxpfKC/H0mflW3Yw6HM8TtARy0SXRu26YcT1OhAVteUuATzsqt5DuCt/JhyoMTFVe9K9FHcT4Hod4rjNR+QoHtXPB6iZJ1vUBsJK8/5jl+AYD2nGTc9sikMty2EUmmJbLN4hcg/2Bo8TESBegVgBzG/COPDrxN6yAKHYbicLLQzzk/sG2JvUiJxuB389LV/PrMufDnPOe/qu4yh749E0MsedkTHlG/yTMEM9jywrb3ssedolkrrmQfGeFQLSg2kLZvQozQ5XLxl7uAOMQKD2r504QARUaDfqNcCbaQuB'
    # spider = MinSpider('2023-02-10')
    # spider.replace_ip()
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
    # print(spider.get_company_info('5118022207150001'))
    # sql_seach('2023-02-10')
    # while True:
    #     print(spider.randomtime())
