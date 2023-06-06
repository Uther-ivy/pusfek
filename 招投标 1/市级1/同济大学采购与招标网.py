# -*- coding: utf-8 -*-
import json
import re
import time, html
import requests
from lxml import etree
from lxml.etree import HTML
import tool
from save_database import process_item

# 同济大学采购与招标网
class baoshan_ggzy:
    def __init__(self):
        self.url_list = [
            'https://czb.tongji.edu.cn/sggl/cgw/zbggList.jsp?type=B',

        ]
        self.url = self.url_list.pop(0)
        self.headers = {
            # 'Cookie': 'homeid=1a444a31-e460-47ff-9931-1c075c0f3cd8',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36',
        }

    def parse(self):
        while True:
            date = tool.date
            # date='2021-04-20'
            text = tool.requests_get(self.url,self.headers)
            # print(text)
            html = HTML(text)
            detail = html.xpath('//div[@class="main_list"]//li')
            for li in detail:
                href = li.xpath('.//a/@href')[0]
                url = f"https://czb.tongji.edu.cn/sggl/cgw/{href}"
                title =li.xpath('.//a/text()')[0]
                date1 = li.xpath('.//text()')[1]
                date2 = li.xpath('.//text()')[2]
                date3 = li.xpath('.//text()')[0]
                date_Today = date1 + '-' + date2 + '-' + date3
                if '发布' in date_Today:
                    continue
                if '测试' in title:
                    continue
                print(title, url, date_Today)
                # # time.sleep(666)
                if tool.Transformation(date) <= tool.Transformation(date_Today):
                    if tool.removal(title, date):
                        self.parse_detile(title, url, date_Today)
                    else:
                        print('【existence】', url)
                        continue
                else:
                    print('日期不符, 正在切换类型', date_Today, self.url)
                    return

            if detail[:-1]:

                break
            # self.url = self.url_list.pop(0)

    def parse_detile(self, title, url, date):
        print(url)
        t = tool.requests_get(url, self.headers)
        url_html = etree.HTML(t)
        detail = url_html.xpath('//div[@class="artical_text"]')[0]
        # print(detail)
        detail_html = etree.tostring(detail, method='HTML')
        detail_html = html.unescape(detail_html.decode())
        detail_text = url_html.xpath('string(//div[@class="artical_text"])').replace('\xa0', '').replace('\n', ''). \
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
        item['nativeplace'] = 5009
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
        item['resource'] = '同济大学采购与招标网'
        item["shi"] = 5009
        item['sheng'] = 5000
        # print(item)
        item['removal']= title
        process_item(item)

if __name__ == '__main__':
    import traceback, os
    try:
        jl = baoshan_ggzy()
        jl.parse()
    except Exception as e:
        traceback.print_exc()

