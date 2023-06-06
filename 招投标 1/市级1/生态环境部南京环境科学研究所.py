# -*- coding: utf-8 -*-
import json
import re
import time, html
import requests
from lxml import etree
from lxml.etree import HTML
import tool
from save_database import process_item

# 生态环境部南京环境科学研究所
class baoshan_ggzy:
    def __init__(self):
        self.url_list = [
            'https://www.nies.org/xwyl/tzgg/index{}.html'
        ]
        self.url = self.url_list.pop(0)
        self.headers = {
            'Cookie': 'Hm_lvt_40ceb75c1dee2b74e07241cc4755bd5b=1629181282; Hm_lvt_82a29b710c5d9be09d3e792652635959=1629181282; Hm_lpvt_82a29b710c5d9be09d3e792652635959=1629181850; Hm_lpvt_40ceb75c1dee2b74e07241cc4755bd5b=1629181850',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36',
        }

    def parse(self):
        date = tool.date
        # date = '2021-08-02'
        page = 0
        while True:
            page += 1
            if page == 1:
                text = tool.requests_get(self.url.format(''), self.headers).replace('\u2022', '')
            else:
                text = tool.requests_get(self.url.format('_'+str(page-1)), self.headers).replace('\u2022', '')
            print('*' * 20, page, '*' * 20)
            html = HTML(text)
            detail = html.xpath('//*[@class="sub_rli"]/li')
            for li in detail:
                title = li.xpath('./a/text()')[0].replace('\n', '').replace('\t', '').replace(' ', '').replace('\r', '')
                url = li.xpath('./a/@href')[0]
                url_domain = 'https://www.nies.org/xwyl/tzgg'
                if 'http' not in url:
                    if '../../' in url:
                        url = url_domain + url[5:]
                    elif '../' in url:
                        url = url_domain + url[2:]
                    elif './' in url:
                        url = url_domain + url[1:]
                    else:
                        url = url_domain + url
                date_Today = li.xpath('./span/text()')[0]\
                    .replace('\n', '').replace('\t', '').replace(' ', '').replace('\r', '').replace('[', '').replace(']', '')
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
                    return


    def parse_detile(self, title, url, date):
        print(url)
        t = tool.requests_get(url, self.headers)
        url_html = etree.HTML(t)
        detail = url_html.xpath('//*[@class="TRS_Editor"]')[0]
        detail_html = etree.tostring(detail, method='HTML')
        detail_html = html.unescape(detail_html.decode()).replace('浏览次数：', '').replace('原文链接', '')
        detail_text = url_html.xpath('string(//*[@class="TRS_Editor"])').replace('\xa0', '').replace('\n', ''). \
            replace('\r', '').replace('\t', '').replace(' ', '').replace('\xa5', '')
        item = {}
        item['title'] = title.replace('\u2022', '')
        item['url'] = url
        item['date'] = date
        item['typeid'] = tool.get_typeid(item['title'])
        item['senddate'] = int(time.time())
        item['mid'] = 867
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
        item['winner'] = tool.get_winner(detail_text)
        item['address'] = tool.get_address(detail_text)
        item['linkman'] = tool.get_linkman(detail_text)
        item['function'] = tool.get_function(detail_text)
        item['resource'] = '生态环境部南京环境科学研究所'
        item['sheng'] = 5500
        item['nativeplace'] = self.get_nativeplace(title)
        item['shi'] = 5501
        item['removal']= title
        process_item(item)

    def get_nativeplace(self, addr):
        city = ''
        city_list = [['5501.001', '武区'], ['5501.01', '江宁区'], ['5501.011', '六合区'], ['5501.012', '溧水县'], ['5501.013', '高淳县'], ['5501.002', '白下区'], ['5501.003', '秦淮区'], ['5501.004', '建邺区'], ['5501.005', '鼓楼区'], ['5501.006', '下关区'], ['5501.007', '浦口区'], ['5501.008', '栖霞区'], ['5501.009', '雨花台区']]

        for i in city_list:
            if i[1] in addr:
                city = float(i[0])
                break
        if city == '':
            city = 5501
        return city

if __name__ == '__main__':
    import traceback,os
    try:
        jl = baoshan_ggzy()
        jl.parse()
    except Exception as e:
        traceback.print_exc()



