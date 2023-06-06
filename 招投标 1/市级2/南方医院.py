# -*- coding: utf-8 -*-
import json
import re
import time, html
import requests
from lxml import etree
from lxml.etree import HTML
import tool
from save_database import process_item

# 南方医院
class baoshan_ggzy:
    def __init__(self):
        self.url_list = [
            'http://www.nfyy.com/xwzx/yygg/index{}.html'
        ]
        self.url = self.url_list.pop(0)
        self.headers = {
            'Cookie': 'homeid=1a444a31-e460-47ff-9931-1c075c0f3cd8',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36',
        }

    def parse(self):
        date = tool.date
        # date = '2021-08-13'
        page = 0
        while True:
            page += 1
            if page == 1:
                text = tool.requests_get(self.url.format(''), self.headers).replace('\u2022', '')
            else:
                text = tool.requests_get(self.url.format('_{}'.format(page)), self.headers).replace('\u2022', '')
            print('*' * 20, page, '*' * 20)
            html = HTML(text)
            detail = html.xpath('//*[@class="clearfix"]/li')
            for li in detail[1:]:
                title = li.xpath('./div/h3/a/text()')[0].replace('\n', '').replace('\t', '').replace(' ', '').replace('\r', '')
                url = li.xpath('./div/h3/a/@href')[0]
                url_domain = 'http://www.nfyy.com'
                if 'http' not in url:
                    if '../../' in url:
                        url = url_domain + url[5:]
                    elif '../' in url:
                        url = url_domain + url[2:]
                    elif './' in url:
                        url = url_domain + url[1:]
                    else:
                        url = url_domain + url
                date_Today = li.xpath('./div/em/text()')[0]\
                    .replace('\n', '').replace('\t', '').replace(' ', '').replace('\r', '')[:10]
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
                break

    def parse_detile(self, title, url, date):
        print(url)
        t = tool.requests_get(url, self.headers)
        url_html = etree.HTML(t)
        detail = url_html.xpath('//*[@class="art_con"]')[0]
        detail_html = etree.tostring(detail, method='HTML')
        detail_html = html.unescape(detail_html.decode()).replace('浏览次数：', '').replace('原文链接', '')
        detail_text = url_html.xpath('string(//*[@class="art_con"])').replace('\xa0', '').replace('\n', ''). \
            replace('\r', '').replace('\t', '').replace(' ', '').replace('\xa5', '')
        if len(detail_text) < 300:
            return
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
        item['resource'] = '南方医院'
        item['sheng'] = 10000
        item['nativeplace'] = self.get_nativeplace(item['address'])
        item['shi'] = 10001
        item['removal']= title
        process_item(item)

    def get_nativeplace(self, addr):
        city = ''
        city_list = [['10001.001', '东山区'], ['10001.01', '花都区'], ['10001.011', '增城市'], ['10001.012', '从化市'], ['10001.002', '荔湾区'], ['10001.003', '越秀区'], ['10001.004', '海珠区'], ['10001.005', '天河区'], ['10001.006', '芳村区'], ['10001.007', '白云区'], ['10001.008', '黄埔区'], ['10001.009', '番禺区'], ['10001.013', '南沙区'], ['10001.014', '开发区']]

        for i in city_list:
            if i[1] in addr:
                city = float(i[0])
                break
        if city == '':
            city = 10001
        return city

if __name__ == '__main__':
    import traceback,os
    try:
        jl = baoshan_ggzy()
        jl.parse()
    except Exception as e:
        traceback.print_exc()



