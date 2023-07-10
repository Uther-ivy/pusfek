import json
import logging
import os
import random
import re
import threading
import time
import traceback


import requests as requests
from lxml import etree

import ip_proxys
from caigouyixiang.cgyxdata.sql import serversql, rundb


class cgyxspider(object):
    def __init__(self):
        self._session=requests.session()
        self.proxys = {
            'http': '',
            'https': ''
        }
        self.headers= {
            'Content-Type': 'application/json',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36'
    }
        self.errors=0

    def replace_ip(self):

        proxy = ip_proxys.replace_ip()
        self.proxys = {
            'http': proxy,
            'https': proxy
        }
        print(self.proxys)

    def article_field(self):
        data_dict = {
            'districtName': '',
            'articleId': '',
            'publishDate': '',
            'procurement':'',
            'title': '',
            'detailurl':'',
            'detail': {}

        }
        return data_dict

    def req_(self, url,method,data=None,params=None):
        prox=self.proxys
        if method =='get':
            res = self._session.get(url=url, headers=self.headers,params=params, data=data, proxies=prox, verify=False, timeout=60)
        else:
            res = self._session.post(url=url, headers=self.headers, params=params,data=data, proxies=prox, verify=False, timeout=60)
        if res.status_code == requests.codes.ok:
            # print(res.status_code)
            res_data = res.content.decode()
            return res_data

    def request_(self, url, method, data=None,params=None):
        try:
            # time.sleep(random.random() * 10)
            res = self.req_(url,method,data,params)
        except Exception as e:
            print(e)
            logging.info("proxy disabled！！！ change proxy")
            time.sleep(random.random() * 10)
            self.replace_ip()
            res = self.req_(url,method,data,params)
        return res

    def get_data_detail(self, res):
        detail_list = list()
        content = etree.tostring(res.xpath("//div[@id='yxgk_content']")[0], method="HTML").decode()
        # size = len(res.xpath("//tbody/tr"))
        # for num in range(1, size):
        #     detail_dict = {}
        #     proname = res.xpath(f"//tr[@id='tr_num{num}']/td[2]/p/span/text()")
        #     if proname:
        #         proname = proname[0]
        #     require = res.xpath(f"//tr[@id='tr_num{num}']/td[3]/p/span/text()")
        #     if require:
        #         require = require[0]
        price = res.xpath(f"//tr[@id='tr_num1']/td[4]/p/span/text()")
        if price:
                price = price[0].replace('万元','').replace(',','')
        futher = res.xpath(f"//tr[@id='tr_num1']/td[5]/p/span/text()")
        if futher:
                futher =int(time.mktime(time.strptime(futher[0], "%Y%m")))
            # comment = res.xpath(f"//tr[@id='tr_num{num}']/td[6]/p/span/text()")
            # if comment:
            #     comment = comment[0]
            #
            # detail_dict['proname'] = proname
            # detail_dict['price'] = price
            # detail_dict['require'] = require
            # detail_dict['futher'] = futher
            # detail_dict['comment'] = comment
            # detail_list.append(detail_dict)
            # print( proname,price,require,futher,comment)

        return content,futher,price

    def get_data_info(self, url):
        # id='1467440'

        res = self.request_(url,method='get')
        return res

    def get_data_list(self, page):
        url = 'http://www.ccgp-hunan.gov.cn/mvc/getnewContentList1.do?'
        payload = {
            'column_code': '51,52',
            'title':'',
            'dept':'',
            'pub_time1':'',
            'pub_time2':'',
            'area_id': 1,
            'page': page,
            'pageSize': 18
        }
        method='post'
        res = self.request_(url, method,params=payload)
        # print(res)
        if res:
            return json.loads(res)

    def write_data(self,file,data):
        with open(file,'a',encoding='utf-8') as w:
            w.write(data)
            w.close()

    def err(self):
        self.errors=1
def run(page,spider,times,file):
    # try:

            data_list = spider.get_data_list(page)
            # print(data_list)
            for lis in data_list['rows']:
                # print(lis)
                releasetime = int(time.mktime(time.strptime(lis['STAFF_DATE'], "%Y-%m-%d")))
                # releasetime = lis['STAFF_DATE']
                todaytime = int(time.mktime(time.strptime(times, "%Y-%m-%d")))
                # print(releasetime,todaytime)
            #     return lis
                if releasetime >= todaytime:
                    prodict = spider.article_field()
                    districtName = lis['AREA_NAME']
                    articleId=lis['COLUMN_ID']
                    title=lis['TITLE']
                    prodict['procurement'] = lis['ORG_NAME']
                    prodict['districtName'] = districtName
                    prodict['articleId'] =articleId
                    prodict['publishDate'] = releasetime
                    prodict['title'] = title
                    # print(lis)
                    detailurl = f'http://www.ccgp-hunan.gov.cn/mvc/viewContent.do?columnId={articleId}'
                    prodict['detailurl']=detailurl
                    print(detailurl)
                    content = spider.get_data_info(detailurl)
                    if content:
                        detail_data = etree.HTML(content)
                        prodict['detail'],prodict['futher'],prodict['price'] = spider.get_data_detail(detail_data)
                        mysqldb = serversql()
                        rundb(mysqldb, prodict)
                    print(prodict)
                    # exit()

                    #
                else:
                    print(f'{times}今日获取完毕{page}页')
                    spider.err()

def main(page, times, file):
    threads = []
    spider = cgyxspider()
    spider.replace_ip()
    for num in range(1, page):
        # print(num)
        if spider.errors == 1:
            break
        t = threading.Thread(target=run, args=(num,),
                             kwargs={'spider': spider, 'times': times, 'file': file})
        time.sleep(5 + random.random() * 5)
        # print(spider.errors)
        threads.append(t)
        t.start()

    for thread in threads:
        thread.join()



if __name__ == '__main__':
    times = time.time()
    file = os.path.basename('../unit.txt')
    with open(file, 'r') as f:
        if os.path.exists(file):
            read = f.readline()
            f.close()
            base = json.loads(read)
            print(base['time'])
            main(base['page'], base['time'], base['file'])
    print(time.time() - times)

