# -*- coding: utf-8 -*-
import json
import re
import time, html
import requests
from lxml import etree
from lxml.etree import HTML
import tool
from save_database import process_item

# 云南木典采招投交易网
class wenshan_ggzy:
    def __init__(self):
        self.url_list = [
            'https://www.e-czt.com/ydcms/category/allDataList.html?searchDate=1998-03-30&dates=300&word=&categoryId=2&tenderType=02&page={}', #招标公告
                    ]
        self.url = self.url_list.pop(0)
        self.headers={'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36'}
    def parse(self):
        date = tool.date
        # date = '2020-09-21'
        page = 0
        while True:
            page += 1
            text = tool.requests_get(url=self.url.format(page), headers=self.headers)
            print('*' * 20, page, '*' * 20)
            html = HTML(text)
            # print(11, text)
            # time.sleep(6666)
            detail = html.xpath('//div[@class="bd"]/ul/li')
            for li in detail:
                title = li.xpath('./div[1]/div[1]/a/@title')[0]
                date_Today = li.xpath('./div[1]/div[2]/div[4]/b/text()')[0].replace('\r', '').replace('\t', '').replace('\n', '').replace(' ','')
                print(date_Today)
                url = li.xpath('./div[1]/div[1]/a/@href')[0]
                # print(title, url, date_Today)
                # time.sleep(666)
                # self.parse_detile(title, url, date_Today)
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
                print('日期不符, 正在切换类型')
                self.url = self.url_list.pop(0)
                break

    def parse_detile(self, title, url, date):
        print(url)
        t = tool.requests_get(url=url, headers=self.headers)
        # print(t)
        # time.sleep(2222)
        url_html = etree.HTML(t)
        pdf = url_html.xpath('//div[@id="showPdf"]//@src')
        item = {}
        if pdf:
            pdf = pdf[0]
            item['body'] = pdf
        else:
            detail = url_html.xpath('//div[@id="container"]')[0]
            detail_html = etree.tostring(detail, method='HTML')
            detail_html = html.unescape(detail_html.decode()).replace("display: none", '')
            detail_text = url_html.xpath('string(//div[@id="container"]//text())').replace('\xa0', '').replace('\n',
                                                                                                                   ''). \
                replace('\r', '').replace('\t', '').replace(' ', '').replace('\xa5', '')
            if len(detail_html) < 200:
                int('a')

            item['title'] = title.replace('\u2022', '')
            item['url'] = url
            item['date'] = date
            item['typeid'] = tool.get_typeid(item['title'])
            item['senddate'] = int(time.time())
            item['mid'] = 867
            item['nativeplace'] = self.get_nativeplace(item['title'])
            item['infotype'] = tool.get_infotype(item['title'])
            item['body'] = tool.qudiao_width(detail_html)
            item['body'] = item['body']
            # print(item['body'].replace('\xa0', '').replace('\xa5', '').replace('\xb3', ''))
            # time.sleep(6666)
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
            item['resource'] = '云南木典采招投交易网'
            item['shi'] = 6507
            item['sheng'] = 6500
            item['removal'] = title
        # print(item["body"])
        process_item(item)
    def get_nativeplace(self, addr):
        city = ''
        city_list = [['6507.001', '铜官山区'], ['6507.002', '狮子山区'], ['6507.003', '郊区'], ['6507.004', '铜陵县']]
        for i in city_list:
            if i[1] in addr:
                city = float(i[0])
                break
        if city == '':
            city = 6507
        return city

if __name__ == '__main__':
    import os,traceback
    try:
        jl = wenshan_ggzy()
        jl.parse()
    except Exception as e:
        traceback.print_exc()
        tool.send_error('报错文件：'+str(os.path.basename(__file__))+'报错信息：'+str(e))



