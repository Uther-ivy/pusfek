# -*- coding: utf-8 -*-
import json
import re
import time, html
import requests
from lxml import etree
from lxml.etree import HTML
import tool
from save_database import process_item

# 粤北人民医院
class baoshan_ggzy:
    def __init__(self):
        self.url_list = [
            'http://www.ybyy.net/index.php?m=content&c=index&a=lists&catid=256&page={}'
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
            text = tool.requests_get(self.url.format(page), self.headers).replace('\u2022', '')
            print('*' * 20, page, '*' * 20)
            html = HTML(text)
            detail = html.xpath('//*[@id="listbox"]/div/span/ul/li')
            for li in detail:
                title = li.xpath('./a/text()')[0].replace('\n', '').replace('\t', '').replace(' ', '').replace('\r', '')
                url = li.xpath('./a/@href')[0]
                url_domain = 'http://www.ybyy.net'
                if 'http' not in url:
                    if '../../' in url:
                        url = url_domain + url[5:]
                    elif '../' in url:
                        url = url_domain + url[2:]
                    elif './' in url:
                        url = url_domain + url[1:]
                    else:
                        url = url_domain + url
                date_Today = li.xpath('./i/text()')[0]\
                    .replace('\n', '').replace('\t', '').replace(' ', '').replace('\r', '').replace('[', '').replace(']', '')
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
                    return


    def parse_detile(self, title, url, date):
        print(url)
        t = tool.requests_get(url, self.headers)
        url_html = etree.HTML(t)
        detail = url_html.xpath('//*[@id="main"]/div/div[2]/div[2]/div[2]')[0]
        detail_html = etree.tostring(detail, method='HTML')
        detail_html = html.unescape(detail_html.decode()).replace('浏览次数：', '').replace('原文链接', '')
        detail_text = url_html.xpath('string(//*[@id="main"]/div/div[2]/div[2]/div[2])').replace('\xa0', '').replace('\n', ''). \
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
        item['resource'] = '粤北人民医院'
        item['sheng'] = 10000
        item['nativeplace'] = self.get_nativeplace(item['address'])
        item['shi'] = 10002
        item['removal']= title
        process_item(item)

    def get_nativeplace(self, addr):
        city = ''
        city_list = [['10002.001', '武江区'], ['10002.01', '南雄市'], ['10002.002', '浈江区'], ['10002.003', '曲江区'], ['10002.004', '始兴县'], ['10002.005', '仁化县'], ['10002.006', '翁源县'], ['10002.007', '乳源瑶族自治县'], ['10002.008', '新丰县'], ['10002.009', '乐昌市']]

        for i in city_list:
            if i[1] in addr:
                city = float(i[0])
                break
        if city == '':
            city = 10002
        return city

if __name__ == '__main__':
    import traceback,os
    try:
        jl = baoshan_ggzy()
        jl.parse()
    except Exception as e:
        traceback.print_exc()



