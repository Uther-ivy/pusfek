# -*- coding: utf-8 -*-
import json
import re
import time, html
import requests
from lxml import etree
from lxml.etree import HTML
import tool
from save_database import process_item

# 滨州市公共资源交易平台
class baoshan_ggzy:
    def __init__(self):
        self.url_list = [
            'http://www.bzggzyjy.cn/bzweb/002/002004/',
            'http://www.bzggzyjy.cn/bzweb/002/002005/',
                         ]
        self.url = self.url_list.pop(0)
        self.headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.75 Safari/537.36',
        }

    def parse(self):
        date = tool.date
        # date = '2021-07-27'
        page = 0
        while True:
            page += 1
            text = tool.requests_get(self.url, self.headers)
            print('*' * 20, page, '*' * 20)
            html_ = HTML(text)
            detail = html_.xpath('//*[@id="right"]/table/tr')
            for ul in detail:
                for li in ul.xpath('./td/table/tr[2]/td[2]/table/tr'):
                    title = li.xpath('./td[2]/a/@title')[0].replace('\n', '').replace('\r', '')\
                        .replace('\t', '').replace(' ', '')
                    url = li.xpath('./td[2]/a/@href')[0]
                    if 'http' not in url:
                        url = 'http://www.bzggzyjy.cn' + url
                    date_Today = li.xpath('./td[3]/font/text()')[0].replace('\n', '').replace('\r', '') \
                        .replace('\t', '').replace(' ', '').replace('(', '').replace(')', '').replace('.', '-')\
                        .replace('[', '').replace(']', '')
                    if '测试' in title:
                        continue
                    # print(title, url, date_Today)
                    # time.sleep(666)
                    if tool.Transformation(date_Today) == tool.Transformation(date):
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
        t = tool.requests_get(url, self.headers)
        url_html = etree.HTML(t)
        try:
            detail = url_html.xpath('//*[@id="ZtbzbggDetail_jsgc1_content"]')[0]
            detail_html = etree.tostring(detail, method='HTML')
            detail_html = html.unescape(detail_html.decode())
            detail_text = url_html.xpath('string(//*[@id="ZtbzbggDetail_jsgc1_content"])').replace('\xa0', '').replace('\n',
                                                                                                         ''). \
                replace('\r', '').replace('\t', '').replace(' ', '').replace('\xa5', '')
            if '没有相关公告' in detail_text:
                int('a')
        except:
            try:
                detail = url_html.xpath('//*[@id="TDContent"]')[0]
                detail_html = etree.tostring(detail, method='HTML')
                detail_html = html.unescape(detail_html.decode())
                detail_text = url_html.xpath('string(//*[@id="TDContent"])').replace('\xa0', '').replace(
                    '\n',
                    ''). \
                    replace('\r', '').replace('\t', '').replace(' ', '').replace('\xa5', '')
                if '没有相关公告' in detail_text:
                    int('a')
            except:
                detail = url_html.xpath('//*[@id="ZtbzbgsDetail_jsgc1_content"]')[0]
                detail_html = etree.tostring(detail, method='HTML')
                detail_html = html.unescape(detail_html.decode())
                detail_text = url_html.xpath('string(//*[@id="ZtbzbgsDetail_jsgc1_content"])').replace('\xa0', '').replace(
                    '\n',
                    ''). \
                    replace('\r', '').replace('\t', '').replace(' ', '').replace('\xa5', '')
                if '没有相关公告' in detail_text:
                    int('a')
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
        item['resource'] = '滨州市公共资源交易平台'
        item['shi'] = 8015
        item['sheng'] = 8000
        item['removal']= title
        process_item(item)

    def get_nativeplace(self, addr):
        city = ''
        city_list = [['8015.001', '滨城区'], ['8015.002', '惠民县'], ['8015.003', '阳信县'], ['8015.004', '无棣县'], ['8015.005', '沾化县'], ['8015.006', '博兴县'], ['8015.007', '邹平县']]

        for i in city_list:
            if i[1] in addr:
                city = float(i[0])
                break
        if city == '':
            city = 8015
        return city

if __name__ == '__main__':
    import traceback,os
    try:
        jl = baoshan_ggzy()
        jl.parse()
    except Exception as e:
        traceback.print_exc()
        tool.send_error('报错文件：'+str(os.path.basename(__file__))+'报错信息：'+str(e))


