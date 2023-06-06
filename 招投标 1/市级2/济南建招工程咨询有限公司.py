# -*- coding: utf-8 -*-
import json
import re
import time, html
import requests
from lxml import etree
from lxml.etree import HTML
import tool
from save_database import process_item

# 济南建招工程咨询有限公司
class xinyang_ggzy:
    def __init__(self):
        self.url_list = [
            # 招标公告
            '102',
            # 废标公告
            '119',
            # 中标公告
            '105'
        ]
        self.url = self.url_list.pop(0)
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36',
        }

    def parse(self):
        date = tool.date
        # date = '2020-07-01'
        page = 0
        while True:
            page += 1
            if page == 1:
                text = tool.requests_get('http://www.jnjianzhao.com/channels/{}.html'.format(self.url), self.headers)
            else:
                text = tool.requests_get('http://www.jnjianzhao.com/channels/{}_{}.html'.format(self.url, page), self.headers)
            html = HTML(text)
            print('*' * 20, page, '*' * 20)
            detail = html.xpath('//*[@id="main"]/div/div/div/div[2]/div[2]/ul/li')
            for li in detail:
                try:
                    title = li.xpath('./a/text()')[0].replace('\xa0', '').replace(' ', '')
                except:
                    title = li.xpath('./a/strong/text()')[0].replace('\xa0', '').replace(' ', '')
                url = 'http://www.jnjianzhao.com' + \
                      li.xpath('./a/@href')[0]
                date_Today = li.xpath('./span/text()')[0]
                # print(title, url, date_Today)
                # time.sleep(666)
                if '测试' in title:
                    continue
                if tool.Transformation(date) <= tool.Transformation(date_Today):
                    if tool.removal(title, date):
                        self.parse_detile(title, url, date_Today)
                    else:
                        print('【existence】', url)
                        continue
                else:
                    print('日期不符, 正在切换类型', date_Today)
                    self.url = self.url_list.pop(0)
                    page = 0
                    break
            if page == 20:
                self.url = self.url_list.pop(0)
                break
    def parse_detile(self, title, url, date):
        print(url)
        url_html = etree.HTML(tool.requests_get(url, self.headers))
        detail = url_html.xpath('//*[@id="main"]/div/div/div/div[2]/div[2]/div[2]')[0]
        detail_html = etree.tostring(detail, method='HTML')
        detail_html = html.unescape(detail_html.decode()).replace('\xa0', '').replace('\ufeff', '')
        detail_text = url_html.xpath('string(//*[@id="main"]/div/div/div/div[2]/div[2]/div[2])') \
            .replace('\xa0', '').replace('\n', '').replace('\r', '').replace('\t', '') \
            .replace(' ', '').replace('\xa5', '').replace('\ufeff', '')
        # print(detail_text.replace('\xa0','').replace('\xa5',''))
        # time.sleep(6666)
        item = {}
        item['title'] = title.replace('\u2022', '')
        item['url'] = url
        item['date'] = date
        item['typeid'] = tool.get_typeid(item['title'])
        item['senddate'] = int(time.time())
        item['mid'] = 867
        item['nativeplace'] = self.get_nativeplace_to(item['title'])
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
        item['resource'] = '济南建招工程咨询有限公司'
        item['shi'] = 8001
        item['sheng'] = 8000
        item['removal']= title
        process_item(item)
        # print(item['body'])

    def get_nativeplace_to(self, city):
        a = ''
        ls = [['8001', '济南'], ['8001.001', '历下区'], ['8001.01', '章丘'], ['8001.002', '中区'], ['8001.003', '槐荫区'], ['8001.004', '天桥区'], ['8001.005', '历城区'], ['8001.006', '长清区'], ['8001.007', '平阴县'], ['8001.008', '济阳县'], ['8001.009', '商河县']]
        for i in ls:
            if i[1] in city:
                a = i[0]
                break
        if a == '':
            return 8001
        else:
            return a

if __name__ == '__main__':
    jl = xinyang_ggzy()
    jl.parse()


