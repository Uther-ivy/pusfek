import json
import logging
import os
import random
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
            'http': "",
            'https':""
        }
        self.headers= {

        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36'
    }
        self.errors=0

    def replace_ip(self):
        proxy=ip_proxys.replace_ip()
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

    def get_cookie(self):
        # url = 'http://www.ccgp-anhui.gov.cn/CSPDREL1pjeUFubm91bmNlbWVudC9aY3lBbm5vdW5jZW1lbnQxL2luZGV4Lmh0bWw=?wzwscspd=MC4wLjAuMA=='
        url = 'http://www.ccgp-anhui.gov.cn/CSPDREL1pjeUFubm91bmNlbWVudC9aY3lBbm5vdW5jZW1lbnQxL1pjeUFubm91bmNlbWVudDEwMDE2L3BTYjFhSHpicmtrNzJiS251WVZta1E9PS5odG1s?wzwscspd=MC4wLjAuMA=='
        proxy = self.proxys
        self._session.get(url,proxies=proxy,verify=False)
        cookies = requests.utils.dict_from_cookiejar(self._session.cookies)
        cookie = f"wzws_sid={cookies['wzws_sid']}"
        # 'wzws_sessionid={cookies['wzws_sessionid']}; wzws_sid={cookies['wzws_sid']}; '
        # 'wzws_sessionid=gTU1OWRhM4AxMDYuMTEzLjY1Ljg5gjQ2NTdiYaBjnCjw; ' \
        # 'wzws_cid=74a5593ccc12335e11424a702afd92edc3a6eaf0606d3fe25b17d8ffb4ceee5f79a7c827a629d5bf5cebc19ecf040933ba0a22f2a5304cebecc79435aa3255b2f94d61422eceb35297bef56adb67281b; ' \
        # 'wzws_sid=617bc1736cb249ca994df5b6d7855e614de3a7a3a43243b6eab95bc004977249b903630188f1bac6b4c99e74c28f018fb3a921386c46f1a238ac4f08691e998c9505528234cbe8ef3c4a7c501ef8d1fa1e9b31e70c5faf017e3a02a33f267e38'
        print(cookie)
        return cookie

    def get_data_detail(self, url):
        if self.headers.get('Content-Type'):
            self.headers.pop('Content-Type')
        # self.headers['Cookie'] =cookie
        detail_list=list()
        res = self.request_(url, method='get')
        print('ssss',res)
        if res:
            data= json.loads(res)['result']['data']
            content=data.get('content')
            # print(content)
            detail = etree.HTML(content)
            size= detail.xpath("//tbody/tr")
            for num in range(1,len(size)+1):
                detail_dict = {}
                proname = detail.xpath(f"//tr[{num}]/td[@class='code-purchaseProjectName']/text()")
                if proname:
                    proname = proname[0].replace('\u3000','')
                require = detail.xpath(f"//tr[{num}]/td[@class='code-purchaseRequirementDetail']/text()")
                if require:
                    require = require[0]
                price = detail.xpath(f"//tr[{num}]/td[@class='code-budgetPrice']/text()")
                if price :
                    price =float(price[0])/10000
                futher = detail.xpath(f"//tr[{num}]/td[@class='code-estimatedPurchaseTime']/text()")
                if futher:
                    futher=futher[0]
                    if '年' in futher:
                        futher = int(time.mktime(time.strptime(futher.strip(), "%Y年%m月")))  #
                    else:
                        futher = int(time.mktime(time.strptime(futher.strip(), "%Y-%m")))  #
                comment = detail.xpath(f"//tr[{num}]/td[@class='code-remark']/text()")
                if comment:
                    comment = comment[0]
                detail_dict['proname'] = proname
                detail_dict['price'] = price
                detail_dict['require'] = require
                detail_dict['futher'] = futher
                detail_dict['comment'] = comment
                detail_list.append(detail_dict)
                # print( proname,price,require,futher,comment)
            return detail_list
    def get_data_detail_xpath(self, url):
        if self.headers.get('Content-Type'):
            self.headers.pop('Content-Type')
        # self.headers['Cookie'] =cookie
        detail_list=list()
        res = self.request_(url, method='get')
        # print('ssss',res)
        if res:
            html = etree.HTML(res)
            jsdata=html.xpath("//input[@name='articleDetail']/@value")
            data= json.loads(jsdata[0])
            content=data.get('content')
            # print(content)
            detail = etree.HTML(content)
            size= detail.xpath("//tbody/tr")
            for num in range(1,len(size)+1):
                detail_dict = {}
                proname = detail.xpath(f"//tr[{num}]/td[@class='code-purchaseProjectName']/text()")
                if proname:
                    proname = proname[0].replace('\u3000','')
                require = detail.xpath(f"//tr[{num}]/td[@class='code-purchaseRequirementDetail']/text()")
                if require:
                    require = require[0]
                price = detail.xpath(f"//tr[{num}]/td[@class='code-budgetPrice']/text()")
                if price :
                    price =float(price[0])/10000
                futher = detail.xpath(f"//tr[{num}]/td[@class='code-estimatedPurchaseTime']/text()")
                if futher:
                    futher=futher[0]
                    if '年' in futher:
                        futher = int(time.mktime(time.strptime(futher.strip(), "%Y年%m月")))  #
                    else:
                        futher = int(time.mktime(time.strptime(futher.strip(), "%Y-%m")))  #
                comment = detail.xpath(f"//tr[{num}]/td[@class='code-remark']/text()")
                if comment:
                    comment = comment[0]
                detail_dict['proname'] = proname
                detail_dict['price'] = price
                detail_dict['require'] = require
                detail_dict['futher'] = futher
                detail_dict['comment'] = comment
                detail_list.append(detail_dict)
                # print( proname,price,require,futher,comment)
            return detail_list
        # except Exception as e:
        #     logging.error(f"list获取失败{e}\n{traceback.format_exc()}")



    def get_data_list(self, times,page):
        url = f'http://www.ccgp-anhui.gov.cn/portal/category'
        print(url)
        payload = '{"pageNo":'+str(page)+',"pageSize":15,"categoryCode":"ZcyAnnouncement10016","districtCode":null,"leaf":null,"_t":'+str(int(time.time())*1000)+'}'
        data=None
        self.headers['Content-Type']= 'application/json;charset=UTF-8'
        data_list = self.request_(url,  method='post',data=payload,param=data)
        print(self._session.cookies)
        print(data_list)
        # time.sleep(2222)
        if data_list:
            # return data_list
            jsondata=json.loads(data_list)
            for lis in jsondata.get('result').get('data').get('data'):
                # lis=data.
                # releasetime = int(time.mktime(time.strptime(lis['auditTime'], "%Y-%m-%d")))
                releasetime = int(lis['publishDate']/1000)
                todaytime = int(time.mktime(time.strptime(times, "%Y-%m-%d")))
                print(releasetime,todaytime)
                if releasetime >= todaytime:
                    districtName = lis['districtName'].replace('本级','')
                    articleId=lis['articleId']
                    title=lis['title']
                    href=f'http://www.ccgp-anhui.gov.cn/portal/detail?articleId={articleId}&timestamp={int(time.time())}'
                    procurement=lis['author']

                    yield districtName,releasetime,articleId,title,href,procurement
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
        # cookie=spider.get_cookie()
        districtName, releasetime, articleId, title, href, procurement = lis
        prodict = spider.article_field()
        prodict['procurement'] = procurement
        prodict['districtName'] = districtName
        prodict['articleId'] = int(str(int(time.time()*100000+random.random()*200))[-6:])
        prodict['publishDate'] = releasetime
        prodict['title'] = title
        detailurl = f'http://www.ccgp-anhui.gov.cn/luban/detail?parentId=541080&articleId=LmYvnjdtHaQJguU1Vi99eA==&utm=luban.luban-PC-4720.878-pc-websitegroup-anhuisecondLevelPage-front.16.efb164f0ebe211ed977cab0b3cbfc657'
        detailurl = f'http://www.ccgp-anhui.gov.cn/luban/detail?parentId=541080&articleId=2WJZZKUSMkGsaJwS5z6ihw==&utm=luban.luban-PC-4720.878-pc-websitegroup-anhuisecondLevelPage-front.21.efb164f0ebe211ed977cab0b3cbfc657'
        print(detailurl)
        prodict['detailurl'] = detailurl
        prodict['detail'] = spider.get_data_detail(href)
        # spider.write_data(file,str(prodict)+"\n")
        mysqldb = serversql()
        rundb(mysqldb, prodict)
        print(prodict)


def main(page, times, file):
    threads = []
    spider = cgyxspider()
    # spider.replace_ip()
    for num in range(1, page):
        # print(num)
        if spider.errors == 1:
            break
        t = threading.Thread(target=run, args=(num,), kwargs={'spider': spider, 'times': times, 'file': file})
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

