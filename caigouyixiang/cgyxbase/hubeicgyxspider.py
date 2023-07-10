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

        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36'
    }
        self.errors = 0

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
            'deftailurl':'',
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

    def get_data_detail(self, res):
            detail_list=list()
            content=etree.tostring(res.xpath("//div[@class='art_con']/div[2]")[0],method="HTML").decode()
            # size=len(res.xpath("//tbody/tr"))
            # for num in range(2,size+1):
            #     detail_dict = {}
            #     if num > 1:
            #         proname = res.xpath(f"//tr[{num}]/td[2]/p/text()")
            #         if proname:
            #             proname = proname[0]
            price = res.xpath(f"//tr[2]/td[4]/p/text()")
            if price :
                        price = price[0]
                    # require = res.xpath(f"//tr[{num}]/td[3]/p/text()")
                    # if require:
                    #     require = require[0]
            futher = res.xpath(f"//tr[2]/td[5]/p/text()")
            if futher:
                        futher = int(time.mktime(time.strptime(futher[0], "%Y-%m")))
                    # comment = res.xpath(f"//tr[{num}]/td[6]/p/text()")
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
        # except Exception as e:
        #     logging.error(f"list获取失败{e}\n{traceback.format_exc()}")

    def get_data_info(self, url):
        # id='1467440'
        # url = f'http://www.ccgp-henan.gov.cn/webfile/zhumadian/cgxx/cgyx/webinfo{id}.htm'
        # print(url)
        # self.headers['Referer']=heard
        res = self.request_(url,method='get')
        return res

    def get_data_list(self,url):

        method='get'
        res = self.request_(url, method)
        if res:
            # print(res)
            return res

    def write_data(self,file,data):
        with open(file,'a',encoding='utf-8') as w:
            w.write(data)
            w.close()

    def err(self):
        self.errors=1
def run(page,spider,times,file):
    # try:

    for rank in ['sjcgyxgg','sxcgyxgg']:
            url = f'http://www.ccgp-hubei.gov.cn/notice/cgyxgg/{rank}/index_{page}.html'
            data_list = spider.get_data_list(url)
            # print(data_list)
            html=etree.HTML(data_list)
            for data in html.xpath("//ul[@class='news-list-content list-unstyled margin-top-20']/li"):
                date=data.xpath("./span/text()")
                if date:
                    date=date[0]
                releasetime = int(time.mktime(time.strptime(date, "%Y-%m-%d")))
                todaytime = int(time.mktime(time.strptime(times, "%Y-%m-%d")))
                print(releasetime,todaytime)
            #     return lis
                if releasetime >= todaytime:
                    prodict = spider.article_field()
                    href=data.xpath("./a/@href")[0]
                    # articleId=int(str(int(time.time()*100000+random.random()*200))[-6:])
                    title=data.xpath("./a/text()")[0].replace('中共','')
                    if rank == 'sjcgyxgg':
                        districtName = ['湖北省']
                    else:
                        if '县' in title:  # if
                            districtName = re.findall('(\w+县).*', title)
                            if '市' in districtName[0]:
                                districtName = re.findall('市(\w+县)', districtName[0])
                        elif '区' in title:
                            districtName = re.findall('(\w+区)', title)
                            if '市' in districtName[0]:
                                districtName = re.findall('市(\w+区)', districtName[0])
                        elif '市' in title:
                            districtName = re.findall('(\w+市).*', title)
                        else:
                            districtName = ['湖北省']

                    prodict['districtName'] = districtName[0]
                    prodict['articleId'] =int(str(int(time.time()*100000+random.random()*200))[-6:])
                    prodict['publishDate'] = releasetime
                    prodict['title'] = title.strip()
                    # re_num=re.findall('(\d{4}-\d{2})-\d+',date)[0]
                    # id='/'+re_num.replace('-','/')+'/'+articleId
                    detailurl='http://www.ccgp-hubei.gov.cn'+href
                    print(detailurl)
                    prodict['detailurl']=detailurl
                    content = spider.get_data_info(detailurl)
                    if content:
                        detail_data = etree.HTML(content)

                        proc=detail_data.xpath("//div[1]/div/span[2]/text()")[0]
                        print(proc)
                        prodict['procurement'] =re.findall('发布单位[：:]\s?(\S+)',proc)[0]
                        prodict['detail'],prodict['futher'],prodict['price'] = spider.get_data_detail(detail_data)
                        mysqldb = serversql()
                        rundb(mysqldb, prodict)
                    print(detailurl)
                    print(prodict)
                        # print(prodict)
                        # exit()
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
    # file='E:\\surface\\Desktop\\python_code\\pusfek\\caigouyixiang\\unit.txt'
    file = os.path.basename('../unit.txt')
    with open(file, 'r') as f:
        if os.path.exists(file):
            read = f.readline()
            f.close()
            base = json.loads(read)
            print(base['time'])
            main(base['page'], base['time'], base['file'])
    print(time.time() - times)

