# -*- coding: utf-8 -*-
import json
import re
import time, html
import requests
from lxml import etree
from lxml.etree import HTML
import tool
from save_database import process_item

# 龙岩市公共资源交易中心
class baoshan_ggzy:
    def __init__(self):
        self.url_list = [
            'https://ggzy.longyan.gov.cn/lyztb/gcjs/moreinfo.html',
            'https://ggzy.longyan.gov.cn/lyztb/zqcg/moreinfo.html',
        ]
        self.url = self.url_list.pop(0)
        self.headers = {
            # 'Cookie': 'homeid=1a444a31-e460-47ff-9931-1c075c0f3cd8',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36',
        }

    def parse(self):
        while True:
            date = tool.date
            date='2021-12-17'
            text = tool.requests_get(self.url,self.headers)
            # print(text)
            html = HTML(text)
            detail = html.xpath('//ul[@class="list"]//li')
            # print(de)
            for li in range(len(detail)):
                # print(html.xpath('(//table[@id="dataTable"]//tr//@id)[1]'))
                url = html.xpath(f'(//ul[@class="list"]//li//a//@href)[{li+1}]')[0]
                title = html.xpath(f'(//ul[@class="list"]//li//a//text())[{li+1}]')[0].strip()

                date_Today = html.xpath(f'(//ul[@class="list"]//li//span//text())[{li+1}]')[0].strip()
                if '发布' in date_Today:
                    continue
                if '测试' in title:
                    continue
                url="https://ggzy.longyan.gov.cn"+url
                # print(title, url, date_Today)
                # time.sleep(666)
                if tool.Transformation(date) <= tool.Transformation(date_Today):
                    if tool.removal(title, date):
                        self.parse_detile(title, url, date_Today)
                    else:
                        print('【existence】', url)
                        continue
                else:
                    # print(tool.Transformation(date),self.Transformation(date_Today))
                    # print('日期不符, 正在切换类型', date_Today, self.url)
                    print('日期不符', date_Today)
                    self.url = self.url_list.pop(0)
                    page = 0
                    continue
            self.url = self.url_list.pop(0)


    def parse_detile(self, title, url, date):
        print(url)
        t = tool.requests_get(url, self.headers)
        url_html = etree.HTML(t)
        detail = url_html.xpath('//*[@id="mainContent"]')[0]
        # print(detail)
        detail_html = etree.tostring(detail, method='HTML')
        detail_html = html.unescape(detail_html.decode())
        detail_text = url_html.xpath('string(//*[@id="mainContent"])').replace('\xa0', '').replace('\n', ''). \
            replace('\r', '').replace('\t', '').replace(' ', '').replace('\xa5', '')
        # if len(detail_text) < 100:
        #     return
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
        item['resource'] = '龙岩市公共资源交易中心'
        item["shi"] = 7008
        item['sheng'] = 7000
        # print(item)
        item['removal']= title
        process_item(item)

    def get_nativeplace(self, addr):
        city = ''
        city_list = [['7008.001', '新罗区'], ['7008.002', '长汀县'], ['7008.003', '永定县'], ['7008.004', '上杭县'], ['7008.005', '武平县'], ['7008.006', '连城县'], ['7008.007', '漳平市']]

        for i in city_list:
            if i[1] in addr:
                city = float(i[0])
                break
        if city == '':
            city = 7008
        return city

if __name__ == '__main__':
    import traceback, os
    try:
        jl = baoshan_ggzy()
        jl.parse()
    except Exception as e:
        traceback.print_exc()


