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
        detail_list=list()
        res = self.request_(url, method='get')
        # print(res)
        if res:

            data= json.loads(res)
            content=data.get('result').get('data').get('content')
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
        url = f'http://ccgp-bingtuan.gov.cn/portal/category'
        print(url)
        for discode in ['660000','660199','660299','660399','660499','660599','660699','660799','660899','660999','661099','661199','661299','661399','661499']:

            payload = {
                "categoryCode": "ZcyAnnouncement10016",
                "districtCode": [discode],
                "pageNo":page,
                "pageSize":100,
                "_t": int(time.time()*1000)
            }
            data=None
            data_list = self.request_(url,  method='post',data=json.dumps(payload),param=data)
            if data_list:
                # return data_list
                jsondata=json.loads(data_list)
                lis = jsondata.get('result').get('data').get('data')
                for num in range(len(lis)):
                    # releasetime = int(time.mktime(time.strptime(lis['auditTime'], "%Y-%m-%d")))
                    releasetime = int(lis[num]['publishDate']/1000)
                    todaytime = int(time.mktime(time.strptime(times, "%Y-%m-%d")))
                    print(releasetime,todaytime)
                    if releasetime >= todaytime:
                        district=lis[num]['districtName']
                        if "师" in district:
                            districtName = re.findall(r".*师(\w+市)本?级?",district)
                        else:
                            districtName='新疆维吾尔自治区'
                        articleId=lis[num]['articleId']
                        title=lis[num]['title']
                        procurement=lis[num]['author']
                        href=f'http://ccgp-bingtuan.gov.cn/luban/detail?parentId=189169&articleId={articleId}&utm=luban.luban-PC-4840.633-pc-websitegroup-secondlevelpage-front.{num+1}.c25843506b0b11ed8d01831ca74ff0e7'
                        yield districtName,releasetime,articleId,title,href,procurement
                    else:
                        print(f'{discode}{times}获取完毕{page}页')
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
        districtName, releasetime, articleId, title, href, procurement = lis
        prodict = spider.article_field()
        prodict['procurement'] = procurement
        prodict['districtName'] = districtName
        prodict['articleId'] = int(str(int(time.time()*100000+random.random()*200))[-6:])
        prodict['publishDate'] = releasetime
        prodict['title'] = title
        detailurl = f'http://ccgp-bingtuan.gov.cn/portal/detail?articleId={articleId}&timestamp={str(int(time.time()))}'
        prodict['detailurl'] = href
        prodict['detail'] = spider.get_data_detail(detailurl)
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
            main(base['page'], base['time'], base['file'])
    print(time.time() - times)

