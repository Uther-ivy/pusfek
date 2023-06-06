# -*- coding: utf-8 -*-
import json
import re
import time, html
import requests
from lxml import etree
from lxml.etree import HTML
import tool
from save_database import process_item

# 龙成集团电子招标平台
class baoshan_ggzy:
    def __init__(self):
        self.url_list = [
            'http://zhaobiao.elongcheng.com:82/HomeSite/Site/NewsList?k=f86Jg1QShHaA5gKAgnWI2V5rt8s4pWBfHoqNbCOmKFnDVogFPixIVOPTQIUDZSrz&id={}',
            'http://zhaobiao.elongcheng.com:82/HomeSite/Site/NewsList?k=f86Jg1QShHZsPoaJQMWz2l5rt8s4pWBfHoqNbCOmKFnDVogFPixIVOPTQIUDZSrz&id={}',
            'http://zhaobiao.elongcheng.com:82/HomeSite/Site/NewsList?k=f86Jg1QShHbJCZx1w5cS%2BF5rt8s4pWBfHoqNbCOmKFnDVogFPixIVOPTQIUDZSrz&id={}',
            'http://zhaobiao.elongcheng.com:82/HomeSite/Site/NewsList?k=f86Jg1QShHbVV1jfLpST6F5rt8s4pWBfHoqNbCOmKFnDVogFPixIVOPTQIUDZSrz&id={}',
        ]
        self.url = self.url_list.pop(0)
        self.headers = {
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'Cookie': 'ASP.NET_SessionId=gtzmqpdtt0n5fje44v1i03sp; LastCookie=2021/8/18 15:12:35',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36',
        }

    def parse(self):
        date = tool.date
        # date = '2021-08-06'
        page = 0
        while True:
            page += 1
            text = tool.requests_get(self.url.format(page), self.headers).replace('\u2022', '')
            print('*' * 20, page, '*' * 20)
            html = HTML(text)
            detail = html.xpath('//*[@class="news-list unlist"]/li')
            for li in detail:
                title = li.xpath('./a/text()')[0].replace('\n', '').replace('\t', '').replace(' ', '').replace('\r', '')
                url = li.xpath('./a/@href')[0]
                url_domain = 'http://zhaobiao.elongcheng.com:82'
                if 'http' not in url:
                    if '../../' in url:
                        url = url_domain + url[5:]
                    elif '../' in url:
                        url = url_domain + url[2:]
                    elif './' in url:
                        url = url_domain + url[1:]
                    else:
                        url = url_domain + url
                date_Today = li.xpath('./span[1]/text()')[0]
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
            if page == 5:
                self.url = self.url_list.pop(0)
                page = 0

    def parse_detile(self, title, url, date):
        print(url)
        t = tool.requests_get(url, self.headers)
        url_html = etree.HTML(t)
        detail = url_html.xpath('//*[@id="divContent"]')[0]
        detail_html = etree.tostring(detail, method='HTML')
        detail_html = html.unescape(detail_html.decode()).replace('浏览次数：', '').replace('原文链接', '')
        detail_text = url_html.xpath('string(//*[@id="divContent"])').replace('\xa0', '').replace('\n', ''). \
            replace('\r', '').replace('\t', '').replace(' ', '').replace('\xa5', '')
        if detail_text == '':
            print('该新闻必须是注册用户才能阅读！')
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
        item['resource'] = '龙成集团电子招标平台'
        item['sheng'] = 8500
        item['nativeplace'] = 8513.005
        item['shi'] = 8513
        item['removal']= title
        process_item(item)

if __name__ == '__main__':
    import traceback,os
    try:
        jl = baoshan_ggzy()
        jl.parse()
    except Exception as e:
        traceback.print_exc()



