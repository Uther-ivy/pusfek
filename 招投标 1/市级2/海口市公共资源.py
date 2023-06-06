# -*- coding: utf-8 -*-
import json
import re
import time, html
import requests
from lxml import etree
from lxml.etree import HTML
import tool
from save_database import process_item

# 海口市公共资源交易中心
class baoshan_ggzy:
    def __init__(self):
        self.url='http://ggzy.haikou.gov.cn/login.do?method=getSecondTableInfo'
        self.date_list=[
            {
                "currentPage": "1",
                "pageSize": "20",
                "flag": "3",
                "type": "GC_JY",
            },
            {
                "currentPage": "1",
                "pageSize": "20",
                "flag": "3",
                "type": "GC_GS",
                "notice_title":"",
            },
            {
                "currentPage": "1",
                "pageSize": "20",
                "flag": "3",
                "type": "GC_JG",
                "notice_title": "",
            },
            {
                "currentPage": "1",
                "pageSize": "20",
                "flag": "3",
                "type": "ZC_JY",
                "notice_title":"",
            },
            {
                "currentPage": "1",
                "pageSize": "20",
                "flag": "3",
                "type": "ZC_JG",
                "notice_title":"",
            }

        ]
        self.date = self.date_list.pop(0)
        self.headers = {
            'Accept': 'application/json, text/javascript, */*; q=0.01',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'zh-CN,zh;q=0.9',
            'Connection': 'keep-alive',
            'Content-Length': '57',
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'Cookie': 'JSESSIONID=AEB60058038E0BAE8109F8D019551528',
            'Host': 'ggzy.haikou.gov.cn',
            'Origin': 'http://ggzy.haikou.gov.cn',
            'Referer': 'http://ggzy.haikou.gov.cn/xxgk/zbgg/02/3_GC_JY_1.html',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36',
            'X-Requested-With': 'XMLHttpRequest'
        }

    def parse(self):
        while True:
            date = tool.date
            text = json.loads(tool.requests_post(self.url,self.date,self.headers))
            detail = text['result']
            for li in detail:
                url=f"http://ggzy.haikou.gov.cn/xxgk/zbgg/01/3_GC_JY_{li['KEYID']}.html"
                title = li['NAME']
                date_Today =li['TIME']
                if '发布' in date_Today:
                    continue
                if '测试' in title:
                    continue
                print(title, url, date_Today)
                if tool.Transformation(date) <= tool.Transformation(date_Today):
                    if tool.removal(title, date):
                        self.parse_detile(title, url, date_Today)
                    else:
                        print('【existence】', url)
                        continue
                else:
                    print('日期不符, 正在切换类型', date_Today, self.url)
                    continue
            self.date = self.date_list.pop(0)

    def parse_detile(self, title, url, date):
        headers={
            'Accept': 'application/json, text/javascript, */*; q=0.01',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'zh-CN,zh;q=0.9',
            'Cache - Control': 'max - age = 0',
            'Connection': 'keep-alive',
            'Cookie': 'JSESSIONID=AEB60058038E0BAE8109F8D019551528',
            'Host': 'ggzy.haikou.gov.cn',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36',
        }

        t = tool.requests_get(url, headers)
        # print(t)
        url_html = etree.HTML(t)
        detail = url_html.xpath('//div[@class="TRS_Editor"]')[0]
        # print(detail)
        detail_html = etree.tostring(detail, method='HTML')
        detail_html = html.unescape(detail_html.decode())
        detail_text = url_html.xpath('string(//div[@class="TRS_Editor"])').replace('\xa0', '').replace('\n', ''). \
            replace('\r', '').replace('\t', '').replace(' ', '').replace('\xa5', '')
        item = {}
        item['title'] = title.replace('\u2022', '')
        item['url'] = url
        item['date'] = date
        item['typeid'] = tool.get_typeid(item['title'])
        item['senddate'] = int(time.time())
        item['mid'] = 867
        item['infotype'] = tool.get_infotype(item['title'])
        item['body'] = tool.qudiao_width(detail_html)
        item['endtime'] = tool.get_endtime(detail_text)
        item['nativeplace'] = self.get_nativeplace(title)
        if item['endtime'] == '':
            item['endtime'] = int(time.mktime(time.strptime(date, "%Y-%m-%d")))
        else:
            try:
                item['endtime'] = int(time.mktime(time.strptime(item['endtime'], "%Y-%m-%d")))
            except:
                item['endtime'] = int(time.mktime(time.strptime(date, "%Y-%m-%d")))
        item['tel'] = tool.get_tel(detail_text)
        item['email'] = ''
        item['address'] = tool.get_address(detail_text)
        item['linkman'] = tool.get_linkman(detail_text)
        item['function'] = tool.get_function(detail_text)
        item['resource'] = '海口市公共资源交易中心'
        item["shi"] = 11001
        item['sheng'] = 11000
        # print(item)
        item['removal']= title
        process_item(item)

    def get_nativeplace(self, city):
        a = ''
        ls = [['11001.001', '秀英区'], ['11001.002', '龙华区'], ['11001.003', '琼山区'], ['11001.004', '美兰区']]

        for i in ls:
            if i[1] in city:
                a = i[0]
                break
        if a == '':
            return 11001
        else:
            return a

if __name__ == '__main__':

    import traceback, os
    try:
        jl = baoshan_ggzy()
        jl.parse()
    except Exception as e:
        traceback.print_exc()
