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
            'detail': {}

        }
        return data_dict

    def req_(self, url, method, data=None, param=None):
        prox = self.proxys
        if method == 'get':
            res = self._session.get(url=url, headers=self.headers, data=data, params=param, proxies=prox, verify=False,
                                    timeout=60)
        else:
            res = self._session.post(url=url, headers=self.headers, data=data, params=param, proxies=prox, verify=False,
                                     timeout=60)
        if res.status_code == requests.codes.ok:
            # print(res.status_code)
            res_data = res.text
            return res_data

    def request_(self, url, method, data=None, param=None):
        try:
            # time.sleep(random.random() * 10)
            res = self.req_(url, method, data, param)
        except Exception as e:
            print(e)
            logging.info("proxy disabled！！！ change proxy")
            time.sleep(random.random() * 10)
            self.replace_ip()
            res = self.req_(url, method, data, param)
        return res

    def get_data_detail(self, res):
            detail_list=list()
            for detail in res.xpath('//tbody/tr'):
                detail_dict = {}
                proname = detail.xpath("./td[@class='code-purchaseProjectName']/text()")
                if proname:
                    proname = proname[0].replace('\u3000','')
                price = detail.xpath("./td[@class='code-budgetPrice']/text()")
                if price :
                    dor=float(price[0])/10000
                    price = round(dor,2)
                require = detail.xpath("./td[@class='code-purchaseRequirementDetail']/text()")
                if require:
                    require = require[0]
                futher = detail.xpath("./td[@class='code-estimatedPurchaseTime']/text()")
                if futher:
                    futher=futher[0]
                    if '年' in futher:
                        futher = int(time.mktime(time.strptime(futher.strip(), "%Y年%m月")))  #
                    else:
                        futher = int(time.mktime(time.strptime(futher.strip(), "%Y-%m")))  #
                comment = detail.xpath("./td[@class='code-remark']/text()")
                if comment:
                    comment = comment[0]

                detail_dict['proname'] = proname
                detail_dict['price'] = price
                # detail_dict['protype'] =
                detail_dict['require'] = require
                detail_dict['futher'] = futher
                detail_dict['comment'] = comment
                detail_list.append(detail_dict)
                # print( proname,price,require,futher,comment)

            return detail_list
        # except Exception as e:
        #     logging.error(f"list获取失败{e}\n{traceback.format_exc()}")

    def get_data_info(self, url):
        # id='1467440'
        res = self.request_(url,method='get')
        return res

    def get_data_list(self, page):
        url = 'http://www.ccgp-shanghai.gov.cn/front/search/category'
        payload = {
            'categoryCode':"ZcyAnnouncement10016",
            'pageNo': page,
            'pageSize':15,
            'utm':"sites_group_front.2ef5001f.0.0.ea5361d05cc111eda9bbfdfb393a9737"}
        method='post'
        res = self.request_(url, method,json.dumps(payload))
        if res:
            # print(res)
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
            for data in data_list['hits']['hits']:
                lis=data['_source']
                # releasetime = int(time.mktime(time.strptime(lis['publishDate'], "%Y-%m-%d %H:%M:%S")))
                releasetime = int(lis['publishDate']/1000)
                todaytime = int(time.mktime(time.strptime(times, "%Y-%m-%d")))
                # print(releasetime,todaytime)
            #     return lis
                if releasetime >= todaytime:
                    prodict = spider.article_field()
                    districtName = lis['districtName'].replace('本级','')
                    articleId=lis['articleId']
                    title=lis['title']
                    prodict['districtName'] = districtName
                    prodict['articleId'] =articleId
                    prodict['publishDate'] = releasetime
                    prodict['title'] = title
                    detailurl=f'http://www.ccgp-shanghai.gov.cn/front/search/mobile/detail?id={articleId}&timestamp={int(time.time())}'
                    print(detailurl)
                    content = spider.get_data_info(detailurl)
                    prodict['detailurl']=detailurl
                    if content:
                        html=json.loads(content).get('result').get('content')
                        detail_data = etree.HTML(html)
                        prodict['procurement'] = detail_data.xpath("//samp[@class='bookmark-item uuid-1610438087802 code-singleChoicePurchaser editDisable addContent drop-list-cls readonly']/text()")[0]
                        prodict['detail'] = spider.get_data_detail(detail_data)
                        # spider.write_data(file,str(prodict)+"\n")
                        mysqldb = serversql()
                        rundb(mysqldb, prodict)
                    print(detailurl)
                    print(prodict)

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

