# -*- coding: utf-8 -*-
import json
import time, html
import requests
from lxml import etree
import tool
from save_database import process_item
import io
import sys
# sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf8')

# 大同市公共资源交易中心
class chaoyang_ggzy:
    def __init__(self):
        self.url_ls = [
            'http://ggzyjy.dt.gov.cn/jyxx/index_{}.jhtml',
            'http://ggzyjy.dt.gov.cn/jyxxzc/index_{}.jhtml'
        ]
        self.url = self.url_ls.pop(0)
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36',
            'Accept': '*/*',
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'Origin': 'http://ggzyjy.dt.gov.cn',
            # 'OWASP_CSRFTOKEN': 'MCMY-RMO0-PW7T-M07T-915Z-T1WH-16DC-MVDB',
            # 'Referer': 'http://ggzyjy.dt.gov.cn/zyjyPortal/portal/tradeNoticeNews?category=%E6%94%BF%E5%BA%9C%E9%87%87%E8%B4%AD',
            'X-Requested-With': 'XMLHttpRequest, XMLHttpRequest'
        }

    def parse(self):
        date = tool.date
        # date = '2021-07-26'
        page = 0
        while True:
            page += 1
            text = tool.requests_get(self.url.format(page), self.headers)
            print('*' * 20, page, '*' * 20)
            # print(text)
            # time.sleep(6666)
            # detail = json.loads(text)['rows']
            html = etree.HTML(text)
            detail = html.xpath('//*[@class="cs_two_content"]/a')
            for li in detail:
                title = li.xpath('./p[1]/text()')[0].strip()
                url = li.xpath('./@href')[0]
                date_Today = li.xpath('./p[2]/span[2]/text()')[0].strip().replace('/', '-')
                if 'http' not in url:
                    if '../../' in url:
                        url = '/'.join(self.url.split('/')[:3]) + '/' + url.replace('../', '')
                    elif '../' in url:
                        url = '/'.join(self.url.split('/')[:5]) + '/' + url.replace('../', '')
                    elif url[0] == '/':
                        url = '/'.join(self.url.split('/')[:3]) + url.replace('./', '')
                    else:
                        url = '/'.join(self.url.split('/')[:-1]) + '/' + url.replace('./', '')
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
                    self.url = self.url_ls.pop()
                    page = 0
                    break


    def parse_detile(self, title, url, date):
        print(url)
        url_html = etree.HTML(tool.requests_get(url, self.headers))
        detail = url_html.xpath('//*[@class="gycq-table"]')[0]
        detail_html = etree.tostring(detail, method='HTML')
        detail_html = html.unescape(detail_html.decode())
        detail_text = url_html.xpath('string(//*[@class="gycq-table"])').replace('\xa0', '').replace('\n', '').\
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
        item['resource'] = '大同市公共资源交易中心'
        item['shi'] = 2502
        item['sheng'] = 2500
        item['removal']= title
        process_item(item)

    def get_nativeplace(self, addr):
        city = ''
        city_list = [['2502.001', '南郊区'], ['2502.01', '城区'], ['2502.011', '矿区'], ['2502.012', '南郊区'], ['2502.002', '新荣区'], ['2502.003', '阳高县'], ['2502.004', '天镇县'], ['2502.005', '广灵县'], ['2502.006', '灵丘县'], ['2502.007', '浑源县'], ['2502.008', '左云县'], ['2502.009', '大同县']]

        for i in city_list:
            if i[1] in addr:
                city = float(i[0])
                break
        if city == '':
            city = 2502
        return city

if __name__ == '__main__':

    import traceback, os
    try:
        jl = chaoyang_ggzy()
        jl.parse()
    except Exception as e:
        traceback.print_exc()
