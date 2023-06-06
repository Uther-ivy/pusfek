# -*- coding: utf-8 -*-
import json
import re
import time, html
import requests
from lxml import etree
from lxml.etree import HTML
import tool
from save_database import process_item

# 南平市公共资源交易网
class baoshan_ggzy:
    def __init__(self):
        self.url_list = [
            'http://ggzy.np.gov.cn/npztb/jsgc/010001/?Paging={}',
            'http://ggzy.np.gov.cn/npztb/jsgc/010002/?Paging={}',
            'http://ggzy.np.gov.cn/npztb/jsgc/010003/?Paging={}',
            'http://ggzy.np.gov.cn/npztb/jsgc/010004/?Paging={}',
            'http://ggzy.np.gov.cn/npztb/jsgc/010005/?Paging={}'
        ]
        self.url = self.url_list.pop(0)
        self.headers = {
            'Cookie': 'homeid=1a444a31-e460-47ff-9931-1c075c0f3cd8',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36',
        }

    def parse(self):
        date = tool.date
        # date = '2021-07-23'
        page = 0
        while True:
            page += 1
            text = tool.requests_get(self.url.format(page), self.headers)
            print('*' * 20, page, '*' * 20)
            html = HTML(text)
            mi1 = 0
            if '010001' in text:
                mi1 = 1
            elif '010002' in text:
                mi1 = 2
            elif '010003' in text:
                mi1 = 3
            elif '010004' in text:
                mi1 = 4
            elif '010005' in text:
                mi1 = 5
            # print(11, text)
            # time.sleep(6666)
            detail = html.xpath('/html/body/div[2]/div[2]/div/div[1]/table/tr')
            for li in detail:
                title = li.xpath('./td[2]/a/@title')[0].replace('\n', '').replace('\t', '').replace(' ', '').replace(
                    '\r', '')
                url = li.xpath('./td[2]/a/@href')[0]
                url_domain = 'http://ggzy.np.gov.cn'
                if 'http' not in url:
                    if '../../' in url:
                        url = url_domain + url[5:]
                    elif '../' in url:
                        url = url_domain + url[2:]
                    elif './' in url:
                        url = url_domain + url[1:]
                    else:
                        url = url_domain + url
                date_Today = li.xpath('./td[3]/text()')[0].replace('\n', '').replace('\t', '').replace(' ', '').replace(
                    '\r', '').replace('[', '').replace(']', '')
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
        t = tool.requests_get(url, self.headers)
        url_html = etree.HTML(t)
        try:
            detail = url_html.xpath('/html/body/div[2]/div[2]')[0]
            detail_html = etree.tostring(detail, method='HTML')
            detail_html = html.unescape(detail_html.decode()).replace('浏览次数：', '').replace('原文链接', '')
            detail_text = url_html.xpath('string(/html/body/div[2]/div[2])').replace('\xa0', '').replace('\n', ''). \
                replace('\r', '').replace('\t', '').replace(' ', '').replace('\xa5', '')
            if len(detail_text) < 100:
                int('a')
        except:
            try:
                detail = url_html.xpath('//*[@id="JshxrgsDetail1_content"]')[0]
                detail_html = etree.tostring(detail, method='HTML')
                detail_html = html.unescape(detail_html.decode()).replace('浏览次数：', '').replace('原文链接', '')
                detail_text = url_html.xpath('string(//*[@id="JshxrgsDetail1_content"])').replace('\xa0', '').replace('\n', ''). \
                    replace('\r', '').replace('\t', '').replace(' ', '').replace('\xa5', '')
                if len(detail_text) < 100:
                    int('a')
            except:
                detail = url_html.xpath('//*[@id="JszbggDetail1_content"]')[0]
                detail_html = etree.tostring(detail, method='HTML')
                detail_html = html.unescape(detail_html.decode()).replace('浏览次数：', '').replace('原文链接', '')
                detail_text = url_html.xpath('string(//*[@id="JszbggDetail1_content"])').replace('\xa0', '').replace(
                    '\n', ''). \
                    replace('\r', '').replace('\t', '').replace(' ', '').replace('\xa5', '')
                if len(detail_text) < 100:
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
        s = re.findall('<table cellspacing="1".*?</table>', item['body'], re.S)[0]
        item['body'] = item['body'].replace(s, '')
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
        item['resource'] = '南平市公共资源交易网'
        item['shi'] = 7007
        item['sheng'] = 7000
        item['removal']= title
        process_item(item)

    def get_nativeplace(self, addr):
        city = ''
        city_list = [['7007', '南平市'], ['7007.001', '延平区'], ['7007.01', '建阳市'], ['7007.002', '顺昌县'], ['7007.003', '浦城县'], ['7007.004', '光泽县'], ['7007.005', '松溪县'], ['7007.006', '政和县'], ['7007.007', '邵武市'], ['7007.008', '武夷山市'], ['7007.009', '建瓯市']]

        for i in city_list:
            if i[1] in addr:
                city = float(i[0])
                break
        if city == '':
            city = 7004
        return city

if __name__ == '__main__':
    import traceback,os
    try:
        jl = baoshan_ggzy()
        jl.parse()
    except Exception as e:
        traceback.print_exc()
        tool.send_error('报错文件：'+str(os.path.basename(__file__))+'报错信息：'+str(e))



