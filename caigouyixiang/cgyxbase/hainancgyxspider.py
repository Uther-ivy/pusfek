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
            res_data = res.content.decode()
            return res_data

    def request_(self, url, method, data=None, param=None):
        try:
            res = self.req_(url, method, data, param)
        except Exception as e:
            print(e)
            logging.info("proxy disabled！！！ change proxy")
            time.sleep(random.random() * 10)
            self.replace_ip()
            res = self.req_(url, method, data, param)
        return res

    def get_data_info(self, url):
        res = self.request_(url,method='get')
        html=etree.HTML(res)
        infourl = html.xpath(f"//tr[@class='cg20-b1']/td[3]/a/@href")[0]

        return infourl

    def get_data_detail(self, url):
        detail_list=list()
        print(url)
        res = self.request_(url, method='get')
        # print(res)
        detail = etree.HTML(res)
        detail_dict = {}
        text=detail.xpath("//table[1]")
        print(text)
        content =etree.tostring(text[0],method='HTML').decode()
        # if proname:
        #     proname = proname[0].replace('\u3000','')
        price = detail.xpath(f"//tr[5]/td[@class='cg20-bg3']/span/text()")
        if price :
            dor=float(price[0])
            price = round(dor,2)
        # require = detail.xpath(f"//tr[7]/td[@class='cg20-bg3']/span/text()")
        # if require:
        #     require = require[0]
        futher = detail.xpath(f"//tr[8]/td[@class='cg20-bg3']/span/text()")
        if futher:
            futher=futher[0]
            if '年' in futher:
                futher = int(time.mktime(time.strptime(futher.strip(), "%Y年%m月")))  #
            else:
                futher = int(time.mktime(time.strptime(futher.strip(), "%Y-%m")))  #
        # comment = detail.xpath(f"//tr[9]/td[@class='cg20-bg3']//text()")
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
        return content, futher,price
        # except Exception as e:
        #     logging.error(f"list获取失败{e}\n{traceback.format_exc()}")

    def get_data_list(self, times,page):
        url = 'https://www.ccgp-hainan.gov.cn/cgw/cgw_list_cgyx.jsp'
        payload = {'mofdivcode': '',
                   'pageNo': page,
                   'searchword': ''}
        data=None
        data_list = self.request_(url,  method='get',data=data,param=payload)
        html=etree.HTML(data_list)
        all_data=html.xpath("//td[@class='cg20-bgz']")
        for num in range(2, len(all_data) + 1):
            auditTime = html.xpath(f'//tr[{num}]/td[3]/text()')
            releasetime = int(time.mktime(time.strptime(auditTime[0], "%Y-%m-%d %H:%M:%S")))
            # releasetime = int(lis['publishDate']/1000)
            todaytime = int(time.mktime(time.strptime(times, "%Y-%m-%d")))
            print(releasetime, todaytime)
            if releasetime >= todaytime:
                title = html.xpath(f"//tr[{num}]/td[@class='cg20-bgz']/a/text()")[0]
                href = html.xpath(f"//tr[{num}]/td[@class='cg20-bgz']/a/@href")[0]
                articleId = re.findall(r'id=(\d+)&', href)[0]
                procurement = html.xpath(f'//tr[{num}]/td[2]/text()')[0]
                if '县' in procurement:  # if
                    districtName = re.findall('(\w+县).*', procurement)[0]
                    if '市' in districtName:
                        districtName = re.findall('市(\w+县)', districtName[0])
                elif '区' in procurement:
                    districtName = re.findall('(\w+区)', procurement)[0]
                    if '市' in districtName:
                        districtName = re.findall('市(\w+区)', districtName[0])
                elif '市' in procurement:
                    districtName = re.findall('(\w+市).*', procurement)[0]
                else:
                    districtName = '海南省'
                    # print(districtName, releasetime, articleId, procurement, href, title)
                yield districtName, releasetime, articleId, procurement, href, title
            else:
                print(f'{times}获取完毕{page}页')
                self.err()

    def write_data(self,file,data):
        with open(file,'a',encoding='utf-8') as w:
            w.write(data)
            w.close()

    def err(self):
        self.errors=1
def run(page,spider,times,file):

    for lis in spider.get_data_list(times,page):
        districtName,releasetime,articleId,procurement,href,title=lis
        prodict = spider.article_field()
        prodict['procurement'] = procurement
        prodict['districtName'] = districtName
        prodict['articleId'] = articleId
        prodict['publishDate'] = releasetime
        prodict['title'] = title
        domain = f'https://www.ccgp-hainan.gov.cn/cgw/'
        detailurl=domain+spider.get_data_info(domain+href)
        prodict['detailurl'] = detailurl
        prodict['detail'], prodict['futher'], prodict['price'] = spider.get_data_detail(detailurl)
        # spider.write_data(file,str(prodict)+"\n")
        mysqldb = serversql()
        rundb(mysqldb, prodict)
        print(detailurl)
        print(prodict)


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
    # base = {"time": "2022-5-1", "file": "./cgyxdata/hainancgyxspider.txt", "page": 3000}
            main(base['page'], base['time'], base['file'])
    print(time.time() - times)

