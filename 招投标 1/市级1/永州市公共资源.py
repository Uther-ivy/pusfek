# -*- coding: utf-8 -*-
import json
import re
import time, html
import requests
from lxml import etree
from lxml.etree import HTML
import tool
from save_database import process_item

# 永州市公共资源
class baoshan_ggzy:
    def __init__(self):
        self.url_list = [
            'https://yongzhou.hnsggzy.com/gczb/index.jhtml',
            'https://yongzhou.hnsggzy.com/jygkzfcg/index.jhtml',
            'https://yongzhou.hnsggzy.com/jygktd/index.jhtml',
            'https://yongzhou.hnsggzy.com/cqjy/index.jhtml',

        ]
        self.url = self.url_list.pop(0)
        self.headers = {
            # 'Cookie': 'homeid=1a444a31-e460-47ff-9931-1c075c0f3cd8',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36',
        }

    def parse(self):
        while True:
            date = tool.date
            # date = '2021-07-26'
            text = tool.requests_get(self.url,self.headers)
            html = HTML(text)
            detail = html.xpath('//ul[@class="article-list2"]//li')
            for li in range(len(detail)):
                url=html.xpath(f'(//ul[@class="article-list2"]//li//a//@href)[{li+1}]')[0]
                title = ''.join(html.xpath(f'(//ul[@class="article-list2"]//li//a)[{li+1}]//text()')).strip()
                date_Today = html.xpath(f'(//ul[@class="article-list2"]//li//div[@class="list-times"]//text())[{li+1}]')[0]
                if '发布' in date_Today:
                    continue
                if '测试' in title:
                    continue
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
        t = tool.requests_get(url, self.headers)
        url_html = etree.HTML(t)
        detail = url_html.xpath('//table[@class="gycq-table"]')[0]
        # print(detail)
        detail_html = etree.tostring(detail, method='HTML')
        detail_html = html.unescape(detail_html.decode())
        detail_text = url_html.xpath('string(//table[@class="gycq-table"])').replace('\xa0', '').replace('\n', ''). \
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
        item['resource'] = '永州市公共资源'
        item["shi"] = 9511
        item['sheng'] = 9500
        # print(item)
        item['removal']= title
        process_item(item)

    def get_nativeplace(self, addr):
        city = ''
        city_list = [['9511.001', '芝山区'], ['9511.01', '新田县'], ['9511.011', '江华瑶族自治县'], ['9511.002', '冷水滩区'], ['9511.003', '祁阳县'], ['9511.004', '东安县'], ['9511.005', '双牌县'], ['9511.006', '道县'], ['9511.007', '江永县'], ['9511.008', '宁远县'], ['9511.009', '蓝山县']]
        for i in city_list:
            if i[1] in addr:
                city = float(i[0])
                break
        if city == '':
            city = 9511
        return city

if __name__ == '__main__':

    import traceback, os
    try:
        jl = baoshan_ggzy()
        jl.parse()
    except Exception as e:
        traceback.print_exc()
