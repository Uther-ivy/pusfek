# -*- coding: utf-8 -*-
import json
import re
import time, html

import execjs
import requests
from lxml import etree
from lxml.etree import HTML
import tool
from save_database import process_item

# 必联网
class baoshan_ggzy:
    def __init__(self):
        self.url_list = [
          'http://bidding.fgw.hunan.gov.cn/ztb/api/getBiddingList?totalCount=713&limit=10&page={}&categoryId=92&areaNo='
        ]
        self.url = self.url_list.pop(0)
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36',
        }


    def parse(self):
        date = tool.date
        # date = '2020-12-17'
        page = 0
        while True:
            page += 1
            text = tool.requests_get(self.url.format(page), headers=self.headers)
            print('*' * 20, page, '*' * 20)
            print(text)
            # print(11, text)
            # time.sleep(6666)
            detail = json.loads(text)['page']['list']
            for li in detail:
                title = li['projectName']
                url = str(li['id'])

                date_Today = li['createTime'].split(' ')[0]
                if '测试' in title:
                    continue
                # print(title, url, date_Today)
                # time.sleep(666)
                if tool.Transformation(date) <= tool.Transformation(date_Today):
                    if tool.removal(title, date):
                        self.parse_detile(title, url, date_Today)
                    else:
                        print('【existence】', url)
                        continue
                else:
                    print('日期不符, 正在切换类型', date_Today, self.url)
                    self.url = self.url_list.pop(0)
                    page = 0
                    break
            if page == 20:
                self.url = self.url_list.pop(0)
                page = 0

    def parse_detile(self, title, url, date):
        print(url)
        url1=f'http://bidding.fgw.hunan.gov.cn/ztb/api/getBiddingInfo/{url}?COLLCC=3323414442&'
        t = tool.requests_get(url1,headers=self.headers)
        print(t,url1)
        text=json.loads(t)
        detail_text = t
        item = {}
        item['title'] = title
        item['url'] = f'http://bidding.fgw.hunan.gov.cn/bidding/notice/{url}?isdetail=1'
        item['date'] = date
        item['typeid'] = tool.get_typeid(item['title'])
        item['senddate'] = int(time.time())
        item['mid'] = 867
        item['nativeplace'] = tool.get_city(item['title'])
        item['infotype'] = tool.get_infotype(item['title'])
        item['body'] = ''
        item['endtime'] = tool.get_endtime(detail_text)

        if item['endtime'] == '':
            item['endtime'] = int(time.mktime(time.strptime(date, "%Y-%m-%d")))
        else:
            try:
                item['endtime'] = int(time.mktime(time.strptime(item['endtime'], "%Y-%m-%d")))
            except:
                item['endtime'] = int(time.mktime(time.strptime(date, "%Y-%m-%d")))
        item['tel'] = tool.get_tel(detail_text)
        item['email'] = ''
        item['address'] = tool.get_address(detail_text).replace('<em>','').replace('</em>','').replace('<p>','').replace('</p>','')

        item['linkman'] = tool.get_linkman(detail_text)
        item['function'] = tool.get_function(detail_text)
        item['linkman'] = tool.get_linkman(detail_text)
        item['function'] = tool.get_function(detail_text)
        item['resource'] = '湖南招投标监管网'
        item['shi'] = tool.get_city(text['TradeCenterName'])
        item['sheng'] = tool.get_sheng(item['title'])
        item['removal']= item['title']
        process_item(item)

    def get_nativeplace(self, addr):
        city = ''
        city_list = [['7004.001','梅列区'],['7004.01','泰宁县'],['7004.011','建宁县'],['7004.012','永安市'],['7004.002','三元区'],
    ['7004.003','明溪县'],['7004.004','清流县'],['7004.005','宁化县'],['7004.006','大田县'],['7004.007','尤溪县'],
    ['7004.008','沙　县'],['7004.009','将乐县']]
        for i in city_list:
            if i[1] in addr:
                city = float(i[0])
                break
        if city == '':
            city = 7004
        return city

if __name__ == '__main__':
    import traceback,os
    try:
        jl = baoshan_ggzy()
        jl.parse()
    except Exception as e:
        traceback.print_exc()
        tool.send_error('报错文件：'+str(os.path.basename(__file__))+'报错信息：'+str(e))



