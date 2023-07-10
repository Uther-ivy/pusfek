import html
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
        detail_dict = {}
        print(url)
        res = self.request_(url, method='get')
        # print(res)
        if res:

            detail_data = etree.HTML(res)
            content = etree.tostring(detail_data.xpath("//div[@class='pubtable']")[0],method='HTML').decode()

            # proname = detail_data.xpath('//tr[4]/td[2]//text()')
            # if proname:
            #     proname = proname[0]
            price = detail_data.xpath('//tr[5]/td[2]//text()')
            if price:
                price = price[0].replace("万元(人民币)",'')
            # protype = detail_data.xpath('//tr[6]/td[2]//text()')
            # if protype:
            #     protype = protype[0]
            # require = detail_data.xpath('//tr[7]/td[2]//text()')
            # if require:
            #     require = require[0]
            futher = detail_data.xpath('//tr[8]/td[2]//text()')
            if futher:
                futher = futher[0]
                if '年' in futher:
                    futher = int(time.mktime(time.strptime(futher.strip(), "%Y年%m月")))  #
                else:
                    futher = int(time.mktime(time.strptime(futher.strip(), "%Y-%m")))
            # comment = detail_data.xpath('//tr[9]/td[2]//text()')
            # if comment:
            #     comment = comment[0]
            # detail_dict['proname'] = proname
            # detail_dict['price'] = price
            # detail_dict['protype'] = protype
            # detail_dict['require'] = require
            # detail_dict['futher'] = futher
            # detail_dict['comment'] = comment
            # detail_list.append(detail_dict)

            return content,futher ,price
        # except Exception as e:
        #     logging.error(f"list获取失败{e}\n{traceback.format_exc()}")

    def get_data_info(self, id):
        url = f'http://cgyx.ccgp.gov.cn/cgyx/pub/details?groupId={id}'
        res = self.request_(url,method='get')
        urldata= etree.HTML(res)
        parse_url=urldata.xpath('//tbody/tr/td[5]/a/@href')
        if parse_url:
            return parse_url

    def get_data_list(self, times,page):
        url = f'http://cgyx.ccgp.gov.cn/cgyx/pub/pubSearchData'
        print(url)
        payload = {
            'releaseUnitId': '2c83829e4931cbe801493bc2de23001f',
            'pageSize': 10,
            'pageNo': page}
        data=None
        data_list = self.request_(url,  method='post',data=data,param=payload)
        if data_list:
            jsondata=json.loads(data_list)
            for lis in jsondata.get('rows'):
                releasetime = int(time.mktime(time.strptime(lis['releaseDate'], "%Y-%m-%d %H:%M:%S")))
                # releasetime = int(lis['addtime']/1000)
                todaytime = int(time.mktime(time.strptime(times, "%Y-%m-%d")))
                print(releasetime,todaytime)
                if releasetime >= todaytime:
                    districtName = '中央'
                    articleId = lis['groupId']
                    procurement = lis['releaseUnitName']
                    title = lis['groupName']
                    yield districtName,releasetime,articleId,procurement,title
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
        districtName,releasetime,articleId,procurement,title=lis
        prodict = spider.article_field()
        prodict['procurement'] = procurement
        prodict['districtName'] = districtName
        prodict['articleId'] = int(str(time.time()*1000)[::3])
        prodict['publishDate'] = releasetime
        prodict['title'] = title
        url_list=spider.get_data_info(articleId)
        # print(url_list)
        for href in url_list:
            detailurl = f'http://cgyx.ccgp.gov.cn{href}'
            prodict['detailurl'] = detailurl
            prodict['detail'],prodict['futher'],prodict['price'] = spider.get_data_detail(detailurl)
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

