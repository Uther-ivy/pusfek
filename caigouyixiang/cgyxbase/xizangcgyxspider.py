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
        time.sleep(5+random.random()*5)
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

    def get_data_detail(self, url):
        print(url)
        detail_list = list()
        res = self.request_(url, method='get')
        if res:
            detail = etree.HTML(res)
            content = etree.tostring(detail.xpath("//div[@class='noticeArea']")[0],method='HTML').decode()
            # size = detail.xpath('//tbody/tr')
            # for num in range(1, len(size) + 1):
            #     detail_dict = {}
            #     proname = detail.xpath(f"//tbody/tr[{num}]/td[2]/text()")
            #     if proname:
            #         proname = proname[0].replace('\u3000', '')
            price = detail.xpath(f"//tr[2]/td[4]/text()")
            if price:
                price = float(price[0].replace(',',''))
            # require = detail.xpath(f"//tbody/tr[{num}]/td[3]/text()")
            # if require:
            #     require = require[0]
            futher = detail.xpath(f"//tr[2]/td[5]/text()")
            if futher:
                futher = futher[0]
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

            return content, futher, price


    def get_data_list(self, times,page):
        url = f'http://www.ccgp-xizang.gov.cn/freecms/rest/v1/notice/selectInfoMoreChannel.do?&siteId=18de62f0-2fb0-4187-a6c1-cd8fcbfb4585&channel=b541ffff-03ee-4160-be64-b11ccf79660d&currPage={page}&pageSize=100&noticeType=59&cityOrArea=&noticeName=&operationStartTime=&operationEndTime=&selectTimeName=noticeTime'
               # 'http://www.ccgp-xizang.gov.cn/freecms/rest/v1/notice/selectInfoMoreChannel.do?&siteId=18de62f0-2fb0-4187-a6c1-cd8fcbfb4585&channel=b541ffff-03ee-4160-be64-b11ccf79660d&currPage=1     &pageSize=100&noticeType=59&cityOrArea=&noticeName=&operationStartTime=&operationEndTime=&selectTimeName=noticeTime'
        print(url)
        payload =None
        data=None
        data_list = self.request_(url,  method='get',data=data,param=payload)
        print(data_list)
        if data_list:
            jsondata=json.loads(data_list)
            for lis in jsondata.get('data'):
                # releasetime = int(time.mktime(time.strptime(lis['auditTime'], "%Y-%m-%d")))
                releasetime = int(lis['addtime']/1000)
                todaytime = int(time.mktime(time.strptime(times, "%Y-%m-%d")))
                print(releasetime,todaytime)
                if releasetime >= todaytime:
                    title=lis['title']
                    articleId=lis['htmlIndexnum']
                    href=lis['pageurl']
                    procurement=''
                    yield releasetime,procurement,articleId,title,href
                else:
                    print(f'{times}获取完毕{page}页')
                    self.err()
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
        releasetime,procurement,articleId,title,href=lis
        # print(lis)
        prodict = spider.article_field()
        # prodict['articleId'] = int(str(time.time()*1000)[::3])
        prodict['articleId'] = articleId
        prodict['publishDate'] = releasetime
        prodict['title'] = title

        prodict['procurement']=procurement
        # detail =spider.get_data_detail(detailurl,detail_info)

        if '县' in title:
            districtName = re.findall('(\w+县).*', title)
            if '市' in districtName:
                districtName = re.findall('市(\w+县)', title)
            else:
                districtName = ['西藏自治区']
        elif '区' in title:
            districtName = re.findall('(\w+区)', title)
            if '市' in districtName:
                districtName = re.findall('市(\w+区)', title)
            else:
                districtName = ['西藏自治区']
        elif '市' in title:
            districtName = re.findall('年?(\w+市).*', title)

        else:
            districtName = ['西藏自治区']
        prodict['procurement'] = procurement
        prodict['districtName'] = districtName
        detailurl = f'http://www.ccgp-xizang.gov.cn{href}'
        prodict['detailurl'] = detailurl
        prodict['detail'], prodict['futher'], prodict['price'] = spider.get_data_detail(detailurl)
        print(prodict)
        # spider.write_data(file,str(prodict)+"\n")
        mysqldb = serversql()
        rundb(mysqldb, prodict)
        print(detailurl)


def main(page, times, file):
    threads = []
    spider = cgyxspider()
    spider.replace_ip()
    for num in range(1,page):
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

