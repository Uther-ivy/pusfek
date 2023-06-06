# -*- coding: utf-8 -*-
import json
import re
import time, html
import requests
from lxml import etree
from lxml.etree import HTML
import tool
from save_database import process_item

# 吉安市公共资源交易网
class baoshan_ggzy:
    def __init__(self):
        self.url_list = [
            'http://ggzy.jian.gov.cn/jyxx/jsgc/zbgg/{}.shtml',
            'http://ggzy.jian.gov.cn/jyxx/jsgc/zbgs/{}.shtml'
                         ]
        self.url = self.url_list.pop(0)
        self.headers = {
            'Cookie': 'homeid=1a444a31-e460-47ff-9931-1c075c0f3cd8',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36',
        }

    def parse(self):
        date = tool.date
        # date = '2021-07-26'
        page = 0
        while True:
            page += 1
            if page == 12:
                self.url = self.url_list.pop(0)
                page = 0
                continue
            if page == 1:
                text = tool.requests_get(self.url.format('index'), self.headers)
            else:
                text = tool.requests_get(self.url.format('index_' + str(page-1)), self.headers)
            print('*' * 20, page, '*' * 20)
            html = HTML(text)
            # print(11, text)
            # time.sleep(6666)
            detail = html.xpath('//*[@class="pagingList"]/ul/li')
            for li in detail:
                title = li.xpath('./a/@title')[0].replace('\n', '').replace('\r', '')\
                    .replace('\t', '').replace(' ', '').replace('<spanstyle="color:red">', '').replace('</span>', '')
                url = li.xpath('./a/@href')[0]
                if 'http' not in url:
                    url = 'http://ggzy.jian.gov.cn' + url
                date_Today = li.xpath('./span/text()')[0].replace('\n', '').replace('\r', '') \
                    .replace('\t', '').replace(' ', '').replace('[', '').replace(']', '').replace('/', '-')
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
            # print(self.url)


    def parse_detile(self, title, url, date):
        print(url)
        url_html = etree.HTML(tool.requests_get(url, self.headers))
        try:
            detail = url_html.xpath('//*[@class="TRS_PreAppend"]')[0]
            detail_html = etree.tostring(detail, method='HTML')
            detail_html = html.unescape(detail_html.decode())
            detail_text = url_html.xpath('string(//*[@class="TRS_PreAppend"])').replace('\xa0', '').replace('\n', '').\
                replace('\r', '').replace('\t', '').replace(' ', '').replace('\xa5', '')
        except:
            try:
                detail = url_html.xpath('//*[@class="TRS_Editor"]')[0]
                detail_html = etree.tostring(detail, method='HTML')
                detail_html = html.unescape(detail_html.decode())
                detail_text = url_html.xpath('string(//*[@class="TRS_Editor"])').replace('\xa0', '').replace('\n', ''). \
                    replace('\r', '').replace('\t', '').replace(' ', '').replace('\xa5', '')
            except:
                detail = url_html.xpath('//*[@class="text-main"]')[0]
                detail_html = etree.tostring(detail, method='HTML')
                detail_html = html.unescape(detail_html.decode())
                detail_text = url_html.xpath('string(//*[@class="text-main"])').replace('\xa0', '').replace('\n', ''). \
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
        item['resource'] = '吉安市公共资源交易网'
        item['shi'] = 7508
        item['sheng'] = 7500
        item['removal']= title
        process_item(item)

    def get_nativeplace(self, addr):
        city = ''
        city_list = [['7508.001', '吉州区'], ['7508.01', '万安县'], ['7508.011', '安福县'], ['7508.012', '永新县'], ['7508.013', '井冈山市'], ['7508.002', '青原区'], ['7508.003', '吉安县'], ['7508.004', '吉水县'], ['7508.005', '峡江县'], ['7508.006', '新干县'], ['7508.007', '永丰县'], ['7508.008', '泰和县'], ['7508.009', '遂川县']]

        for i in city_list:
            if i[1] in addr:
                city = float(i[0])
                break
        if city == '':
            city = 7508
        return city

if __name__ == '__main__':
    import traceback, os
    try:
        jl = baoshan_ggzy()
        jl.parse()
    except Exception as e:
        traceback.print_exc()
        tool.send_error('报错文件：'+str(os.path.basename(__file__))+'报错信息：'+str(e))


