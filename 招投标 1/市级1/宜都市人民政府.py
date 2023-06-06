# -*- coding: utf-8 -*-
import json
import re
import time, html
import requests
from lxml import etree
from lxml.etree import HTML
import tool
from save_database import process_item

# 宜都市人民政府
class baoshan_ggzy:
    def __init__(self):
        self.url_list = [
            'https://xxgkapi.yichang.gov.cn/show/lists?jsoncallback=jQuery11240003985185487628939_1630571104283&areaid=8&webid=&cid=44&page=1&pagenums=20&orderby=1&_=1630571104288',
        ]
        self.url = self.url_list.pop(0)
        self.headers = {
            # 'Cookie': 'homeid=1a444a31-e460-47ff-9931-1c075c0f3cd8',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36',
        }

    def parse(self):
        while True:
            date = tool.date
            # date='2021-04-16'
            text = tool.requests_get(self.url,self.headers)
            text = '{' + text.split('({')[1][:-1]
            # print(text)
            # time.sleep(2222)
            detail = json.loads(text)
            for li in detail['lists']:
                url= f'https://xxgkapi.yichang.gov.cn/show/detail?jsoncallback=jQuery&areaid=8&id={li["n_id"]}&cache=on&'
                title = li['title']
                date_Today = li['vc_inputtime']
                if '发布' in date_Today:
                    continue
                if '测试' in title:
                    continue
                # print(title, url, date_Today)
                # # time.sleep(666)
                if tool.Transformation(date) <= tool.Transformation(date_Today):
                    if tool.removal(title, date):
                        self.parse_detile(title, url, date_Today)
                    else:
                        print('【existence】', url)
                        continue
                else:
                    print('日期不符, 正在切换类型', date_Today, self.url)
                    return

    def parse_detile(self, title, url, date):
        print(url)
        detail = tool.requests_get(url, self.headers).replace('jQuery(', '')
        # print(json.loads(detail[:-1])[0]['content'])
        # time.sleep(2222)
        detail_html = json.loads(detail[:-1])[0]['content']
        detail_text = ''.join(re.findall('>(.*?)<', detail_html, re.S)).replace('\xa0', '').replace('\n', ''). \
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
        item['nativeplace'] = 9004.011
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
        item['resource'] = '宜都市人民政府'
        item["shi"] = 9004
        item['sheng'] = 9000
        # print(item)
        item['removal']= title
        process_item(item)

    def get_nativeplace(self, addr):
        city = ''
        city_list = [['7509.001', '袁州区'], ['7509.01', '高安市'], ['7509.002', '奉新县'], ['7509.003', '万载县'], ['7509.004', '上高县'], ['7509.005', '宜丰县'], ['7509.006', '靖安县'], ['7509.007', '铜鼓县'], ['7509.008', '丰城市'], ['7509.009', '樟树市']]

        for i in city_list:
            if i[1] in addr:
                city = float(i[0])
                break
        if city == '':
            city = 7509
        return city

if __name__ == '__main__':

    import traceback, os
    try:
        jl = baoshan_ggzy()
        jl.parse()
    except Exception as e:
        traceback.print_exc()
