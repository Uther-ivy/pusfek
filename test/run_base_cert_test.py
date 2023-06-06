import datetime
import logging
import threading
import traceback
from spider.sikuyipingminspider import MinSpider, read_file
from spider.sql import serch_siku, serch_siku_id


def get_company_base_cert(fil):
    try:
        company_base_cert_list = list(serch_siku())


        # company_base_cert_list = [serch_siku_id('七台河市廷东建筑工程有限公司')]
        print(company_base_cert_list,len(company_base_cert_list))
        # spider = MinSpider(fil)
        # spider.replace_ip()
        # print(type(company_base_cert_list),len(company_base_cert_list),company_base_cert_list)
        # while True:
        #     threads = []
        #     if len(company_base_cert_list) >= 10:
        #         rangenum = 10
        #     elif 0 <len(company_base_cert_list) < 10:
        #         rangenum = len(company_base_cert_list)
        #     else:
        #         break
        #     for n in range(rangenum):
        #         companybase= company_base_cert_list.pop()
        #         cname = companybase[0]
        #         cid = companybase[1]
        #         scthread = threading.Thread(target=spider.run_search_base_cert, args=(cid, fil, cname),)
        #         scthread.start()
        #         threads.append(scthread)
        #     for thread in threads:
        #         thread.join()
        #     spider.companyset.clear()
        #     spider.randomtime()
    except Exception as e:
        logging.error(f"def excute_company 获取失败{e}\n{traceback.format_exc()}")


if __name__ == '__main__':
    fil = str(datetime.datetime.today().strftime('%Y-%m-%d'))
    get_company_base_cert(fil)

    # ls = os.listdir('企业名称')
    # print(ls)
    # for i in ls[1:30]:
    #     print(i)
        # for n in read_file(f'企业名称/{i}'):
        #     n.replace('\n','')
