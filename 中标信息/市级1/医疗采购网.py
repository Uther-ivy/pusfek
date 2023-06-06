# -*- coding: utf-8 -*-
import json
import re
import time, html
import requests
from lxml import etree
from lxml.etree import HTML
import tool
from save_database import process_item

# 医疗采购网
class baoshan_ggzy:
    def __init__(self):
        self.url_list = [
            'https://www.120bid.com/ajax/latest?t=&status%5B%5D=%E6%8B%9B%E6%A0%87%E7%BB%93%E6%9E%9C&date%5B%5D=2019-01-01&date%5B%5D=2023-04-19&areas%5B%5D=130000&page={}'
        ]
        self.url = self.url_list.pop(0)
        self.headers = {
'Referer': 'https://www.120bid.com/latest.html',
'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36',
'X-Requested-With': 'XMLHttpRequest'


            }

    def parse(self):
        date = tool.date
        # date = '2020-12-17'
        page = 196
        while True:
            page += 1
            url=f'https://www.120bid.com/ajax/latest'
            print(url)
            data={
            't': int(time.time()*1000),
            'status[]': '招标结果',
            'date[]': '2019-01-01',
            'date[]': '2023-04-19',
            # 'areas[]': '130000',
            'page': page
            }
            # data=f't={int(time.time()*1000)}&status%5B%5D=%E6%8B%9B%E6%A0%87%E7%BB%93%E6%9E%9C&date%5B%5D=2023-01-01&date%5B%5D=2023-04-19&areas%5B%5D=130000&page={page}'

            print(data)
            # if page == 1:
            text = tool.requests_post_param(url, self.headers,param=data).replace('\u2022', '')
            print(text)
            # else:
            #     text = tool.requests_get(self.url.format('_' + str(page)), self.headers).replace('\u2022', '')
            print('*' * 20, page, '*' * 20)
            html = json.loads(text)
            detail = html['data']
            for li in detail:
                try:
                    title = li.get('itemRaw').replace('null', '').replace('\n', '').replace('\t', '').replace(' ', '').replace('\r', '')
                    url = li.get('url')

                    date_Today = li.get('dateStr') \
                                     .replace('\n', '').replace('\t', '').replace(' ', '').replace('\r', '')[:10]

                    try:
                        city =re.findall(r'>(\w+)<',li.get('areaName'))
                    except:
                        city = ''
                    if '分钟' in date_Today or '小时' in date_Today or '刚刚' in date_Today:
                        date_Today = time.strftime('%Y-%m-%d', time.localtime(time.time()))
                    url_domain = 'https://www.120bid.com'
                    if 'http' not in url:
                        if '../../' in url:
                            url = url_domain + url[5:]
                        elif '../' in url:
                            url = url_domain + url[2:]
                        elif './' in url:
                            url = url_domain + url[1:]
                        else:
                            url = url_domain + url

                    if '测试' in title:
                        continue
                    print(title, url, date_Today)
                    # time.sleep(666)
                    if tool.Transformation(date) <= tool.Transformation(date_Today):
                        # if tool.removal(title, date):
                            self.parse_detile(title, url, date_Today,city)
                        # else:
                        #     print('【existence】', url)
                        #     continue
                    else:
                        print('日期不符, 正在切换类型', date_Today, self.url)
                        return
                except Exception as e:
                    traceback.print_exc()

    def parse_detile(self, title, url, date,city):
        print(url)
        t = tool.requests_get(url, self.headers)
        url_html = etree.HTML(t)
        detail = url_html.xpath('//*[@id="content"]')[0]
        detail_html = etree.tostring(detail, method='HTML')
        detail_html = html.unescape(detail_html.decode()).replace('浏览次数：', '').replace('原文链接', '')
        detail_text = url_html.xpath('string(//*[@id="content"])').replace('\xa0', '').replace('\n', ''). \
            replace('\r', '').replace('\t', '').replace(' ', '').replace('\xa5', '')
        if len(detail_text) < 300:
            return
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
        item['resource'] = '医疗采购网'
        item['sheng'] = tool.get_sheng(city)
        item['nativeplace'] = tool.get_title_city(item['title'])
        if item['nativeplace'] == 0:
            item['nativeplace'] = tool.get_title_city(item['title']+detail_text)
        if len(str(item['sheng'])) == 4:
            if str(item['nativeplace'])[:2] != str(item['sheng'])[:2]:
                item['nativeplace'] = item['sheng']
        else:
            if str(item['nativeplace'])[:3] != str(item['sheng'])[:3]:
                item['nativeplace'] = item['sheng']
        item['shi'] = int(str(item['nativeplace']).split('.')[0])
        item['removal']= title
        process_item(item)


if __name__ == '__main__':
    import traceback,os
    try:
        jl = baoshan_ggzy()
        jl.parse()
    except Exception as e:
        traceback.print_exc()



