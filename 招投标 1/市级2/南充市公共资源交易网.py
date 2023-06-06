# -*- coding: utf-8 -*-
import json
import re
import time, html
import requests
from lxml import etree
from lxml.etree import HTML
import tool
from save_database import process_item

# 南充市公共资源交易网
class baoshan_ggzy:
    def __init__(self):
        self.url_list = [
            'http://www.scncggzy.com.cn/TPFront/ShowInfo/Jyxxsearch.aspx?area=&category=071002&categoryno=&Eptr3=&Paging={}',
            'http://www.scncggzy.com.cn/TPFront/ShowInfo/Jyxxsearch.aspx?area=&category=071003&categoryno=&Eptr3=&Paging={}',
            'http://www.scncggzy.com.cn/TPFront/ShowInfo/Jyxxsearch.aspx?area=&category=071005&categoryno=&Eptr3=&Paging={}',
            'http://www.scncggzy.com.cn/TPFront/ShowInfo/Jyxxsearch.aspx?area=&category=072001&categoryno=&Eptr3=&Paging={}',
            'http://www.scncggzy.com.cn/TPFront/ShowInfo/Jyxxsearch.aspx?area=&category=072002&categoryno=&Eptr3=&Paging={}',
            'http://www.scncggzy.com.cn/TPFront/ShowInfo/Jyxxsearch.aspx?area=&category=072003&categoryno=&Eptr3=&Paging={}',
        ]
        self.url = self.url_list.pop(0)
        self.headers = {
            'Cookie': 'homeid=1a444a31-e460-47ff-9931-1c075c0f3cd8',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36',
        }

    def parse(self):
        date = tool.date
        # date = '2020-12-01'
        page = 0
        while True:
            page += 1
            text = tool.requests_get(self.url.format(page), self.headers)
            print('*' * 20, page, '*' * 20)
            html = HTML(text)
            # print(11, res)
            # time.sleep(6666)
            detail = html.xpath('//*[@id="result"]/div/ul/li')
            for li in detail:
                title = li.xpath('./div/a/text()')[0].replace('\n', '').replace('\r', '')\
                    .replace('\t', '').replace(' ', '')
                url = li.xpath('./div/a/@href')[0].replace("window.open('", '').replace("');", '')
                if 'http' not in url:
                    url = 'http://www.scncggzy.com.cn' + url
                date_Today = li.xpath('./span/text()')[0].replace('\n', '').replace('\r', '') \
                    .replace('\t', '').replace(' ', '')
                if '067001' in self.url:
                    date_Today = li.xpath('./div[5]/p/text()')[0].replace('\n', '').replace('\r', '') \
                        .replace('\t', '').replace(' ', '')

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
        url_html = etree.HTML(tool.requests_get(url, self.headers))
        detail = url_html.xpath('//*[@id="TDContent"]')[0]
        detail_html = etree.tostring(detail, method='HTML')
        detail_html = html.unescape(detail_html.decode())
        detail_text = url_html.xpath('string(//*[@id="TDContent"])').replace('\xa0', '').replace('\n', '').\
            replace('\r', '').replace('\t', '').replace(' ', '').replace('\xa5', '')
        if len(detail_html) < 500:
            int('a')
        # print(detail_text.replace('\xa0','').replace('\xa5',''))
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
        item['resource'] = '南充市公共资源交易网'
        item['shi'] = 12011
        item['sheng'] = 12000
        item['removal']= title
        process_item(item)

    def get_nativeplace(self, addr):
        city = ''
        city_list = [['12011.001', '顺庆区'], ['12011.002', '高坪区'], ['12011.003', '嘉陵区'], ['12011.004', '南部县'], ['12011.005', '营山县'], ['12011.006', '蓬安县'], ['12011.007', '仪陇县'], ['12011.008', '西充县'], ['12011.009', '阆中市']]

        for i in city_list:
            if i[1] in addr:
                city = float(i[0])
                break
        if city == '':
            city = 12011
        return city

if __name__ == '__main__':
    import traceback, os
    try:
        jl = baoshan_ggzy()
        jl.parse()
    except Exception as e:
        traceback.print_exc()
        tool.send_error('报错文件：'+str(os.path.basename(__file__))+'报错信息：'+str(e))



