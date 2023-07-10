import datetime
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
from cgyxdata.sql import serversql, rundb


class cgyxspider(object):

    def __init__(self):

        self._session=requests.session()
        self.proxys = {
            'http': '',
            'https': ''
        }
        self.headers= {
'Accept':'application/json, text/plain, */*',
# 'Accept-Encoding':'gzip, deflate',
# 'Accept-Language':'zh-CN,zh;q=0.9',
# 'Connection':'keep-alive',
# 'Content-Length':'79',
'Content-Type':'application/json;charset=UTF-8',
# 'Cookie':'ASP.NET_SessionId=fyt0kf451vsllv4544cbtmii',
'Host':'www.ccgp-dalian.gov.cn',
# 'Origin':'http://www.ccgp-dalian.gov.cn',
# 'Referer':'http://www.ccgp-dalian.gov.cn/luban/category?parentId=55812&childrenCode=ZcyAnnouncement1',
'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36',
# 'X-Requested-With':'XMLHttpRequest',
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
        # prox = self.proxys
        time.sleep(5+random.random()*5)
        if method == 'get':
            res = self._session.get(url=url, headers=self.headers,  verify=False,
                                    timeout=60)
        else:
            res = self._session.post(url=url, headers=self.headers, data=data, params=param,  verify=False,
                                     timeout=60)
        if res.status_code == requests.codes.ok:
            res_data = res.text
            return res_data

    def request_(self, url, method, data=None, param=None):
        try:
            res = self.req_(url, method, data, param)
        except Exception as e:
            print(e)
            logging.info("proxy disabled！！！ change proxy")
            time.sleep(random.random() * 10)
            # self.replace_ip()
            res = self.req_(url, method, data, param)
        return res

    def get_data_detail(self, url):
        detail_list=list()
        print(url)
        res = self.request_(url, method='get')
        print(res)
        if res:
            content=json.loads(res).get('result').get('data').get('content')
            detail = etree.HTML(content)
            # size= detail.xpath("//table[@id='_Sheet1_7_0']//tr")
            # for num in range(3,len(size)+1):
            #     detail_dict = {}
            #     proname = detail.xpath(f"//table[@id='_Sheet1_7_0']//tr[{num}]/td[2]/text()")
            #     if proname:
            #         proname = proname[0].replace('\u3000','')
            price = detail.xpath(f"//td[@class='code-budgetPrice']/text()")[0].replace('\xa0','')
            if price :
                price =price
            else:
                price=0
            #     require = detail.xpath(f"//table[@id='_Sheet1_7_0']//tr[{num}]/td[3]/text()")
            #     if require:
            #         content=''
            #         for text in require:
            #             content+=text
            #         require = content
            futher = detail.xpath(f"//td[@class='code-estimatedPurchaseTime']/text()")
            if futher:
                futher=futher[0].replace('\xa0','')
                if '年' in futher:
                    futher = int(time.mktime(time.strptime(futher.strip(), "%Y年%m月")))  #
                else:
                    futher = int(time.mktime(time.strptime(futher.strip(), "%Y-%m")))  #
            #     comment = detail.xpath(f"/table[@id='_Sheet1_7_0']//tr[{num}]/td[6]/text()")
            #     if comment:
            #         comment = comment[0]
            #
            #     detail_dict['proname'] = proname
            #     detail_dict['price'] = price
            #     detail_dict['protype'] =
                # detail_dict['require'] = require
                # detail_dict['futher'] = futher
                # detail_dict['comment'] = comment
                # detail_list.append(detail_dict)
                # print( proname,price,require,futher,comment)
            return content, futher,price
        # except Exception as e:
        #     logging.error(f"list获取失败{e}\n{traceback.format_exc()}")



    def get_data_list(self, times,page):
        print(page)
        url='http://www.ccgp-dalian.gov.cn/portal/category'
        # print(url)
        payload = None
        data={"pageNo":page,"pageSize":15,"categoryCode":"ZcyAnnouncement2","_t":int(time.time()*1000)}
        data_list = self.request_(url,  method='post',data=json.dumps(data),param=payload)
        # print(data_list)
        if data_list:
            for data in json.loads(data_list).get('result').get('data').get('data'):
                # print(type(data),data)
                # auditTime = int(data.get('publishDate')[:11])
                # year=datetime.datetime.today().year
                # date=f'{year}-{auditTime[0]}'
                # releasetime = int(time.mktime(time.strptime(auditTime[:11], "%Y-%m-%d")))
                releasetime = int(data.get('publishDate'))/1000
                # releasetime = int(lis['publishDate']/1000)
                todaytime = int(time.mktime(time.strptime(times, "%Y-%m-%d")))
                print(releasetime, todaytime)
                if releasetime >= todaytime:
                    title = data.get('title')
                    article=data.get('articleId')
                    href = f'http://www.ccgp-dalian.gov.cn/luban/detail?parentId=55812&articleId={article}'
                    # articleId = int(str(time.time()*1000)[::3])
                    # articleId = re.findall(r'Id=(\d+)', href)[0]
                    procurement =''# re.findall(r'\】(\w+)\d{4}',title)[0]
                    districtName='大连市'
                    # print(districtName, releasetime, procurement, href, title)
                    yield districtName, article,releasetime,  procurement, href, title
                else:
                    print(f'{times}获取完毕{page}页')
                    self.err()
        else:
            print(f'{times}获取完毕{page}页')
            self.err()

    def get_data_list2(self, times,page):
        if page==1:
            url='http://www.ccgp-dalian.gov.cn/dlweb/'
            print(url)
            payload = None
            data=None
            data_list = self.request_(url,  method='get',data=data,param=payload)
            # print(data_list)
            html=etree.HTML(data_list)
            all_data = html.xpath("//div[@id='menutab_3_5']//tr[@class='trstyle']/td[3]")
            for num in range(1, len(all_data) + 1 , 2):
                auditTime = html.xpath(f"//div[@id='menutab_3_5']//tr[{num}]/td[3]/font/text()")
                # year=datetime.datetime.today().year
                # date=f'{year}-{auditTime[0]}'
                releasetime = int(time.mktime(time.strptime(auditTime[0], "%Y-%m-%d")))
                # releasetime = int(lis['publishDate']/1000)
                todaytime = int(time.mktime(time.strptime(times, "%Y-%m-%d")))
                print(releasetime, todaytime)
                if releasetime >= todaytime:
                    title = html.xpath(f"//div[@id='menutab_3_5']//tr[@class='trstyle'][{num}]/td[2]/a/text()")[0]
                    href = html.xpath(f"//div[@id='menutab_3_5']//tr[@class='trstyle'][{num}]/td[2]/a/@href")[0]
                    # articleId = int(str(time.time()*1000)[::3])
                    # articleId = re.findall(r'Id=(\d+)', href)[0]
                    procurement = re.findall(r'\】(\w+)\(?\（?本?级?\)?\）?\d{4}',title)[0]
                    districtName='大连市'
                        # print(districtName, releasetime, articleId, procurement, href, title)
                    yield districtName, releasetime,  procurement, href, title
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
    for lis in spider.get_data_list(times, page):
            districtName,article, releasetime, procurement, href, title = lis
            # print(lis)
            prodict = spider.article_field()
            prodict['procurement'] = procurement
            prodict['districtName'] = districtName
            prodict['articleId'] = int(str(int(time.time() * 100000 + random.random() * 200))[-6:])
            prodict['publishDate'] = releasetime
            prodict['title'] = title
            showurl = f'http://www.ccgp-dalian.gov.cn/luban/detail?parentId=55812&articleId={article}'
            detailurl=f'http://www.ccgp-dalian.gov.cn/portal/detail?articleId={urllib.parse.quote(article)}&timestamp={int(float(time.time()))}'
            prodict['detailurl'] = showurl
            prodict['detail'], prodict['futher'], prodict['price'] = spider.get_data_detail(detailurl)
            print(prodict)
            # spider.write_data(file,str(prodict)+"\n")
            mysqldb = serversql()
            rundb(mysqldb, prodict)
            # print(detailurl)

def main(page, times, file):
    threads = []
    spider = cgyxspider()
    spider.replace_ip()
    for num in range(1, page):
        # print(num)
        if spider.errors == 1:
            break
        t = threading.Thread(target=run, args=(num,spider,times,file))
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

