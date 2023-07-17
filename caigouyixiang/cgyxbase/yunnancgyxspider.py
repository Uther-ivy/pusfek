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
'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
'Content-Type':'application/x-www-form-urlencoded; charset=UTF-8',
'Connection':'keep-alive',
'Host':'www.ccgp-yunnan.gov.cn',
'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36',
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
            res_data = res.text
            return res_data

    def request_(self, url, method, data=None, param=None):
        try:
            res = self.req_(url, method, data, param)
        except Exception as e:
            logging.info("proxy disabled！！！ change proxy")
            time.sleep(random.random() * 10)
            self.replace_ip()
            res = self.req_(url, method, data, param)
        return res

    def get_data_info(self,uid):
        listurl = f'http://www.ccgp-yunnan.gov.cn/api/procurement/Procurement.purchaseList.svc?captchaCheckFlag=0&p=1'
        data = {

            'current': 1,
            'rowCount': 5,
            'searchPhrase': '',
            'unit_id': uid,
            'item_name': '',
            'purchasedate': '',
            'query_startTime': '',
            'query_endTime': ''

        }
        res =self.request_(listurl, method='post', data=data)
        return  res

    def get_data_detail(self, url):
        detail_list=list()
        print(url)
        res = self.request_(url, method='post')
        if res:
            content=json.loads(res).get('opcontent')
            detail = etree.HTML(content)
            # size= detail.xpath("//table[1]//tr")
            # for num in range(2,len(size)+1):
            #     detail_dict = {}
            #     proname = detail.xpath(f"//tr[{num}]/td[2]//text()")
            #     if proname:
            #         proname = proname[0].replace('\u3000','')
            #     require = detail.xpath(f"//tr[{num}]/td[3]//text()")
            #     if require:
            #         require = require[0]
            price = detail.xpath(f"//tr[2]/td[4]/font/text()")
            if price :
                    price =price[0]
            futher = detail.xpath(f"//tr[2]/td[5]/font/text()")
            if futher:
                    futher=futher[0]
                    if '年' in futher:
                        futher = int(time.mktime(time.strptime(futher.strip(), "%Y年%m月")))  #
                    else:
                        futher = int(time.mktime(time.strptime(futher.strip(), "%Y-%m")))  #
                # comment = detail.xpath(f"//tr[{num}]/td[6]/text()")
                # if comment:
                #     comment = comment[0]
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

    def get_data_list(self, times,page,cid):
            url=f'http://sj.yngp.com/governmentpolicy.do?method=queryPurchItemList&current={page}&rowCount=5&searchPhrase=&unit_id={cid}'
            # url=f'http://www.ccgp-yunnan.gov.cn/api/procurement/Procurement.purchaseList.svc?captchaCheckFlag=0&p={page}&current={page}&rowCount=5&searchPhrase=&unit_id={cid}&item_name=&unit_name=&purchasedate=&query_startTime=&query_endTime='
            payload =None
            data=None
            data_list = self.request_(url,  method='post',data=data,param=payload)
            # return data_list
            jsondata=json.loads(data_list)
            if jsondata:
                for lis in jsondata.get('rows'):
                    # unitid=lis['sys_purchaseintention_id']
                    districtName = ''
                    # res= self.get_data_info(unitid)
                    # datalist=json.loads(res)
                    # for lis in datalist.get('data').get('rows'):
                    releasetime = int(time.mktime(time.strptime(lis['purchasedate'], "%Y-%m-%d")))
                    # releasetime = int(lis['send_date']/1000)
                    todaytime = int(time.mktime(time.strptime(times, "%Y-%m-%d")))
                    print(releasetime,todaytime)
                    if releasetime >= todaytime:
                        articleId=lis['sys_purchaseintention_id']
                        procurement=lis['unit_name']
                        title=lis['item_name']
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
def run(page,spider,times,file,data):

        cid = data.get('id')
        area=data.get('name')
        for lis in spider.get_data_list(times,page,cid):
            districtName,releasetime,articleId,procurement,title=lis

            prodict = spider.article_field()
            prodict['procurement'] = procurement
            prodict['articleId'] = int(str(int(time.time() * 100000 + random.random() * 200))[-6:])
            prodict['publishDate'] = releasetime
            prodict['title'] = title
            if '县' in area:
                districtName = re.findall('(\w+县).*', area)
                if '市' in districtName:
                    districtName = re.findall('市(\w+县)', area)
                else:
                    districtName = ['云南省']
            elif '区' in area:
                districtName = re.findall('(\w+区)', area)
                if '市' in districtName:
                    districtName = re.findall('市(\w+区)', area)
                else:
                    districtName = ['云南省']
            elif '市' in area:
                districtName = re.findall('(\w+市).*', area)
            else:
                districtName = ['云南省']
            prodict['districtName'] = districtName
            showurl = f'http://www.ccgp-yunnan.gov.cn/viewPurchaseInfo.html?sys_purchaseintention_id={articleId}'
            detailurl = f'http://sj.yngp.com/governmentpolicy.do?method=viewPurchaseInfoA&R=1688801935037505.6592241992488&sys_purchaseintention_id={articleId}'
            prodict['detailurl'] = showurl
            prodict['detail'],prodict['futher'],prodict['price'] = spider.get_data_detail(detailurl)
            print(prodict)
            # spider.write_data(file,str(prodict)+"\n")
            mysqldb = serversql()
            rundb(mysqldb, prodict)
            print(detailurl)


def main(page, times, file):

    spider = cgyxspider()
    nodes = [
        {
            "id": "ynsysdw",
            "parentId": "budgetunit",
            "isLeaf": "1",
            "text": "云南省预算单位",
            "name": "云南省预算单位",
            "code": "530000",

            "nodes": []
        },
        {
            "id": "-52a5eac.163d4a36e81.-7fed",
            "parentId": "budgetunit",
            "isLeaf": "1",
            "text": "昆明市预算单位",
            "name": "昆明市预算单位",
            "code": "530100",

            "nodes": []
        },
        {
            "id": "533c866b.16a68bcee3c.-7d63",
            "parentId": "budgetunit",
            "isLeaf": "1",
            "text": "曲靖市预算单位",
            "name": "曲靖市预算单位",
            "code": "530300",

            "nodes": []
        },
        {
            "id": "5ba2af91.16a9609cb07.-7d80",
            "parentId": "budgetunit",
            "isLeaf": "1",
            "text": "玉溪市预算单位",
            "name": "玉溪市预算单位",
            "code": "530400",

            "nodes": []
        },
        {
            "id": "b067b8e.162f279bad5.-7ff3",
            "parentId": "budgetunit",
            "isLeaf": "1",
            "text": "保山市预算单位",
            "name": "保山市预算单位",
            "code": "530500",

            "nodes": []
        },
        {
            "id": "-249d8abc.164d5a77204.-7fcd",
            "parentId": "budgetunit",
            "isLeaf": "1",
            "text": "昭通市预算单位",
            "name": "昭通市预算单位",
            "code": "530600",

            "nodes": []
        },
        {
            "id": "533c866b.16a68bcee3c.-7a0c",
            "parentId": "budgetunit",
            "isLeaf": "1",
            "text": "丽江市预算单位",
            "name": "丽江市预算单位",
            "code": "530700",

            "nodes": []
        },
        {
            "id": "533c866b.16a68bcee3c.-7f43",
            "parentId": "budgetunit",
            "isLeaf": "1",
            "text": "普洱市预算单位",
            "name": "普洱市预算单位",
            "code": "530800",

            "nodes": []
        },
        {
            "id": "533c866b.16a68bcee3c.-7aff",
            "parentId": "budgetunit",
            "isLeaf": "1",
            "text": "临沧市预算单位",
            "name": "临沧市预算单位",
            "code": "530900",

            "nodes": []
        },
        {
            "id": "533c866b.16a68bcee3c.-7786",
            "parentId": "budgetunit",
            "isLeaf": "1",
            "text": "楚雄州预算单位",
            "name": "楚雄州预算单位",
            "code": "532300",

            "nodes": []
        },
        {
            "id": "-79fa5825.16a833da25d.-689e",
            "parentId": "budgetunit",
            "isLeaf": "1",
            "text": "红河州预算单位",
            "name": "红河州预算单位",
            "code": "532500",

            "nodes": []
        },
        {
            "id": "167b33b2.16a9542416a.-7c60",
            "parentId": "budgetunit",
            "isLeaf": "1",
            "text": "文山州预算单位",
            "name": "文山州预算单位",
            "code": "532600",

            "nodes": []
        },
        {
            "id": "533c866b.16a68bcee3c.-7651",
            "parentId": "budgetunit",
            "isLeaf": "1",
            "text": "版纳州预算单位",
            "name": "版纳州预算单位",
            "code": "532800",

            "nodes": []
        },
        {
            "id": "533c866b.16a68bcee3c.-78d3",
            "parentId": "budgetunit",
            "isLeaf": "1",
            "text": "大理州预算单位",
            "name": "大理州预算单位",
            "code": "532900",

            "nodes": []
        },
        {
            "id": "167b33b2.16a9542416a.-7ab0",
            "parentId": "budgetunit",
            "isLeaf": "1",
            "text": "德宏州预算单位",
            "name": "德宏州预算单位",
            "code": "533100",

            "nodes": []
        },
        {
            "id": "533c866b.16a68bcee3c.-7bce",
            "parentId": "budgetunit",
            "isLeaf": "1",
            "text": "怒江州预算单位",
            "name": "怒江州预算单位",
            "code": "533300",

            "nodes": []
        },
        {
            "id": "3d8379a0.16a68b176c2.-7b81",
            "parentId": "budgetunit",
            "isLeaf": "1",
            "text": "迪庆州预算单位",
            "name": "迪庆州预算单位",
            "code": "533400",

            "nodes": []
        },
        {
            "id": "542142eb.1666127bbaa.-7a52",
            "parentId": "budgetunit",
            "isLeaf": "1",
            "text": "滇中新区预算单位",
            "name": "滇中新区预算单位",
            "code": "533500",

            "nodes": []
        },
        {
            "id": "-f86b7fa.16cb2588503.-7f16",
            "parentId": "budgetunit",
            "isLeaf": "1",
            "text": "中国科学院昆明动物研究所",
            "name": "中国科学院昆明动物研究所",
            "code": "kmls02",
            "nodes": []
        },
        {
            "id": "4b8be852.162f5affea9.-7036",
            "parentId": "budgetunit",
            "isLeaf": "1",
            "text": "人民银行昆明中心支行",
            "name": "人民银行昆明中心支行",
            "code": "ls001",
            "nodes": []
        }
    ]
    for node in nodes:
        print(node)
        threads = []
        spider.replace_ip()
        for num in range(1, page):
            if spider.errors == 1:
                break
            t = threading.Thread(target=run, args=(num,spider, times,file,node),)
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

