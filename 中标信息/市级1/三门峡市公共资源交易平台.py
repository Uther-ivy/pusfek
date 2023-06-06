# -*- coding: utf-8 -*-
import json
import random
import re
import time, html
import requests
from lxml import etree
from lxml.etree import HTML
import tool
from save_database import process_item

# 三门峡市公共资源交易平台
class sanmenxia_ggzy:
    def __init__(self):
        self.url_list = [
            # 'http://gzjy.smx.gov.cn/jyxx/{}.html',
            'http://gzjy.smx.gov.cn/jyxx/001001/001001003/{}'
        ]
        self.url = self.url_list.pop(0)
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36',
        }

    def parse(self):
        date = tool.date
        # date = '2020-02-17'
        page =35
        while True:
            page += 1
            if page == 1:
                # print(self.url)
                text = tool.requests_get(self.url.format('moreinfojy.html'), self.headers)
            else:
                text = tool.requests_get(self.url.format(f'{page}.html'), self.headers)
                if '<!DOCTYPE html>' not in text or (text==''):
                    print('#' * 20, 'channel is  None', '#' * 20)
                    time.sleep(10 + random.random() * 10)
                    text = tool.requests_get(self.url.format(page), self.headers)

            html = HTML(text)
            # print(11, text)
            print('*' * 20, page, '*' * 20)
            # time.sleep(6666)
            detail = html.xpath('//*[@id="infolist1"]/li')
            for li in detail:
                try:
                    title = li.xpath('./div[1]/a/@title')[0]
                    url = 'http://gzjy.smx.gov.cn' + li.xpath('./div[1]/a/@href')[0]
                    date_Today = li.xpath('./span/text()')[0].replace('\r', '').replace('\t', '').replace(' ', '').replace('\n', '')
                    print(title, url, date_Today)
                    # time.sleep(666)
                    if tool.Transformation(date) <= tool.Transformation(date_Today):
                        # print(title)
                        # if tool.removal(title, date):
                            self.parse_detile(title, url, date_Today)
                        # else:
                        #     print('【existence】', url)
                        #     continue
                    else:
                        print('日期不符, 正在切换类型', date_Today, self.url)
                        return
                except Exception:
                    traceback.print_exc()



    def parse_detile(self, title, url, date):
        print(url)
        t=tool.requests_get(url, self.headers)

        url_html = etree.HTML(t)
        detail = url_html.xpath('//*[@class="ewb-article-info"]')[0]

        detail_html = etree.tostring(detail, method='HTML')
        # print(detail_html)
        detail_html = html.unescape(detail_html.decode())
        detail_text = url_html.xpath('string(//*[@class="ewb-article-info"])').replace('\xa0', '').replace('\n', '').\
            replace('\r', '').replace('\t', '').replace(' ', '').replace('\xa5', '')
        # print(detail_text.replace('\xa0','').replace('\xa5',''))
        # time.sleep(6666)
        if len(detail_text) < 300:
            return
        winner=tool.get_winner(detail_text)
        print(winner)
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
        item['winner'] = winner
        item['address'] = tool.get_address(detail_text)
        item['linkman'] = tool.get_linkman(detail_text)
        item['function'] = tool.get_function(detail_text)
        item['resource'] = '三门峡市公共资源交易平台'
        item['shi'] = 8512
        item['sheng'] = 8500
        item['removal']= title
        process_item(item)


    def get_nativeplace(self, addr):
        city = ''
        city_list = [['8512.001', '湖滨区'], ['8512.002', '渑池县'], ['8512.003', '陕县'], ['8512.004', '卢氏县'], ['8512.005', '义马'], ['8512.006', '灵宝']]

        for i in city_list:
            if i[1] in addr:
                city = float(i[0])
                break
        if city == '':
            city = 8512
        return city

if __name__ == '__main__':

    import traceback, os
    try:
        jl = sanmenxia_ggzy()
        jl.parse()
    except Exception as e:
        traceback.print_exc()
        tool.send_error('报错文件：'+str(os.path.basename(__file__))+'报错信息：'+str(e))


