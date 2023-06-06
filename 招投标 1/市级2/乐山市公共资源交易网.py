# -*- coding: utf-8 -*-
import json
import re
import time, html
import requests
from lxml import etree
from lxml.etree import HTML
import tool
from save_database import process_item

# 乐山市公共资源交易网
class baoshan_ggzy:
    def __init__(self):
        self.url_list = [
            ['JYGCJS', 'ZBGG'],
            ['JYGCJS', 'PBJG'],
            ['JYZFCG', 'CGGG'],
            ['JYZFCG', 'GZGG'],
            ['JYZFCG', 'JGGG'],
            ['JYZFCG', 'ZZGG']
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
            data = {
                'rootCode': 'jyxx',
                'menuCode': self.url[0],
                'typeCode': self.url[1],
                'page': page,
                'areaCode': '',
                'title': '',
                'pubStime': '',
                'pubEtime': '',
                '_csrf': 'f8e504f8-cc39-4347-b398-d50ee9e709a1'
            }
            page += 1
            text = tool.requests_post('http://www.lsggzy.com.cn/pub/infoSearch', data, self.headers)
            print('*' * 20, page, '*' * 20)
            html = HTML(text)
            # print(11, text)
            # time.sleep(6666)
            detail = html.xpath('//*[@class="MainUl"]/ul/li')
            for li in detail:
                title = li.xpath('./a/@title')[0].replace('\n', '').replace('\r', '')\
                    .replace('\t', '').replace(' ', '')
                url = li.xpath('./a/@href')[0]
                if 'http' not in url:
                    url = 'http://www.lsggzy.com.cn' + url
                date_Today = li.xpath('./a/span[1]/text()')[0].replace('\n', '').replace('\r', '')\
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
            detail = url_html.xpath('//*[@id="content"]')[0]
            detail_html = etree.tostring(detail, method='HTML')
            detail_html = html.unescape(detail_html.decode())
            detail_text = url_html.xpath('string(//*[@id="content"])').replace('\xa0', '').replace('\n', '').\
                replace('\r', '').replace('\t', '').replace(' ', '').replace('\xa5', '')
            if len(detail_html) < 500:
                int('a')
        except:
            try:
                detail = url_html.xpath('/html/body/div[2]/div/div[2]/div/div[2]/div/div[3]')[0]
                detail_html = etree.tostring(detail, method='HTML')
                detail_html = html.unescape(detail_html.decode())
                detail_text = url_html.xpath('string(/html/body/div[2]/div/div[2]/div/div[2]/div/div[3])').replace('\xa0', '').replace('\n', ''). \
                    replace('\r', '').replace('\t', '').replace(' ', '').replace('\xa5', '')
                if len(detail_html) < 500:
                    int('a')
            except:
                detail = url_html.xpath('/html/body/div[2]/div/div[2]/div/div[2]')[0]
                detail_html = etree.tostring(detail, method='HTML')
                detail_html = html.unescape(detail_html.decode())
                detail_text = url_html.xpath('string(/html/body/div[2]/div/div[2]/div/div[2])').replace(
                    '\xa0', '').replace('\n', ''). \
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
        item['resource'] = '乐山市公共资源交易网'
        item['shi'] = 12010
        item['sheng'] = 12000
        item['removal']= title
        process_item(item)

    def get_nativeplace(self, addr):
        city = ''
        city_list = [['12010.001', '市中区'], ['12010.01', '马边彝族自治县'], ['12010.011', '峨眉山市'], ['12010.002', '沙湾区'], ['12010.003', '五通桥区'], ['12010.004', '金口河区'], ['12010.005', '犍为县'], ['12010.006', '井研县'], ['12010.007', '夹江县'], ['12010.008', '沐川县'], ['12010.009', '峨边彝族自治县']]

        for i in city_list:
            if i[1] in addr:
                city = float(i[0])
                break
        if city == '':
            city = 12010
        return city

if __name__ == '__main__':
    import traceback, os
    try:
        jl = baoshan_ggzy()
        jl.parse()
    except Exception as e:
        traceback.print_exc()
        tool.send_error('报错文件：'+str(os.path.basename(__file__))+'报错信息：'+str(e))


