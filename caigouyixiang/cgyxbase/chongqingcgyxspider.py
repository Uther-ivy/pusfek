import json
import logging
import os.path
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
            # detail_data =
            for detail in res:
                detail_dict = {}
                proname = detail.get('title')
                price = detail.get('money')
                require = detail.get('depict')
                futher = detail.get('expectTime')
                if futher:
                    futher=futher/1000
                comment = detail.get('remarks')
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

    def get_data_info(self, url):
        # id='1467440'

        res = self.request_(url,method='get')
        return res

    def get_data_list(self, page):
        url = 'https://www.ccgp-chongqing.gov.cn/yw-gateway/demand/demand/front?'
        print(page)
        payload = {
            'type':2,
            'page':page,
            # 'TimeEnd':1667750400000,
            'pageSize':10
           }
        method='get'
        res = self.request_(url, method,param=payload)
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
            for lis in data_list['data']:
                # lis=data['_source']
                # releasetime = int(time.mktime(time.strptime(lis['publishDate'], "%Y-%m-%d %H:%M:%S")))
                releasetime = int(lis['createTime'])/1000
                todaytime = int(time.mktime(time.strptime(times, "%Y-%m-%d")))
                if releasetime >= todaytime:
                    prodict = spider.article_field()
                    title=lis['title']
                    procurement=lis['createOrgName']
                    districtName = lis['createRegionName']
                    articleId=lis['id']
                    publishDate=releasetime
                    prodict['procurement'] = procurement
                    prodict['districtName'] = districtName
                    prodict['articleId'] =int(str(int(time.time()*100000+random.random()*200))[-6:])
                    prodict['publishDate'] = publishDate
                    prodict['title'] = title
                    # print(lis)
                    detailurl = f'https://www.ccgp-chongqing.gov.cn/yw-gateway/demand/demand/{articleId}/front'
                    prodict['detailurl']=detailurl
                    content = spider.get_data_info(detailurl)
                    if content:
                        html=json.loads(content).get('data').get('intentionDetaileList')
                        # detail_url = 'http://cgyx.ccgp.gov.cn/' + parse_data.xpath('//tbody/tr/td[5]/a/@href')[0]
                        prodict['detail'] = spider.get_data_detail(html)
                        mysqldb = serversql()
                        rundb(mysqldb, prodict)
                        # spider.write_data(file,str(prodict)+"\n")
                        print(detailurl)
                        print(prodict)


                #
                else:
                    print(f'{times}今日获取完毕{page}页')
                    spider.err()

                # return prodict
    # except Exception as e:
    #         logging.error(f"list获取失败{e}\n{traceback.format_exc()}")
    #         prodict
            # yield prodict

def main (page,times,file):
    threads = []
    spider = cgyxspider()
    spider.replace_ip()
    for num in range(1, page):
        if spider.errors == 1:
            print(spider.errors)
            break
        t = threading.Thread(target=run, args=(num,), kwargs={'spider': spider, 'times': times, 'file': file})
        time.sleep(5 + random.random() * 5)
        threads.append(t)
        t.start()
    for thread in threads:
        thread.join()


if __name__ == '__main__':
    times = time.time()
    file = os.path.basename('../unit.txt')
    with open(file,'r')as f:
        if os.path.exists(file):
            read=f.readline()
            f.close()
            base=json.loads(read)
            print(base['time'])
            main(base['page'],base['time'],base['file'])
    print(time.time()-times)
