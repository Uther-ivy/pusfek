# -*- coding: utf-8 -*-
import json
import re
import time, html
import requests
from lxml import etree
from lxml.etree import HTML
import tool
from save_database import process_item

# 泰州市公共资源交易平台
class baoshan_ggzy:
    def __init__(self):
        self.url_list = [
            'http://ggzy.taizhou.gov.cn/jyxx/{}.html',
                         ]
        self.url = self.url_list.pop(0)
        self.headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
            'Host': 'ggzy.taizhou.gov.cn',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.75 Safari/537.36',
        }

    def parse(self):
        date = tool.date
        # date = '2021-03-29'
        page = 0
        while True:
            page += 1
            if page == 1:
                text = tool.requests_get(self.url.format('secondPagejyxx'), self.headers)
            else:
                text = tool.requests_get(self.url.format(page), self.headers)
            print('*' * 20, page, '*' * 20)
            html = HTML(text)
            detail = html.xpath('//*[@id="showList"]/tr')
            for li in detail:
                title = li.xpath('./td[2]/a/text()')[0].replace('\n', '').replace('\r', '')\
                    .replace('\t', '').replace(' ', '').replace('<spanstyle="color:red">', '').replace('</span>', '')
                url = li.xpath('./td[2]/a/@href')[0]
                if 'http' not in url:
                    url = 'http://ggzy.taizhou.gov.cn' + url
                date_Today = li.xpath('./td[3]/text()')[0].replace('\n', '').replace('\r', '') \
                    .replace('\t', '').replace(' ', '').replace('(', '').replace(')', '').replace('.', '-')\
                    .replace('[', '').replace(']', '')
                if '测试' in title:
                    continue
                # time.sleep(666)
                if tool.Transformation(date_Today) >= tool.Transformation(date):
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
        try:
            detail = url_html.xpath('//*[@id="Table0"]')[0]
            detail_html = etree.tostring(detail, method='HTML')
            detail_html = html.unescape(detail_html.decode())
            detail_text = url_html.xpath('string(//*[@id="Table0"])').replace('\xa0', '').replace('\n',
                                                                                                         ''). \
                replace('\r', '').replace('\t', '').replace(' ', '').replace('\xa5', '')
            if len(detail_html) < 300:
                return
        except:
            detail = url_html.xpath('//*[@class="ewb-trade-right l"]')[0]
            detail_html = etree.tostring(detail, method='HTML')
            detail_html = html.unescape(detail_html.decode())
            detail_text = url_html.xpath('string(//*[@class="ewb-trade-right l"])').replace('\xa0', '').replace('\n',
                                                                                                  ''). \
                replace('\r', '').replace('\t', '').replace(' ', '').replace('\xa5', '')
            if len(detail_html) < 300:
                return
        # print(111, detail_text.replace('\xa0','').replace('\xa5',''))
        # time.sleep(6666)
        item = {}
        item['title'] = title.replace('\u2022', '')
        item['url'] = url
        item['date'] = date
        item['typeid'] = tool.get_typeid(item['title'])
        item['senddate'] = int(time.time())
        item['mid'] = 867
        item['nativeplace'] = self.get_nativeplace(item['title'])
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
        item['resource'] = '泰州市公共资源交易平台'
        item['shi'] = 5512
        item['sheng'] = 5500
        item['removal']= title
        process_item(item)

    def get_nativeplace(self, addr):
        city = ''
        city_list = [['5512.001', '海陵区'], ['5512.002', '高港区'], ['5512.003', '兴化市'], ['5512.004', '靖江市'], ['5512.005', '泰兴市'], ['5512.006', '姜堰市']]

        for i in city_list:
            if i[1] in addr:
                city = float(i[0])
                break
        if city == '':
            city = 5512
        return city

if __name__ == '__main__':
    import traceback, os
    try:
        jl = baoshan_ggzy()
        jl.parse()
    except Exception as e:
        traceback.print_exc()
