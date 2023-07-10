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
from cgyxdata.sql import serversql, rundb


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
        detail_list=list()
        res = self.request_(url, method='get')
        if res:
            detail = etree.HTML(res)
            text = detail.xpath("//div[@class='noticeArea']")
            content = etree.tostring(text[0], method='HTML').decode()
            # size = detail.xpath("//div[@id='electronicStoreInfo']//tr")
            # print(size)
            # for num in range(2, len(size) + 1):
            #     detail_dict = {}
            #     proname = detail.xpath(f"//div[@id='electronicStoreInfo']//tr[{num}]/td[2]/text()")
            #     if proname:
            #         proname = proname[0].replace('\u3000', '')
            #     require = detail.xpath(f"//div[@id='electronicStoreInfo']//tr[{num}]/td[3]/div")
            #     if require:
            #         content = ''
            #         for text in require:
            #             content += text.xpath('./text()')[0].strip()
            #         require = content

            price = detail.xpath(f"//div[@id='electronicStoreInfo']//tr[2]/td[5]/text()")
            if price:
                price = float(price[0].replace(',', '')) / 10000
            futher = detail.xpath(f"//div[@id='electronicStoreInfo']//tr[2]/td[6]/text()")
            if futher:
                futher = futher[0]
                if '年' in futher:
                    futher = int(time.mktime(time.strptime(futher.strip(), "%Y年%m月")))  #
                else:
                    futher = int(time.mktime(time.strptime(futher.strip(), "%Y-%m")))  #
                # comment = detail.xpath(f"//div[@id='electronicStoreInfo']//tr[{num}]/td[7]/text()")
                # if comment:
                #     comment = comment[0]
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
        if page ==1:
            urls = ['https://gdgpo.czt.gd.gov.cn/freecms/rest/v1/notice/selectInfoForIndex.do?&siteId=cd64e06a-21a7-4620-aebc-0576bab7e07a&channel=fca71be5-fc0c-45db-96af-f513e9abda9d&currPage=1&pageSize=10&noticeType=59&regionCode=!440001&cityOrArea=3&sfTotal=false&selectType=',
                    'https://gdgpo.czt.gd.gov.cn/freecms/rest/v1/notice/selectInfoForIndex.do?&siteId=cd64e06a-21a7-4620-aebc-0576bab7e07a&channel=fca71be5-fc0c-45db-96af-f513e9abda9d&currPage=1&pageSize=10&noticeType=59&regionCode=!440001&cityOrArea=&sfTotal=false&selectType=' ,
                    'https://gdgpo.czt.gd.gov.cn/freecms/rest/v1/notice/selectInfoForIndex.do?&siteId=cd64e06a-21a7-4620-aebc-0576bab7e07a&channel=fca71be5-fc0c-45db-96af-f513e9abda9d&currPage=1&pageSize=10&noticeType=59&regionCode=440001&cityOrArea=&sfTotal=false&selectType=redis']
            payload =None
            data=None
            for url in urls:
                print(url)
                data_list = self.request_(url,  method='get',data=data,param=payload)
                jsondata=json.loads(data_list)
                for lis in jsondata.get('data'):
                    # releasetime = int(time.mktime(time.strptime(lis['noticeTime'], "%Y-%m-%d %H:%M:%S")))
                    releasetime = int(lis['addtime']/1000)
                    todaytime = int(time.mktime(time.strptime(times, "%Y-%m-%d")))
                    print(releasetime,todaytime)
                    if releasetime >= todaytime:
                        districtName = lis['regionName'].replace('本级','')
                        articleId=lis['id']
                        procurement=lis['agency']
                        title=lis['shorttitle']
                        href=lis['pageurl']
                        yield districtName,releasetime,articleId,procurement,title,href
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
        districtName,releasetime,articleId,procurement,title,href=lis
        prodict = spider.article_field()
        prodict['procurement'] = procurement
        prodict['districtName'] = districtName
        prodict['articleId'] = int(str(int(time.time() * 100000 + random.random() * 200))[-6:])
        prodict['publishDate'] = releasetime
        prodict['title'] = title
        detailurl = f'https://gdgpo.czt.gd.gov.cn{href}?singleIntention=singleIntentionFlag'
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
    # spider.replace_ip()
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

