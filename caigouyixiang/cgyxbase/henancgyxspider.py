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
        self._session = requests.session()
        self.proxys = {
            'http': '',
            'https': ''
        }
        self.headers = {

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
            'procurement': '',
            'title': '',
            'detailurl':'',
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
        detail_list = list()
        content=etree.tostring(res.xpath("//td[@class='suojin']/table")[0],method="HTML").decode()
        # for num in range(1,len(detail)+1):
        #     detail_dict = {}
        #     if num>1:
        #
        #         proname = res.xpath(f"//td[@class='suojin']//tr[{num}]/td[3]/text()")
        #         if proname:
        #             proname = proname[0]
        price = res.xpath(f"//td[@class='suojin']//tr[2]/td[5]/text()")
        if price:
            price = price[0].replace(',','')
        # require = res.xpath(f"//td[@class='suojin']//tr[{num}]/td[4]//text()")
        # if require:
        #     require = require[0]
        futher = res.xpath(f"//td[@class='suojin']//tr[2]/td[6]/text()")
        if futher:
            futher = int(time.mktime(time.strptime(futher[0].strip(), "%Y年%m月")))
                # comment = res.xpath(f"//td[@class='suojin']//tr[{num}]/td[7]//text()")
                # if comment:
                #     comment = comment[0]
                # detail_dict['proname'] = proname
                # detail_dict['price'] = price.replace(',','')
                # detail_dict['require'] = require
                # detail_dict['futher'] = futher
                # detail_dict['comment'] = comment
                # detail_list.append(detail_dict)
                # print( proname,price,require,futher,comment)

        return content, futher,price

    # except Exception as e:
    #     logging.error(f"list获取失败{e}\n{traceback.format_exc()}")

    def get_data_info(self, referer,url):
        # print(url,referer)
        self.headers['Referer'] = referer
        time.sleep(1+random.random()*2)
        hrefdata = self.request_(url, method='get')
        # print(hrefdata)
        addr = re.findall(r'\$.get\(\"(.*)\"\, .*\)', hrefdata)
        if addr:
            href ='http://www.ccgp-henan.gov.cn'+addr[0]
            print('ss:',href)
            self.headers['Referer']=href
            res = self.request_(href, method='get')
            return res

    def get_data_list(self, url):

        method = 'get'
        res = self.request_(url, method)

        if res:
            return res

    def write_data(self, file, data):
        with open(file, 'a', encoding='utf-8') as w:
            w.write(data)
            w.close()

    def err(self):
        self.errors = 1


def run(page, spider, times, file):
    for rank in [1, 2]:
        url = f'http://www.ccgp-henan.gov.cn/henan/list2?channelCode=9102&bz={rank}&pageSize=16&gglx=0&gglb=&pageNo={page}'
        data_list = spider.get_data_list(url)
        # print(data_list)
        html = etree.HTML(data_list)
        for data in html.xpath("//div[@class='List2']/ul/li"):
            date = data.xpath("./p/span[@class='Gray Right']/text()")
            if date:
                date = date[0]
            releasetime = int(time.mktime(time.strptime(date, "%Y-%m-%d %H:%M")))
            todaytime = int(time.mktime(time.strptime(times, "%Y-%m-%d")))
            print(releasetime, todaytime)
            #     return lis
            if releasetime >= todaytime:
                prodict = spider.article_field()
                href = data.xpath("./a/@href")[0]
                articleId = re.findall('infoId=(\d+)&', href)[0]
                title = data.xpath("./a/text()")[0]
                districtName = '河南省'
                detailurl = 'http://www.ccgp-henan.gov.cn' + href
                prodict['districtName'] = districtName
                prodict['articleId'] = articleId
                prodict['publishDate'] = releasetime
                prodict['title'] = title
                prodict['detailurl']=detailurl
                content = spider.get_data_info(url,detailurl)
                # print(content)
                if content:
                    detail_data = etree.HTML(content)
                    prodict['procurement'] = detail_data.xpath('//tr[2]/td[2]/text()')[0]
                    prodict['detail'], prodict['futher'], prodict['price'] = spider.get_data_detail(detail_data)
                    # spider.write_data(file, str(prodict) + "\n")
                    mysqldb = serversql()
                    rundb(mysqldb, prodict)
                print(detailurl)
                print(prodict)

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
    # file='../unit.txt'
    file = os.path.basename('../unit.txt')
    with open(file, 'r') as f:
        if os.path.exists(file):
            read = f.readline()
            f.close()
            base = json.loads(read)
            print(base['time'])
            # base['file']='../cgyxdata/henancgyxspider.txt'
            main(base['page'], base['time'], base['file'])
    print(time.time() - times)
