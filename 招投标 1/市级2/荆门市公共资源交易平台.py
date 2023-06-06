# -*- coding: utf-8 -*-
import json
import re
import time, html
import requests
from lxml import etree
from lxml.etree import HTML
import tool
from save_database import process_item

# 荆门市公共资源交易平台
class lijiang_ggzy:
    def __init__(self):
        self.url_list = [
            'http://121.61.253.44:9127/xxfb/{}.html'
        ]
        self.url = self.url_list.pop(0)
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36',
        }

    def parse(self):
        date = tool.date
        # date = '2020-04-07'
        page = 0
        while True:
            page += 1
            if page == 1:
                text = tool.requests_get(self.url.format('level'), self.headers)
            else:
                text = tool.requests_get(self.url.format(page), self.headers)
            print('*' * 20, page, '*' * 20)
            html = HTML(text)
            # print(11, res)
            # time.sleep(6666)
            detail = html.xpath('//*[@id="info"]/li')
            for li in detail:
                title = li.xpath('./a/@title')[0]
                url = 'http://121.61.253.44:9127' + li.xpath('./a/@href')[0]
                date_Today = li.xpath('./a/span[2]/text()')[0]
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
        try:
            detail = url_html.xpath('/html/body/div[2]/div[2]')[0]
            detail_html = etree.tostring(detail, method='HTML')
            detail_html = html.unescape(detail_html.decode()).replace('\xa0', '').replace('\xa5', '')
            detail_text = url_html.xpath('string(/html/body/div[2]/div[2])').replace('\xa0', '').replace('\n', '').\
                replace('\r', '').replace('\t', '').replace(' ', '').replace('\xa5', '')
        except:
            try:
                detail = url_html.xpath('/html/body/div[2]/div/div/div[2]/table')[0]
                detail_html = etree.tostring(detail, method='HTML')
                detail_html = html.unescape(detail_html.decode())
                detail_text = url_html.xpath('string(/html/body/div[2]/div/div/div[2]/table)').replace('\xa0',
                                                                                                           '').replace('\n',
                                                                                                                       ''). \
                    replace('\r', '').replace('\t', '').replace(' ', '').replace('\xa5', '')
                if len(detail) < 1000:
                    int('a')
            except:
                detail = url_html.xpath('/html/body/div[2]/div/div/div[2]')[0]
                detail_html = etree.tostring(detail, method='HTML')
                detail_html = html.unescape(detail_html.decode())
                detail_text = url_html.xpath('string(/html/body/div[2]/div/div/div[2])').replace('\xa0',
                                                                                                       '').replace('\n',
                                                                                                                   ''). \
                    replace('\r', '').replace('\t', '').replace(' ', '').replace('\xa5', '')
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
        item['body'] = detail_html
        item['body'] = item['body'].replace('阅读次数：', '')
        width_list = re.findall('width="(.*?)"', item["body"])
        for i in width_list:
            item["body"] = item["body"].replace('width="{}"'.format(i), '')
        width_list = re.findall('WIDTH: (.*?)pt;', item["body"])
        for i in width_list:
            item["body"] = item["body"].replace('WIDTH: {}pt;'.format(i), '')
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
        item['resource'] = '荆门市公共资源交易平台'
        item['shi'] = 9007
        item['sheng'] = 9000
        item['removal']= title
        process_item(item)

    def get_nativeplace(self, addr):
        city = ''
        city_list = [['9007.001', '钟祥'], ['9007.002', '沙洋县'], ['9007.003', '京山县'], ['9007.004', '掇刀区'], ['9007.005', '东宝区']]

        for i in city_list:
            if i[1] in addr:
                city = float(i[0])
                break
        if city == '':
            city = 9007
        return city

if __name__ == '__main__':

    import traceback, os
    try:
        jl = lijiang_ggzy()
        jl.parse()
    except Exception as e:
        traceback.print_exc()
        tool.send_error('报错文件：'+str(os.path.basename(__file__))+'报错信息：'+str(e))


