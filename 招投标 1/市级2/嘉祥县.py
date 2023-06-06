# -*- coding: utf-8 -*-
import json
import re
import time, html
import requests
from lxml import etree
from lxml.etree import HTML
import tool
from save_database import process_item

# 嘉祥县公共资源交易网
class baoshan_ggzy:
    def __init__(self):
        self.url_list = [
            '503000',
            '503002',
            '511001',
            '513001',
            '517001',
            '551001',
            '552001',
            '553001'
                         ]
        self.url = self.url_list.pop(0)
        self.headers = {
            'Accept': 'application/json, text/javascript, */*; q=0.01',
            # 'Public-X-XSRF-TOKEN': 'efcQ0FKM9xPdZmc9tm7XfPpzNhCbTRI0Aq41f7j8GxkwvGme9kT_uzC1OqTJL7G-RZVRmLrT77RzTwWxHhxhdpFDl9rH4DTkoXwS6-Yjqdg1',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.75 Safari/537.36',
        }

    def parse(self):
        date = tool.date
        # date = '2021-04-19'
        page = 0
        url_ = 'https://jnggzy.jnzbtb.cn:4430/api/services/app/stPrtBulletin/GetBulletinList'
        while True:
            data = {"skipCount":0,"maxResultCount":20,"categoryCode":self.url,"includeAllSite":True,"FilterText":"","tenantId":"3","regionId":"0","tenderProjectType":""}
            page += 1
            text = tool.requests_post_to(url_, data, self.headers)
            print('*' * 20, page, '*' * 20)
            detail = json.loads(text)['result']['items']
            for li in detail:
                title = li['title'].replace('\n', '').replace('\r', '')\
                    .replace('\t', '').replace(' ', '')
                url = li['id']
                if 'http' not in url:
                    # 'http://jnggzy.jnzbtb.cn/JiaXiang/Bulletins/Detail/b2bb4a12-689a-af6a-1d9d-39fbfb1f413b/?CategoryCode=503000'
                    url = 'http://jnggzy.jnzbtb.cn/JiaXiang/Bulletins/Detail/{}/?CategoryCode={}'.format(url, self.url)
                date_Today = li['releaseDate'][:10].replace('\n', '').replace('\r', '') \
                    .replace('\t', '').replace(' ', '').replace('(', '').replace(')', '').replace('.', '-')\
                    .replace('[', '').replace(']', '')
                if '测试' in title:
                    continue
                # print(title, url, date_Today)
                # time.sleep(666)
                if tool.Transformation(date_Today) >= tool.Transformation(date):
                    if tool.removal(title, date):
                        self.parse_detile(title, url, date_Today)
                    else:
                        print('【existence】', url)
                        continue
                else:
                    print('日期不符, 正在切换类型', date_Today, self.url)
                    self.url = self.url_list.pop(0)
                    print(self.url)
                    page = 0
                    break
            if page == 20:
                self.url = self.url_list.pop(0)
                break

    def parse_detile(self, title, url, date):
        print(url)
        t = tool.requests_get(url, self.headers)
        url_html = etree.HTML(t)
        detail = url_html.xpath('//*[@id="ctn-detail"]')[0]
        detail_html = etree.tostring(detail, method='HTML')
        detail_html = html.unescape(detail_html.decode())
        detail_text = url_html.xpath('string(//*[@id="ctn-detail"])').replace('\xa0', '').replace('\n',
                                                                                                     ''). \
            replace('\r', '').replace('\t', '').replace(' ', '').replace('\xa5', '')

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
        item['resource'] = '嘉祥县公共资源交易网'
        item['shi'] = 8007
        item['sheng'] = 8000
        # print(item)
        item['removal']= title
        process_item(item)

    def get_nativeplace(self, addr):
        city = ''
        city_list = [['8007.001', '市中区'], ['8007.01', '曲阜市'], ['8007.011', '兖州市'], ['8007.012', '邹城市'], ['8007.002', '任城区'], ['8007.003', '微山县'], ['8007.004', '鱼台县'], ['8007.005', '金乡县'], ['8007.006', '嘉祥县'], ['8007.007', '汶上县'], ['8007.008', '泗水县'], ['8007.009', '梁山县']]

        for i in city_list:
            if i[1] in addr:
                city = float(i[0])
                break
        if city == '':
            city = 8007
        return city

if __name__ == '__main__':
    import traceback, os
    try:
        jl = baoshan_ggzy()
        jl.parse()
    except Exception as e:
        traceback.print_exc()
