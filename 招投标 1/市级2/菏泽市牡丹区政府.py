# -*- coding: utf-8 -*-
import json
import re
import time, html
import requests
from lxml import etree
from lxml.etree import HTML
import tool
from save_database import process_item

# 菏泽市牡丹区政府
class xinyang_ggzy:
    def __init__(self):
        self.url_list = [
            'http://www.mudan.gov.cn/module/xxgk/search.jsp?standardXxgk=1&infotypeId=A1200302&vc_title=&vc_number=&area='
        ]
        self.url = self.url_list.pop(0)
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36',
        }

    def parse(self):
        date = tool.date
        # date = '2021-07-23'
        page = 1
        data = {
            'infotypeId': '0',
            'jdid': '122',
            'divid': 'div23160',
            'vc_title': '',
            'vc_number': '',
            'currpage': '',
            'vc_filenumber': '',
            'vc_all': '',
            'texttype': '',
            'fbtime': '',
            'infotypeId': 'A1200302',
            'vc_title': '',
            'vc_number': '',
            'area': ''
        }
        text = tool.requests_post(self.url, data, self.headers)
        html = HTML(text)
        # print(11, text)
        # time.sleep(666)
        detail = html.xpath('//*[@class="zfxxgk_zdgkc"]//li')
        print('*' * 20, page, '*' * 20)
        for i in detail:
            title = i.xpath('./a/@title')[0]
            url = i.xpath('./a/@href')[0]
            date_Today = \
            i.xpath('./b/text()')[0].replace('\n', '').replace('\t', '').replace('/', '-').replace('\r',
                                                                                                        '').replace(
                ' ', '')
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
                break


    def parse_detile(self, title, url, date):
        print(url)
        t = tool.requests_get(url, self.headers)
        url_html = etree.HTML(t)
        detail = url_html.xpath('//*[@class="info_content"]')[0]
        detail_html = etree.tostring(detail, method='HTML')
        detail_html = html.unescape(detail_html.decode()).replace('\xa0', '').replace('\ufeff', '')
        detail_text = url_html.xpath('string(//*[@class="info_content"])') \
            .replace('\xa0', '').replace('\n', '').replace('\r', '').replace('\t', '') \
            .replace(' ', '').replace('\xa5', '').replace('\ufeff', '')
        # print(detail_text)
        # time.sleep(6666)
        item = {}
        item['title'] = title.replace('\u2022', '')
        item['url'] = url
        item['date'] = date
        item['typeid'] = tool.get_typeid(item['title'])
        item['senddate'] = int(time.time())
        item['mid'] = 867
        item['infotype'] = tool.get_infotype(item['title'])
        item['body'] = tool.qudiao_width(detail_html)
        # print(detail_html)
        # time.sleep(666)
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
        item['nativeplace'] = 8016.001
        item['linkman'] = tool.get_linkman(detail_text)
        item['function'] = tool.get_function(detail_text)
        item['resource'] = '菏泽市牡丹区政府'
        item["shi"] = 8016
        item['sheng'] = 8000
        item['removal']= title
        process_item(item)
        # print(item['body'])

    def get_nativeplace_to(self, city):
        a = ''
        ls = [['15501.001', '兴庆区'], ['15501.002', '西夏区'], ['15501.003', '金凤区'], ['15501.004', '永宁县'], ['15501.005', '贺兰县'], ['15501.006', '灵武']]
        for i in ls:
            if i[1] in city:
                a = i[0]
                break
        if a == '':
            return 15501
        else:
            return a

if __name__ == '__main__':
    jl = xinyang_ggzy()
    jl.parse()


