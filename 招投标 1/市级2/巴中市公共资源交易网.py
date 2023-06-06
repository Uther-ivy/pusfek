# -*- coding: utf-8 -*-
import json
import re
import time, html
import requests
from lxml import etree
from lxml.etree import HTML
import tool
from save_database import process_item

# 巴中市公共资源交易网
class baoshan_ggzy:
    def __init__(self):
        self.url_list = [
            'http://117.172.156.43:82/pub/showMcontent?mcode=JYGCJS&clicktype=0',
            'http://117.172.156.43:82/pub/showMcontent?mcode=JYZFCG&clicktype=0'
                         ]
        self.url = self.url_list.pop(0)
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.75 Safari/537.36',
        }

    def parse(self):
        date = tool.date
        # date = '2020-08-13'
        page = 0
        while True:
            page += 1
            text = tool.requests_get(self.url, self.headers)
            print('*' * 20, page, '*' * 20)
            detail = json.loads(text)['data']
            for i in detail:
                for li in i['content']:
                    title = li['mctype'].replace('\n', '').replace('\r', '')\
                        .replace('\t', '').replace(' ', '').replace('<spanstyle="color:red">', '').replace('</span>', '')
                    url = 'http://117.172.156.43:82/pub/BZ_indexContent_{}.html'.format(li['id'])
                    if 'http' not in url:
                        url = 'http://117.172.156.43:82' + url
                    date_Today = li['mckeys'].replace('\n', '').replace('\r', '') \
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
                        page = 0
                        break

            self.url = self.url_list.pop(0)
            break

    def parse_detile(self, title, url, date):
        print(url)
        t = tool.requests_get(url, self.headers)
        url_html = etree.HTML(t)
        detail = url_html.xpath('//*[@id="content"]')[0]
        detail_html = etree.tostring(detail, method='HTML')
        detail_html = html.unescape(detail_html.decode())
        detail_text = url_html.xpath('string(//*[@id="content"])').replace('\xa0', '').replace('\n', ''). \
            replace('\r', '').replace('\t', '').replace(' ', '').replace('\xa5', '')
        if len(detail_html) < 300:
            int('a')
        # print(t.replace('\xa0','').replace('\xa5',''))
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
        item['resource'] = '巴中市公共资源交易网'
        item['shi'] = 12017
        item['sheng'] = 12000
        item['removal']= title
        process_item(item)

    def get_nativeplace(self, addr):
        city = ''
        city_list = [['12017.001', '巴州区'], ['12017.002', '通江县'], ['12017.003', '南江县'], ['12017.004', '平昌县']]

        for i in city_list:
            if i[1] in addr:
                city = float(i[0])
                break
        if city == '':
            city = 12017
        return city

if __name__ == '__main__':
    import traceback, os
    try:
        jl = baoshan_ggzy()
        jl.parse()
    except Exception as e:
        traceback.print_exc()
        tool.send_error('报错文件：'+str(os.path.basename(__file__))+'报错信息：'+str(e))


