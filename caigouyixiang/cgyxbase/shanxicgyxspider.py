import json
import logging
import os
import random
import re
import threading
import time
import traceback
import urllib.parse

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
            'Referer':'http://www.ccgp-shanxi.gov.cn/luban/category?parentId=138010&childrenCode=ZcyAnnouncement&utm=luban.luban-PC-38306.959-pc-websitegroup-navBar-front.6.139d47d01bd611ee8ea4c5e8d2eaf12f',
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
            res_data = res.content.decode()
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

    def get_data_detail(self, url):
        print(url)
        html = self.request_(url, method='get')
        # print(html)
        content=json.loads(html).get('result').get('data').get('content')

        detail= etree.HTML(content)
            # size= detail.xpath('//tbody/tr')
            # for num in range(1,len(size)+1):
            #     detail_dict = {}
            #     proname = detail.xpath(f"//tbody/tr[{num}]/td[2]/text()")
            #     if proname:
            #         proname = proname[0].replace('\u3000','')
        price = detail.xpath(f"//td[@class='code-budgetPrice']/text()")
        if price :
                dor=float(price[0])/10000
                price = round(dor,2)
        # require = detail.xpath(f"//tbody/tr[{num}]/td[3]/text()")
        # if require:
        #         require = require[0]
        futher = detail.xpath(f"//td[@class='code-estimatedPurchaseTime']/text()")
        if futher:
                futher=futher[0]
                if '年' in futher:
                    futher = int(time.mktime(time.strptime(futher.strip(), "%Y年%m月")))  #
                else:
                    futher = int(time.mktime(time.strptime(futher.strip(), "%Y-%m")))  #
                # comment = detail.xpath(f"//tbody/tr[{num}]/td[7]/text()")
                # if comment:
                #     comment = comment[0]
                #
                # detail_dict['proname'] = proname
                # detail_dict['price'] = price
                # detail_dict['protype'] =
                # detail_dict['require'] = require
                # detail_dict['futher'] = futher
                # detail_dict['comment'] = comment
                # detail_list.append(detail_dict)
                # print( proname,price,require,futher,comment)

        return content,futher,price
        # except Exception as e:
        #     logging.error(f"list获取失败{e}\n{traceback.format_exc()}")




    def get_data_list(self, page):
        url = 'http://www.ccgp-shanxi.gov.cn/portal/category'
        payload = {"pageNo":page,"pageSize":15,"categoryCode":"ZcyAnnouncement10016","_t":int(time.time()*1000)}
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
    data_list = spider.get_data_list(page)
    datalist=data_list['result']['data']['data']
    for lis in datalist:
        # lis=data['_source']
        # releasetime = int(time.mktime(time.strptime(lis['publishDate'], "%Y-%m-%d %H:%M:%S")))
        releasetime = int(lis['publishDate']/1000)
        todaytime = int(time.mktime(time.strptime(times, "%Y-%m-%d")))
        print(releasetime,todaytime)
    #     return lis
        if releasetime >= todaytime:
            prodict = spider.article_field()
            districtName = lis['districtName'].replace('本级','')
            articleId=lis['articleId']
            title=lis['title']
            href=f'http://www.ccgp-shanxi.gov.cn/portal/detail?articleId={urllib.parse.quote(articleId)}&parentId=138010&timestamp={int(time.time())}'
            showurl=f'http://www.ccgp-shanxi.gov.cn/luban/detail?parentId=138010&articleId={articleId}&utm='
            prodict['districtName'] = districtName
            prodict['articleId'] =int(str(int(time.time()*100000+random.random()*200))[-6:])
            prodict['publishDate'] = releasetime
            prodict['title'] = title
            prodict['detailurl'] = showurl
            prodict['procurement'] = lis['author']
            prodict['detail'],prodict['futher'],prodict['price'] = spider.get_data_detail(href)
                # spider.write_data(file,str(prodict)+"\n")
            mysqldb = serversql()
            rundb(mysqldb, prodict)
            print(prodict)
            # print(detailurl)
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

