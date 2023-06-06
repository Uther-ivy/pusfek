# -*- coding: utf-8 -*-
import json, traceback
import re
import time, html
import requests
from lxml import etree
from lxml.etree import HTML
import tool
from save_database import process_item

# 常州市工程交易网
class xinyang_ggzy:
    def __init__(self):
        self.url_list = [
            'http://www.czgcjy.com/czztb/jyxx/010001/',
            'http://www.czgcjy.com/czztb/jyxx/010002/'
        ]
        self.url = self.url_list.pop(0)
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36',
        }

    def parse(self):
        date = tool.date
        # date = '2020-07-10'
        page = 1
        while True:
            text = tool.requests_get(self.url, self.headers)
            # print(11, text)
            # time.sleep(666)
            detail = HTML(text).xpath('/html/body/table/tr[2]/td/table/tr/td/table/tr/td[4]/table[2]/tr/td/table/tr')
            print('*' * 20, page, '*' * 20)
            for li in detail:
                try:
                    for tr in li.xpath('./td/table/tr[2]/td[2]/table/tr'):
                        title = tr.xpath('./td[2]/a/text()')[0]
                        url = 'http://www.czgcjy.com' + tr.xpath('./td[2]/a/@href')[0]
                        date_Today = tr.xpath('./td[3]/font/text()')[0].replace('(', '').replace(')', '')
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
                            break
                except:
                    traceback.print_exc()
                    continue
            print('正在切换类型')
            self.url = self.url_list.pop(0)


    def parse_detile(self, title, url, date):
        print(url)
        url_html = etree.HTML(tool.requests_get(url, self.headers))
        try:
            detail = url_html.xpath('//*[@id="_Sheet1"]')[0]
            detail_html = etree.tostring(detail, method='HTML')
            detail_html = html.unescape(detail_html.decode()).replace('\xa0', '').replace('\ufeff', '')
            detail_text = url_html.xpath('string(//*[@id="_Sheet1"])') \
                .replace('\xa0', '').replace('\n', '').replace('\r', '').replace('\t', '') \
                .replace(' ', '').replace('\xa5', '').replace('\ufeff', '')
        except:
            detail = url_html.xpath('//*[@id="TDContent"]')[0]
            detail_html = etree.tostring(detail, method='HTML')
            detail_html = html.unescape(detail_html.decode()).replace('\xa0', '').replace('\ufeff', '')
            detail_text = url_html.xpath('string(//*[@id="TDContent"])') \
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
        # print(item['body'])
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
        item['nativeplace'] = self.get_nativeplace_to(item['title'])
        item['linkman'] = tool.get_linkman(detail_text)
        item['function'] = tool.get_function(detail_text)
        item['resource'] = '常州市工程交易网'
        item["shi"] = 5504
        item['sheng'] = 5500
        item['removal']= title
        process_item(item)
        # print(item['body'])

    def get_nativeplace_to(self, city):
        a = ''
        ls = [['5504.001', '天宁区'], ['5504.002', '钟楼区'], ['5504.003', '戚墅堰区'], ['5504.004', '新北区'], ['5504.005', '武进区'], ['5504.006', '溧阳'], ['5504.007', '金坛']]
        for i in ls:
            if i[1] in city:
                a = i[0]
                break
        if a == '':
            return 5504
        else:
            return a

if __name__ == '__main__':

    import traceback, os
    try:
        jl = xinyang_ggzy()
        jl.parse()
    except Exception as e:
        traceback.print_exc()
        tool.send_error('报错文件：'+str(os.path.basename(__file__))+'报错信息：'+str(e))


