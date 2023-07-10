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
from datetime import date

import requests as requests
from lxml import etree

import ip_proxys
from cgyxdata.sql import serversql, rundb


class cgyxspider(object):
    def __init__(self):
        self._session=requests.session()
        self.cookie=''
        self.proxys = {
            'http': '',
            'https': ''
        }
        self.headers= {
'Accept':'*/*',
# 'Accept-Encoding':'gzip, deflate',
# 'Accept-Language':'zh-CN,zh;q=0.9',
# 'Connection':'keep-alive',
# 'Content-Length':'73',
'Content-Type':'application/x-www-form-urlencoded; charset=UTF-8',
# 'Cookie':'HttpOnly; HttpOnly; JSESSIONID=IdAt5sbbSBM6w9o0kVDI08tm08Z0BuOzwi3TdteQf1VfUMhbQj_V!2022974124; TOPAPP_COOKIE=040440402700401d',
# 'Cookie':'HttpOnly; HttpOnly; JSESSIONID=Cpk0o75PeR1DhUkXUUUQIi4kYrfQRIDTdVWwB5Hj4jGTuzaKHr6z!2022974124; TOPAPP_COOKIE=040440402700401d',

# 'Host':'www.ccgp-tianjin.gov.cn',
# 'Origin':'http://www.ccgp-tianjin.gov.cn',
'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36',
'X-Requested-With':'XMLHttpRequest',

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
        # time.sleep(random.random()*10)
        if method == 'get':
            res = self._session.get(url=url, headers=self.headers, data=data, params=param, proxies=prox, verify=False,
                                    timeout=60)
        else:
            res = self._session.post(url=url, headers=self.headers, data=data, params=param, proxies=prox, verify=False,
                                     timeout=60)
        if res.status_code == requests.codes.ok:
            # self.get_cookie(res)
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
            # self.get_cookie()
            res = self.req_(url, method, data, param)
        return res

    def get_data_detail(self, url):
        detail_list=list()
        print(url)

        res = self.request_(url, method='get')
        # print(res)
        if res:
            detail = etree.HTML(res)
            content= etree.tostring(detail.xpath("//tbody/tr/td/div")[0],method='HTML').decode()
            # for num in range(2,len(size)+1):
            #     detail_dict = {}
            #     proname = detail.xpath(f"//tr[{num}]/td[2]/text()")
            #     if proname:
            #         proname = proname[0].replace('\u3000','')
            price = detail.xpath(f"//tr[2]/td[4]/text()")
            if price :
                    price =price[0].replace(',','')
                # require = detail.xpath(f"//tr[{num}]/td[3]/text()")
                # if require:
                #     require = require[0]
            futher = detail.xpath(f"//tr[2]/td[5]/text()")
            if futher:
                    futher=futher[0]
                    if '年' in futher:
                        futher = int(time.mktime(time.strptime(futher.strip(), "%Y年%m月")))  #
                    else:
                        futher = int(time.mktime(time.strptime(futher.strip(), "%Y-%m")))  #
                # comment = detail.xpath(f"//tr[{num}]/td[6]/text()")
                # if comment:
                #     comment = comment[0]
                #
                # detail_dict['proname'] = proname
                # detail_dict['price'] = price
                # detail_dict['protype'] =
                # detail_dict['require'] = require
                # detail_dict['futher'] = futher
                # detail_dict['comment'] = comment
                # detail_list.append(detail_dict)

                # print( proname,price,require,futher,comment)
            return content,futher,price
        # except Exception as e:
        #     logging.error(f"list获取失败{e}\n{traceback.format_exc()}")



    def get_data_list(self, times,page):
        for rank in [2022,2021]:
            if page==1:
                url=f'http://www.ccgp-tianjin.gov.cn/portal/topicView.do?method=view&view=intention&id={rank}&ver=2&stmp={int(time.time()*1000)}'
                data_list = self.request_(url, method='post')
                self.get_cookie(self._session.cookies.get_dict())
            else:
                # pass

                url = f'http://www.ccgp-tianjin.gov.cn/portal/topicView.do?method=view&view=intention&page={page}&id={rank}&step=1&ldateQGE=&ldateQLE='
                data_list = self.request_(url, method='post')
                self.headers['Cookie'] = self.cookie
            print(url)

            payload = {
                'method': 'view',
                'page': page,
                'id': rank,
                'step': 1,
                'view': 'intention',
                'st':1,
                'ldateQGE': '',
                'ldateQLE': ''
            }
            data=None
            # data_list = self.request_(url,  method='post')
            # self.get_cookie(data_list)

            # print(data_list)
            if data_list:

                html=etree.HTML(data_list)
                all_data = html.xpath("//ul[@id='div_ul_1']/li")
                for data in all_data:
                    auditTime = data.xpath(f"./span/text()")
                    # print(auditTime)
                    auditTime=time.strftime("%Y-%m-%d",time.strptime(auditTime[0],"%a %b %d %H:%M:%S CST %Y"))
                    releasetime = int(time.mktime(time.strptime(auditTime, "%Y-%m-%d")))
                    todaytime = int(time.mktime(time.strptime(times, "%Y-%m-%d")))
                    print(releasetime, todaytime)
                    if releasetime >= todaytime:
                        title = data.xpath(f"./a/text()")[0]
                        # articleId = int(str(time.time()*1000)[::3])
                        href = data.xpath(f"./a/@href")[0]
                        articleId = re.findall(r'id=(\d+)&', href)[0]

                        procurement = title
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
                            districtName = '天津市'
                            # print(districtName, releasetime, articleId, procurement, href, title)
                        yield districtName, releasetime, articleId, procurement, href, title
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
        self.errors = 1

    def get_cookie(self,cookies):
        # url = 'http://www.ccgp-tianjin.gov.cn/'
        # session = requests.session()
        # proxy=self.proxys
        # session.get(url,proxies=proxy)
        # print(session.cookies)
        # cookies = res.cookies.get_dict()
        cookie = f"HttpOnly; HttpOnly; JSESSIONID={cookies['JSESSIONID']};TOPAPP_COOKIE={cookies['TOPAPP_COOKIE']}"
        # print(res.cookies.get_dict())
        self.cookie=cookie
        # self.headers['Cookie'] = cookie
        # print(cookie)
        # return cookie


def run(page,spider,times,file):
    # spider.get_cookie()
    for lis in spider.get_data_list(times,page):
        districtName,releasetime,articleId,procurement,href,title=lis
        # print(lis)
        prodict = spider.article_field()
        prodict['procurement'] = procurement
        prodict['districtName'] = districtName
        prodict['articleId'] = int(str(int(time.time() * 100000 + random.random() * 200))[-6:])
        prodict['publishDate'] = releasetime
        prodict['title'] = title
        detailurl = f'http://www.ccgp-tianjin.gov.cn/portal/documentView.do?method=view&id={articleId}&ver=2'
        prodict['detailurl'] = detailurl
        # print(detailurl)
        prodict['detail'],prodict['futher'],prodict['price'] = spider.get_data_detail(detailurl)
        print(prodict)
        # spider.write_data(file,str(prodict)+"\n")
        mysqldb = serversql()
        rundb(mysqldb, prodict)


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
    # spider=cgyxspider().get_data_list("2022-10-1",10)
    # for aa in spider:
    #     print(aa)
    file = os.path.basename('../unit.txt')
    with open(file, 'r') as f:
        if os.path.exists(file):
            read = f.readline()
            f.close()
            base = json.loads(read)
            print(base['time'])
    main(base['page'], base['time'], base['file'])
    print(time.time() - times)

