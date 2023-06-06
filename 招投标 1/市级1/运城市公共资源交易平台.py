# -*- coding: utf-8 -*-
import json
import re
import time, html
import requests
from lxml import etree
from lxml.etree import HTML
import tool
from save_database import process_item

# 运城市公共资源交易平台
class yuncheng_ggzy:
    def __init__(self):
        self.url_list = [
            'http://ggzyjyzx.yuncheng.gov.cn/jyxxgc/index_{}.jhtml',
            'http://ggzyjyzx.yuncheng.gov.cn/jyxxzc/index_{}.jhtml',
        ]
        self.url = self.url_list.pop(0)
        self.headers = {
            'Cookie': 'clientlanguage=zh_CN; JSESSIONID=C297BEFA1F2625BB43E55B3FADE65E92',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36',
        }

    def parse(self):
        date = tool.date
        # date = '2020-01-20'
        page = 0
        while True:
            page += 1
            text = tool.requests_get(self.url.format(page), self.headers)
            print('*' * 20, page, '*' * 20)
            html = HTML(text)
            # print(11, text)
            # time.sleep(6666)
            detail = html.xpath('//*[@class="cs_two_content"]/a')
            for li in detail:
                title = li.xpath('./p[1]/text()')[0].replace('\r', '').replace('\n', '').replace('\t', '').replace(' ', '')
                url = 'http://ggzyjyzx.yuncheng.gov.cn' + li.xpath('./@href')[0]
                date_Today = li.xpath('./p[2]/span[2]/text()')[0].replace('/', '-')
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

                    return
            if page == 20:
                self.url = self.url_list.pop(0)
                break

    def parse_detile(self, title, url, date):
        print(url)
        url_html = etree.HTML(tool.requests_get(url, self.headers))
        try:
            detail = url_html.xpath('//*[@class="gycq-table"]')[0]
            detail_html = etree.tostring(detail, method='HTML')
            detail_html = html.unescape(detail_html.decode())
            detail_text = url_html.xpath('string(//*[@class="gycq-table"])').replace('\xa0', '').replace('\n', '').\
                replace('\r', '').replace('\t', '').replace(' ', '').replace('\xa5', '')
        except:
            detail = url_html.xpath('//*[@class="cs_xq_content"]')[0]
            detail_html = etree.tostring(detail, method='HTML')
            detail_html = html.unescape(detail_html.decode())
            detail_text = url_html.xpath('string(//*[@class="cs_xq_content"])').replace('\xa0', '').replace('\n', ''). \
                replace('\r', '').replace('\t', '').replace(' ', '').replace('\xa5', '')
        # print(detail_html)
        item = {}
        item['title'] = title.replace('\u2022', '')
        item['url'] = url
        item['date'] = date
        item['typeid'] = tool.get_typeid(item['title'])
        item['senddate'] = int(time.time())
        item['mid'] = 867
        item['nativeplace'] = self.get_nativeplace(item['title'])
        item['infotype'] = tool.get_infotype(item['title'])
        item['body']= tool.qudiao_width(detail_html)
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
        item['resource'] = '运城市公共资源交易平台'
        item['shi'] = 2508
        item['sheng'] = 2500
        item['removal']= title
        process_item(item)

    def get_nativeplace(self, addr):
        city = ''
        city_list = [['2508.001', '盐湖区'], ['2508.01', '平陆县'], ['2508.011', '芮城县'], ['2508.012', '永济市'], ['2508.013', '河津市'], ['2508.002', '临猗县'], ['2508.003', '万荣县'], ['2508.004', '闻喜县'], ['2508.005', '稷山县'], ['2508.006', '新绛县'], ['2508.007', '绛县'], ['2508.008', '垣曲县'], ['2508.009', '夏县']]
        for i in city_list:
            if i[1] in addr:
                city = float(i[0])
                break
        if city == '':
            city = 2508
        return city

if __name__ == '__main__':
    import traceback, os
    try:
        jl = yuncheng_ggzy()
        jl.parse()
    except Exception as e:
        traceback.print_exc()
        # tool.send_error('报错文件：'+str(os.path.basename(__file__))+'报错信息：'+str(e))

