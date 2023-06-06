# -*- coding: utf-8 -*-
import json
import re
import time, html
import requests
from lxml import etree
from lxml.etree import HTML
import tool
from save_database import process_item

# 西安市公共资源交易中心
class baoshan_ggzy:
    def __init__(self):
        self.url_list = [
            'http://www.xacin.com.cn/XianGcjy/web/tender/shed_gc.jsp?gc_type=5&page={}',
            'http://www.xacin.com.cn/XianGcjy/web/tender/shed_gc.jsp?gc_type=3&page={}',
            'http://www.xacin.com.cn/XianGcjy/web/tender/shed_gc.jsp?gc_type=6&page={}'
        ]
        self.url = self.url_list.pop(0)
        self.headers = {
            'Cookie': 'homeid=1a444a31-e460-47ff-9931-1c075c0f3cd8',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36',
        }

    def parse(self):
        date = tool.date
        # date = '2020-12-11'
        page = 0
        while True:
            page += 1
            text = tool.requests_get(self.url.format(page), self.headers)
            print('*' * 20, page, '*' * 20)
            html = HTML(text)
            # print(11, text)
            # time.sleep(6666)
            detail = html.xpath('/html/body/table[7]/tr[1]/td[2]/table[2]/tr')
            for li in detail:
                try:
                    title = li.xpath('./td[1]/a/@title')[0].replace('\n', '').replace('\r', '')\
                        .replace('\t', '').replace(' ', '')
                    url = li.xpath('./td[1]/a/@href')[0]
                except:
                    continue
                if 'http' not in url:
                    if '../../' in url:
                        url = 'http://www.xacin.com.cn/XianGcjy/web/tender/' + url[5:]
                    elif '../' in url:
                        url = 'http://www.xacin.com.cn/XianGcjy/web/tender/' + url[2:]
                    elif './' in url:
                        url = 'http://www.xacin.com.cn/XianGcjy/web/tender/' + url[1:]
                    else:
                        url = 'http://www.xacin.com.cn/XianGcjy/web/tender/' + url
                date_Today = li.xpath('./td[2]/text()')[0].replace('\n', '').replace('\r', '')\
                    .replace('\t', '').replace(' ', '').replace('.', '-')
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
        try:
            detail = url_html.xpath('//*[@id="gctable"]')[0]
            detail_html = etree.tostring(detail, method='HTML')
            detail_html = html.unescape(detail_html.decode()).replace('浏览次数：', '').replace('原文链接', '')
            detail_text = url_html.xpath('string(//*[@id="gctable"])').replace('\xa0', '').replace('\n', ''). \
                replace('\r', '').replace('\t', '').replace(' ', '').replace('\xa5', '')
            if len(detail_html) < 100:
                int('a')
        except:
            detail = url_html.xpath('/html/body/table[7]/tr[1]/td[2]/table[2]/tr/td/table/tr[1]')[0]
            detail_html = etree.tostring(detail, method='HTML')
            detail_html = html.unescape(detail_html.decode()).replace('浏览次数：', '').replace('原文链接', '')
            detail_text = url_html.xpath('string(/html/body/table[7]/tr[1]/td[2]/table[2]/tr/td/table/tr[1])').replace('\xa0', '').replace('\n', ''). \
                replace('\r', '').replace('\t', '').replace(' ', '').replace('\xa5', '')
            if len(detail_html) < 300:
                int('a')
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
        item['resource'] = '西安市公共资源交易中心'
        item['shi'] = 14001
        item['sheng'] = 14000
        item['removal']= title
        process_item(item)

    def get_nativeplace(self, addr):
        city = ''
        city_list = [['14001.001', '新城区'], ['14001.01', '蓝田县'], ['14001.011', '周至县'], ['14001.012', '户县'], ['14001.013', '高陵县'], ['14001.002', '碑林区'], ['14001.003', '莲湖区'], ['14001.004', '灞桥区'], ['14001.005', '未央区'], ['14001.006', '雁塔区'], ['14001.007', '阎良区'], ['14001.008', '临潼区'], ['14001.009', '长安区']]

        for i in city_list:
            if i[1] in addr:
                city = float(i[0])
                break
        if city == '':
            city = 14001
        return city

if __name__ == '__main__':
    import traceback, os
    try:
        jl = baoshan_ggzy()
        jl.parse()
    except Exception as e:
        traceback.print_exc()
        tool.send_error('报错文件：'+str(os.path.basename(__file__))+'报错信息：'+str(e))


