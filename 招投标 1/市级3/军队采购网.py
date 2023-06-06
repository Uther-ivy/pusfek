# -*- coding: utf-8 -*-
import json
import re
import time, html
import requests
from lxml import etree
from lxml.etree import HTML
import tool
from save_database import process_item

# 玉林市公共资源交易中心
class wenshan_ggzy:
    def __init__(self):
        self.domain_name = 'https://www.plap.cn'
        self.url_list = [

        ]

        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36',

        }

    def parse(self):
        date = tool.date
        # date = '2020-09-27'
        page = 0
        while True:
            page += 1
            url=f'https://www.plap.cn/index/selectAllByTabs.html?page={page}&articleTypeId=1&secondArticleTypeId=2&title=&productType=&productTypeName=&tab=%25E7%2589%25A9%25E8%25B5%2584&lastArticleTypeName=&publishStartDate=&publishEndDate='
            payload = {
                'noticeType':  1,
                'pageSize': 10,
                'pageNo': page,
                'noticeState': 1,
                'isValid': 1,
                'orderBy': 'publish_time desc'

                }
            text = tool.requests_get(url , self.headers)
            print('*' * 20, page, '*' * 20)
            # print(11, text.replace('\ufffd', ' ').replace('\u30fb', ' '))
            # time.sleep(6666)
            html = HTML(text)
            # print(11, text)
            # time.sleep(6666)
            detail = html.xpath("//ul[@class='categories li_square col-md-12 col-sm-12 col-xs-12 p0 list_new']/li")
            for li in detail:
                title = li.xpath('./a/text()')[0].replace('\xa0', '').replace('\n', ''). \
                    replace('\r', '').replace('\t', '').replace(' ', '').replace('\xa5', '')
                url = li.xpath('./a/@href')[0]
                date_Today = li.xpath("./span[@class='col-md-3 col-sm-3 col-xs-6 tc p0']/text()")[0].replace('\xa0', '').replace('\n', ''). \
                    replace('\r', '').replace('\t', '').replace(' ', '').replace('\xa5', '')
                if 'http' not in url:
                    url = self.domain_name + url
                print(title, url, date_Today)
                # time.sleep(666)
                # endtime=re.findall(r'\d{4}-\d{2}-\d{2}', li['endtime'])[0]
                # date_Today = re.findall(r'\d{4}-\d{2}-\d{2}', date_Today)[0]
                if tool.Transformation(date) >= tool.Transformation_zhong(date_Today):
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
                page = 0

    def parse_detile(self, title, url, date):
        print(url)
        url_text = tool.requests_get(url, self.headers)
        url_html = etree.HTML(url_text)
        detail_url = url_html.xpath("//div[@class='clear margin-top-20 new_content']/img/@src")[0]
        # print(url_text)
        if 'http' not in detail_url:
            detail_url = self.domain_name + detail_url
        detail_html = f'<div class="clear margin-top-20 new_content">\n\t \t\n\t \t\n\t\t \t<img src="{detail_url}"  width="100%"  height="100%" />\n\t \t\n\t </div>\n\t '
        detail_html = etree.tostring( etree.HTML(detail_html), method='HTML')
        detail_html = html.unescape(detail_html.decode())
        # detail_html = html.unescape(detail_html.decode())
        detail_text = detail_html
        # if len(detail_html) < 200:
        #     int('a')
        item = {}
        item['title'] = title.replace('\u2022', '')
        item['url'] = url
        item['date'] = date
        item['typeid'] = tool.get_typeid(item['title'])
        item['senddate'] = int(time.time())
        item['mid'] = 867
        item['nativeplace'] = float(tool.get_title_city(title))
        item['infotype'] = tool.get_infotype(item['title'])
        item['body'] = tool.qudiao_width(detail_text)

        item['endtime'] = tool.get_endtime(date)
        if item['endtime'] == '':
            print(date)
            item['endtime'] =date
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
        item['resource'] = '军队采购网'
        item["shi"] = int(item["nativeplace"])
        if len(str(item["nativeplace"])) == 4:
            item['sheng'] = int(str(item["nativeplace"])[:2] + '00')
        elif len(str(item["nativeplace"])) == 5:
            item['sheng'] = int(str(item["nativeplace"])[:3] + '00')
        else:
            item['sheng'] = 0
        item['removal']= title
        process_item(item)
        print(item)


if __name__ == '__main__':
    import traceback,os
    try:
        jl = wenshan_ggzy()
        jl.parse()
    except Exception as e:
        traceback.print_exc()
        tool.send_error('报错文件：'+str(os.path.basename(__file__))+'报错信息：'+str(e))


