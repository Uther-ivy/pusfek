# -*- coding: utf-8 -*-
import json
import re
import time, html
import requests
from lxml import etree
from lxml.etree import HTML
import tool
from save_database import process_item


# 平顶山市公共资源交易平台
class pingdingshan_ggzy:
    def __init__(self):
        self.url_list = [
            # 建设工程
            # 招标公告
            'http://www.pdsggzy.com/gzbgg/index_{}.jhtml',
            # 变更公示
            'http://www.pdsggzy.com/gbcgg/index_{}.jhtml',
            # 中标结果
            'http://www.pdsggzy.com/gzbgs/index_{}.jhtml',
            # 政府采购
            # 采购公告
            'http://www.pdsggzy.com/zzbgg/index_{}.jhtml',
            # 变更公告
            'http://www.pdsggzy.com/zbcgg/index_{}.jhtml',
            # 结果公告
            'http://www.pdsggzy.com/zzbgs/index_{}.jhtml'
        ]
        self.url = self.url_list.pop(0)
        self.headers = {
            'Cookie': 'clientlanguage=zh_CN; __51cke__=; __tins__18972454=%7B%22sid%22%3A%201583802695327%2C%20%22vd%22%3A%207%2C%20%22expires%22%3A%201583806154188%7D; __51laig__=12',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36',
        }

    def parse(self):
        date = tool.date
        # date = '2022-06-01'
        page = 0
        while True:
            page += 1
            text = tool.requests_get_bm(self.url.format(page), self.headers)
            # print(text)
            print('*' * 20, page, '*' * 20)
            html = HTML(text)
            # print(11, text)
            # time.sleep(6666)
            detail = html.xpath('//div[@class="channel_list"]/ul/li')
            # print(detail)
            for li in detail:
                title = li.xpath('./a/@title')[0]
                url = 'http://www.pdsggzy.com' + li.xpath('./a/@href')[0]
                date_Today = li.xpath('./span/text()')[0]
                # print(title, url, date_Today)
                # time.sleep(666)
                if tool.Transformation(date) <= tool.Transformation(date_Today):
                    if tool.removal(title, date):
                        self.parse_detile(title, url, date_Today)
                    else:
                        print('【existence】', url)
                        continue
                else:
                    print('日期不符, 正在切换类型...', date_Today)
                    self.url = self.url_list.pop(0)
                    page = 0

                    break
            if page == 20:
                self.url = self.url_list.pop(0)
                break

    def parse_detile(self, title, url, date):
        print(url)
        url_html = etree.HTML(tool.requests_get_bm(url, self.headers))
        try:
            detail = url_html.xpath('//div[@class="WordSection1"]')[0]
            detail_html = etree.tostring(detail, method='HTML')
            detail_html = html.unescape(detail_html.decode())
            detail_text = url_html.xpath('string(//div[@class="WordSection1"])').replace('\xa0',
                                                                                                        '').replace(
                '\n', ''). \
                replace('\r', '').replace('\t', '').replace(' ', '').replace('\xa5', '')
        except:
            detail = url_html.xpath('//div[@class="WordSection1"]')[0]
            detail_html = etree.tostring(detail, method='HTML')
            detail_html = html.unescape(detail_html.decode())
            detail_text = url_html.xpath('string(//div[@class="WordSection1"])').replace('\xa0',
                                                                                                 '').replace(
                '\n', ''). \
                replace('\r', '').replace('\t', '').replace(' ', '').replace('\xa5', '')
        # print(detail_text)
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
        item['winner'] = tool.get_winner(detail_text)
        item['address'] = tool.get_address(detail_text)
        item['linkman'] = tool.get_linkman(detail_text)
        item['function'] = tool.get_function(detail_text)
        item['resource'] = '平顶山市公共资源交易平台'
        item['shi'] = 8504
        item['sheng'] = 8500
        item['removal'] = title
        # print(item["body"])
        process_item(item)

    def get_nativeplace(self, addr):
        city = ''
        city_list = [['8504.001', '新华区'], ['8504.01', '汝州市'], ['8504.002', '卫东区'], ['8504.003', '石龙区'],
                     ['8504.004', '湛河区'], ['8504.005', '宝丰县'], ['8504.006', '叶县'], ['8504.007', '鲁山县'],
                     ['8504.008', '郏县'], ['8504.009', '舞钢市']]
        for i in city_list:
            if i[1] in addr:
                city = float(i[0])
                break
        if city == '':
            city = 8504
        return city


if __name__ == '__main__':
    import traceback, os
    try:
        jl = pingdingshan_ggzy()
        jl.parse()
    except Exception as e:
        traceback.print_exc()
