# -*- coding: utf-8 -*-
import json
import re
import time, html
import requests
from lxml import etree
from lxml.etree import HTML
import tool
from save_database import process_item

# 湖州市公共资源交易信息网
class baoshan_ggzy:
    def __init__(self):
        self.url_list = [
            'http://ggzy.huzhou.gov.cn/HZfront/jcjs/021001/021001006/',
            'http://ggzy.huzhou.gov.cn/HZfront/jcjs/021001/021001001',
            'http://ggzy.huzhou.gov.cn/HZfront/jcjs/021001/021001003',
            'http://ggzy.huzhou.gov.cn/HZfront/jcjs/021001/021001005',
            'http://ggzy.huzhou.gov.cn/HZfront/jcjs/021001/021001002',
            'http://ggzy.huzhou.gov.cn/HZfront/jcjs/021002/021002001',
            'http://ggzy.huzhou.gov.cn/HZfront/jcjs/021002/021002003',
            'http://ggzy.huzhou.gov.cn/HZfront/jcjs/021002/021002004',
            'http://ggzy.huzhou.gov.cn/HZfront/jcjs/021002/021002002',
            'http://ggzy.huzhou.gov.cn/HZfront/jcjs/021002/021002005',
            'http://ggzy.huzhou.gov.cn/HZfront/jcjs/021003/021003001',
            'http://ggzy.huzhou.gov.cn/HZfront/jcjs/021003/021003003',
            'http://ggzy.huzhou.gov.cn/HZfront/jcjs/021003/021003004',
            'http://ggzy.huzhou.gov.cn/HZfront/jcjs/021003/021003002',
            'http://ggzy.huzhou.gov.cn/HZfront/jcjs/021003/021003005',
        ]
        self.url = self.url_list.pop(0)
        self.headers = {
            # 'Cookie': 'homeid=1a444a31-e460-47ff-9931-1c075c0f3cd8',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36',
        }

    def parse(self):
        while True:
            date = tool.date
            text = tool.requests_get(url=self.url, headers=self.headers)
            html = HTML(text)
            detail = html.xpath('//table[@align="center"]//tr[@height="24"]')
            for li in detail:
                try:
                    url = li.xpath('./td[2]/a/@href')[0]
                except:
                    continue
                title = li.xpath('./td[2]/a/@title')[0]
                date_Today = li.xpath('./td[4]/font/text()')[0]
                if '测试' in title:
                    continue
                url_domain = 'http://ggzy.huzhou.gov.cn'
                if 'http' not in url:
                    if '../../' in url:
                        url = url_domain + url[5:]
                    elif '../' in url:
                        url = url_domain + url[2:]
                    elif './' in url:
                        url = url_domain + url[1:]
                    else:
                        url = url_domain + url
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

    def parse_detile(self, title, url, date):
        print(url)
        t = tool.requests_get(url, self.headers)
        url_html = etree.HTML(t)
        detail = url_html.xpath('//td[@class="infodetail"]')[0]
        # print(detail)
        detail_html = etree.tostring(detail, method='HTML')
        detail_html = html.unescape(detail_html.decode())
        detail_text = url_html.xpath('string(//td[@class="infodetail"])').replace('\xa0', '').replace('\n', ''). \
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
        item['resource'] = '湖州市公共资源交易信息网'
        item["shi"] = 6005
        item['sheng'] = 6000
        # print(item)
        item['removal']= title
        process_item(item)

    def get_nativeplace(self, addr):
        city = ''
        city_list = [['6005.001', '吴兴区'], ['6005.002', '南浔区'], ['6005.003', '德清县'], ['6005.004', '长兴县'], ['6005.005', '安吉县']]

        for i in city_list:
            if i[1] in addr:
                city = float(i[0])
                break
        if city == '':
            city = 6005
        return city

if __name__ == '__main__':

    import traceback, os
    try:
        jl = baoshan_ggzy()
        jl.parse()
    except Exception as e:
        traceback.print_exc()
