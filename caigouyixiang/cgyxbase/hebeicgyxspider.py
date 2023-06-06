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
        print(url)
        res = self.request_(url, method='get')
        try:
            if res:
                detail = etree.HTML(res)
                data= detail.xpath("//span[@id='intentionAnncInfos']/text()")
                if len(data) >= 2:
                    text = ''
                    for sd in data:
                        text += sd.replace('\n', '')
                    data=text
                else:
                    data=data[0]
                detailarray = data.split('#_@_@')
                detaillist = detailarray[0].split('#_#')
                for num in range(len(detaillist)):
                    detail_dict = {}
                    proname = detailarray[1]
                    if proname:
                        proname=proname.split('#_#')[num]
                    require = detailarray[2]
                    if require:
                        require= require.split('#_#')[num]
                    price = detailarray[3]
                    if price:
                        price=price.split('#_#')[num]
                        price =float(price)/10000
                    futher = detailarray[4]
                    if futher:
                        futher= futher.split('#_#')[num]
                        if '年' in futher:
                            futher = int(time.mktime(time.strptime(futher.strip(), "%Y年%m月")))  #
                        else:
                            futher = int(time.mktime(time.strptime(futher.strip(), "%Y-%m")))
                    comment = detailarray[5]
                    if comment:
                        comment= comment.split('#_#')[num]
                    # print(proname, price, require, futher, comment)
                    detail_dict['proname'] = proname
                    detail_dict['price'] = price
                    # detail_dict['protype'] =
                    detail_dict['require'] = require
                    detail_dict['futher'] = futher
                    detail_dict['comment'] = comment
                    detail_list.append(detail_dict)
                    # print( proname,price,require,futher,comment)
                return detail_list
        except Exception as e:
            logging.error(f"detail获取失败{e}\n{traceback.format_exc()}\n{url}")



    def get_data_list(self, times,page):
        params=['index.html','index_1047.html']
        params1=[f'index_{page}.html',f'index_1047_{page}.html']
        for size in range(len(params)):
            if page >= 1:
                 url= f'http://www.ccgp-hebei.gov.cn/province/zfcgyxgg/zfcgyx/{params1[size]}'
            else:
                url = f'http://www.ccgp-hebei.gov.cn/province/zfcgyxgg/zfcgyx/{params[size]}'
            print(url)
            payload = None
            data=None
            data_list = self.request_(url,  method='get',data=data,param=payload)
            if data_list:
                # return data_list
                html=etree.HTML(data_list)
                all_data = html.xpath("//tr/td[2]/a[@class='a3']")
                for num in range(1, len(all_data) + 1, 2):
                    auditTime = html.xpath(f"//tr[{num+1}]//td[@class='txt1']/span[1]/text()")
                    releasetime = int(time.mktime(time.strptime(auditTime[0].strip(), "%Y-%m-%d")))
                    # releasetime = int(lis['publishDate']/1000)
                    todaytime = int(time.mktime(time.strptime(times, "%Y-%m-%d")))
                    print(releasetime, todaytime)
                    if releasetime >= todaytime:
                        title = html.xpath(f"//tr[{num}]/td[2]/a[@class='a3']/text()")[0]
                        href = html.xpath(f"//tr[{num}]/td[2]/a[@class='a3']/@href")[0]
                        if size ==0:
                            href =href.replace('./','http://www.ccgp-hebei.gov.cn/province/zfcgyxgg/zfcgyx/')
                        else:
                            href= href.replace('../../../','http://www.ccgp-hebei.gov.cn/')
                        # articleId = re.findall(r'id=(\d+)', href)[0]
                        procurement = html.xpath(f"//tr[{num+1}]/td[@class='txt1']/span[2]/text()")[0]
                        if '县' in procurement:  # if
                            districtName = re.findall('(\w+县).*', procurement)[0]
                            if '市' in districtName:
                                districtName = re.findall('市(\w+县)', districtName)[0]
                        elif '区' in procurement:
                            districtName = re.findall('(\w+区)', procurement)[0]
                            if '市' in districtName:
                                districtName = re.findall('市(\w+区)', districtName)[0]
                        elif '市' in procurement:
                            districtName = re.findall('(\w+市).*', procurement)[0]
                        else:
                            districtName = '河北省'
                            # print(districtName, releasetime, articleId, procurement, href, title)
                        yield districtName, releasetime, procurement, href, title
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
        districtName,releasetime,procurement,href,title=lis
        prodict = spider.article_field()
        prodict['procurement'] = procurement
        prodict['districtName'] = districtName
        prodict['articleId'] = int(str(int(time.time()*100000+random.random()*200))[-6:])
        prodict['publishDate'] = releasetime
        prodict['title'] = title
        detailurl = href
        prodict['detailurl'] = detailurl
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
    for num in range(0, page):
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

