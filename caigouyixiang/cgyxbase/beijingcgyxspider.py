import json
import logging
import os
import random
import re
import threading
import time

import requests as requests
from lxml import etree

import ip_proxys
from caigouyixiang.cgyxdata.sql import serversql, rundb


class cgyxspider(object):
    def __init__(self):
        self._session=requests.session()

        self.headers= {

        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36'
    }
        self.errors = 0
        self.proxys = {
            'http': '',
            'https': ''
        }



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
            'detailurl'
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
            detail_dict = {}
            # size=len(res.xpath("//tbody/tr"))
            # for num in range(1,size+1):
            #     if num > 1:
            proname = res.xpath(f"//tr/td[3]/text()")
            if proname:
                proname = proname[0]
            price = res.xpath(f"//tr/td[5]/text()")
            if price :
                price = price[0]
            require = res.xpath(f"//tr/td[4]/text()")
            if require:
                require = require[0]
            futher = res.xpath(f"//tr/td[6]/text()")
            if futher:
                futher = int(time.mktime(time.strptime(futher[0], "%Y-%m")))
            comment = res.xpath(f"//tr/td[7]/text()")
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

    def get_data_info(self, url):

        res = self.request_(url,method='get')
        # print(res)
        return res

    def get_data_list(self,url):
        method='get'
        res = self.request_(url, method)
        # print(res)
        if res:
            return res

    def write_data(self,file,data):
        with open(file,'a',encoding='utf-8') as w:
            w.write(data)
            w.close()

    def err(self):
        self.errors=1
def run(page,spider,times,file):
    # try:
    page=page-1
    for rank in ['qjcgyx','sjcgyx']:
            if page == 0:
                url = f'http://www.ccgp-beijing.gov.cn/cgyx/{rank}/index.html'
            else:
                url = f'http://www.ccgp-beijing.gov.cn/cgyx/{rank}/index_{page}.html'
            data_list = spider.get_data_list(url)
            if data_list:# print(data_list)
                html = etree.HTML(data_list)
                for data in html.xpath("//ul[@class='inner-ul']/li"):
                    date=data.xpath("./span[@class='docRelTime']/text()")
                    if date:
                        date=date[0]
                    releasetime = int(time.mktime(time.strptime(date, "%Y-%m-%d")))
                    todaytime = int(time.mktime(time.strptime(times, "%Y-%m-%d")))
                    print(releasetime,todaytime)
                #     return lis
                    if releasetime >= todaytime:
                        prodict = spider.article_field()
                        href=data.xpath("./a/@href")[0]
                        articleId = re.findall('\\_(\d+).html',href)[0]
                        title=data.xpath("./a/text()")[0]
                        if 'qjcgyx' in rank:
                            districtName = re.findall('\\[(\w+)\\].*',title)[0]+'区'
                        else:
                            districtName ='北京市'
                        prodict['districtName'] = districtName
                        prodict['articleId'] = articleId
                        prodict['publishDate'] = releasetime
                        prodict['title'] = title.strip()
                        detailurl=href.replace('./',f'http://www.ccgp-beijing.gov.cn/cgyx/{rank}/')
                        content = spider.get_data_info(detailurl)
                        prodict['detailurl']=detailurl
                        if content:
                            detail_data = etree.HTML(content)
                            proc=detail_data.xpath("//tr/td[2]/text()")
                            if proc:
                                proc=proc[0]
                            prodict['procurement'] =proc
                            prodict['detail'] = spider.get_data_detail(detail_data)
                            mysqldb = serversql()
                            rundb(mysqldb,prodict)
                            # spider.write_data(file,str(prodict)+"\n")
                            print(detailurl)
                            print(prodict)
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

