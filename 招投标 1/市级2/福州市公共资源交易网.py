# -*- coding: utf-8 -*-
import json
import re
import time, html
import requests
from lxml import etree
from lxml.etree import HTML
import tool
from save_database import process_item

# 福州市公共资源交易网
class baoshan_ggzy:
    def __init__(self):
        self.url_list = [
            'http://fzsggzyjyfwzx.cn/jyxxzbgg/index_{}.jhtml', 'http://fzsggzyjyfwzx.cn/jyxxgcbc/index_{}.jhtml',
            'http://fzsggzyjyfwzx.cn/jyxxkbjl/index_{}.jhtml', 'http://fzsggzyjyfwzx.cn/jyxxzsjg/index_{}.jhtml',
            'http://fzsggzyjyfwzx.cn/jyxxzbgs/index_{}.jhtml', 'http://fzsggzyjyfwzx.cn/jyxxcggg/index_{}.jhtml',
            'http://fzsggzyjyfwzx.cn/jyxxgzsx/index_{}.jhtml', 'http://fzsggzyjyfwzx.cn/jyxxcjgg/index_{}.jhtml'
        ]
        self.url = self.url_list.pop(0)
        self.headers = {
            'Cookie': 'homeid=1a444a31-e460-47ff-9931-1c075c0f3cd8',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36',
        }

    def parse(self):
        date = tool.date
        # date = '2020-12-17'
        page = 0
        while True:
            page += 1
            if page == 1:
                text = tool.requests_get(self.url.format('about-trade'), self.headers)
            else:
                text = tool.requests_get(self.url.format(page), self.headers)
            print('*' * 20, page, '*' * 20)
            html = HTML(text)
            # print(11, text)
            # time.sleep(6666)
            detail = html.xpath('/html/body/div[1]/div[4]/div[3]/div/ul/li')
            for li in detail:
                title = li.xpath('string(./div/a)').replace('\n', '').replace('\t', '').replace(' ', '')
                url = li.xpath('./div/a/@href')[0]
                date_Today = li.xpath('./div/div/text()')[0].replace('\n', '').replace('\t', '').replace(' ', '')
                if '测试' in title:
                    continue
                url_domain = 'http://fzsggzyjyfwzx.cn'
                if 'http' not in url:
                    if '../../' in url:
                        url = url_domain + url[5:]
                    elif '../' in url:
                        url = url_domain + url[2:]
                    elif './' in url:
                        url = url_domain + url[1:]
                    else:
                        url = url_domain + url
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
            detail = url_html.xpath('//*[@class="Section1"]')[0]
            detail_html = etree.tostring(detail, method='HTML')
            detail_html = html.unescape(detail_html.decode())
            detail_text = url_html.xpath('string(//*[@class="Section1"])').replace('\xa0', '').replace('\n', ''). \
                replace('\r', '').replace('\t', '').replace(' ', '').replace('\xa5', '')
            if len(detail_text) < 100:
                print(detail_text)
                return
        except:
            detail = url_html.xpath('//*[@id="content"]')[0]
            detail_html = etree.tostring(detail, method='HTML')
            detail_html = html.unescape(detail_html.decode())
            detail_text = url_html.xpath('string(//*[@id="content"])').replace('\xa0', '').replace('\n', ''). \
                replace('\r', '').replace('\t', '').replace(' ', '').replace('\xa5', '')
            if len(detail_text) < 100:
                print(detail_text)
                return
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
        item['resource'] = '福州市公共资源交易网'
        item['shi'] = 7001
        item['sheng'] = 7000
        item['removal']= title
        process_item(item)

    def get_nativeplace(self, addr):
        city = ''
        city_list = [['7001.001', '鼓楼区'], ['7001.01', '永泰县'], ['7001.011', '平潭县'], ['7001.012', '福清市'], ['7001.013', '长乐市'], ['7001.002', '台江区'], ['7001.003', '仓山区'], ['7001.004', '马尾区'], ['7001.005', '晋安区'], ['7001.006', '闽侯县'], ['7001.007', '连江县'], ['7001.008', '罗源县'], ['7001.009', '闽清县']]

        for i in city_list:
            if i[1] in addr:
                city = float(i[0])
                break
        if city == '':
            city = 7001
        return city

if __name__ == '__main__':
    import traceback, os
    try:
        jl = baoshan_ggzy()
        jl.parse()
    except Exception as e:
        traceback.print_exc()
        tool.send_error('报错文件：'+str(os.path.basename(__file__))+'报错信息：'+str(e))


