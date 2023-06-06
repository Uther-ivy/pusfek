# -*- coding: utf-8 -*-
import json
import re
import time, html
import requests
from lxml import etree
from lxml.etree import HTML
import tool
from save_database import process_item

# 南昌市公共资源交易网
class baoshan_ggzy:
    def __init__(self):
        self.url_list = ['http://www.jxsncggzy.cn/nczbw/jyxx/002001/',
                        'http://www.jxsncggzy.cn/nczbw/jyxx/002002/',
                        'http://www.jxsncggzy.cn/nczbw/jyxx/002003/',
                        'http://www.jxsncggzy.cn/nczbw/jyxx/002009/',
                        'http://www.jxsncggzy.cn/nczbw/jyxx/002004/',
                        'http://www.jxsncggzy.cn/nczbw/jyxx/002010/']
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
            text = tool.requests_get(self.url, self.headers)
            print('*' * 20, page, '*' * 20)
            html = HTML(text)
            # print(11, text)
            # time.sleep(6666)
            detail = html.xpath('/html/body/table[2]/tr/td/table/tr/td/table/tr/td[2]/table[2]/tr[2]/td/table/tr')
            for ul in detail:
                for li in ul.xpath('./td/table/tr[2]/td[2]/table/tr'):
                    title = li.xpath('./td[2]/a/@title')[0].replace('\n', '').replace('\r', '')\
                        .replace('\t', '').replace(' ', '')
                    url = li.xpath('./td[2]/a/@href')[0]
                    if 'http' not in url:
                        url = 'http://www.jxsncggzy.cn' + url
                    date_Today = li.xpath('./td[3]/font/text()')[0].replace('\n', '').replace('\r', '') \
                        .replace('\t', '').replace(' ', '').replace('(', '').replace(')', '')
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
                        break
            self.url = self.url_list.pop(0)
            page = 0
    def parse_detile(self, title, url, date):
        print(url)
        url_html = etree.HTML(tool.requests_get(url, self.headers))
        try:
            detail = url_html.xpath('//*[@id="spnShow"]')[0]
            detail_html = etree.tostring(detail, method='HTML')
            detail_html = html.unescape(detail_html.decode())
            detail_text = url_html.xpath('string(//*[@id="spnShow"])').replace('\xa0', '').replace('\n', '').\
                replace('\r', '').replace('\t', '').replace(' ', '').replace('\xa5', '')
            if len(detail_html) < 500:
                return
        except:
            return
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
        item['resource'] = '南昌市公共资源交易网'
        item['shi'] = 7501
        item['sheng'] = 7500
        item['removal']= title
        process_item(item)

    def get_nativeplace(self, addr):
        city = ''
        city_list = [['7501.001', '东湖区'], ['7501.002', '西湖区'], ['7501.003', '青云谱区'], ['7501.004', '湾里区'], ['7501.005', '青山湖区'], ['7501.006', '南昌县'], ['7501.007', '新建县'], ['7501.008', '安义县'], ['7501.009', '进贤县']]

        for i in city_list:
            if i[1] in addr:
                city = float(i[0])
                break
        if city == '':
            city = 7501
        return city

if __name__ == '__main__':
    import traceback, os
    try:
        jl = baoshan_ggzy()
        jl.parse()
    except Exception as e:
        traceback.print_exc()
        tool.send_error('报错文件：'+str(os.path.basename(__file__))+'报错信息：'+str(e))


