# -*- coding: utf-8 -*-
import json
import re
import time, html
import requests
from lxml import etree
from lxml.etree import HTML
import tool
from save_database import process_item

# 中国电建设备物资集中采购平台
class xinyang_ggzy:
    def __init__(self):
        self.url_list = [
            # 'https://ec.powerchina.cn/zgdjcms/category/bulletinList.html?searchDate=1995-07-21&dates=300&word=&categoryId=2&tabName=&startPublishDate=&endPublishDate=&page={}',
            # 'https://ec.powerchina.cn/zgdjcms/category/bulletinList.html?searchDate=1995-07-21&dates=300&word=&categoryId=3&tabName=&startPublishDate=&endPublishDate=&page={}',
            # 'https://ec.powerchina.cn/zgdjcms/category/bulletinList.html?searchDate=1995-07-21&dates=300&word=&categoryId=5&tabName=&startPublishDate=&endPublishDate=&page={}'
            'https://ec.powerchina.cn/zgdjcms/category/bulletinList.html?dates=300&categoryId=4&tabName=&purType=%E8%AE%BE%E5%A4%87%E7%B1%BB&page={}'
        ]
        self.url = self.url_list.pop(0)
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36',
        }

    def parse(self):
        date = tool.date
        # date = '2020-07-10'
        page = 1700
        while True:
            page += 1
            text = tool.requests_get(self.url.format(page), self.headers)
            # print(11, text)
            # time.sleep(666)
            html = HTML(text)
            print('*' * 20, page, '*' * 20)
            detail = html.xpath('//*[@id="bulletinList"]/li')
            for li in detail:
                try:
                    try:
                        title = li.xpath('./a/@title')[0].replace('\xa0', '').replace(' ', '')
                        url = 'https:' + \
                              li.xpath('./a/@href')[0]
                        date_Today = li.xpath('./a/div/div/text()')[0].replace('月', '-').replace('日', '').replace('\n',
                                                                                                                  '').replace(
                            '\t', '').replace('年', '-')
                    except:
                        continue
                    # print(title, url, date_Today)
                    # time.sleep(666)
                    if '测试' in title:
                        continue
                    if tool.Transformation(date) <= tool.Transformation(date_Today):
                        if tool.removal(title, date):
                            self.parse_detile(title, url, date_Today)
                        else:
                            print('【existence】', url)
                            continue
                    else:
                        print('日期不符, 正在切换类型', date_Today)
                        return
                except Exception:
                    traceback.print_exc()

    def parse_detile(self, title, url, date):
        print(url)
        t = tool.requests_get(url, self.headers)
        # print(t)
        u = 'https:'+re.findall('<iframe\s*id="pdfContainer"\s*src="(.*?)"\s*width=', t)[0].replace('(', '').replace(')', '').replace("'", '')
        detail_html = '''<embed style="width: 100%; height: 1060px; display: block" src='{}'> </embed>'''.format(u)
        print(detail_html)
        # print(detail_text.replace('\xa0','').replace('\xa5',''))
        # time.sleep(6666)
        item = {}
        item['title'] = title.replace('\u2022', '')
        item['url'] = url
        item['date'] = date
        item['typeid'] = tool.get_typeid(item['title'])
        item['senddate'] = int(time.time())
        item['mid'] = 867
        item['infotype'] = tool.get_infotype(item['title'])
        item['body'] = tool.qudiao_width(detail_html)
        # print(detail_html)
        # time.sleep(666)
        item['endtime'] = 0
        item['tel'] = 0
        item['email'] = ''
        item['winner'] = tool.get_winner(detail_html)
        item['address'] = ''
        item['nativeplace'] = tool.get_title_city(item['title'])
        if item['nativeplace'] == 0:
            item['nativeplace'] = tool.more(item['title']+detail_html)
        item['linkman'] = ''
        item['function'] = 0
        item['resource'] = '中国电建设备物资集中采购平台'
        item["shi"] = int(str(item["nativeplace"]).split('.')[0])
        if len(str(int(item["shi"]))) == 4:
            item['sheng'] = int(str(item["shi"])[:2] + '00')
        elif len(str(int(item["shi"]))) == 5:
            item['sheng'] = int(str(item["shi"])[:3] + '00')
        else:
            item['sheng'] = 0
        item['removal']= title
        process_item(item)
        # print(item['body'])


if __name__ == '__main__':
    import traceback,os
    try:
        jl = xinyang_ggzy()
        jl.parse()
    except Exception as e:
        traceback.print_exc()
