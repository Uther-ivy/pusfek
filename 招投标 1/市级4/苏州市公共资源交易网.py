# -*- coding: utf-8 -*-
import json
import re
import time, html
import requests
from lxml import etree
from lxml.etree import HTML
import tool,random
from save_database import process_item

# 苏州市公共资源交易网
class baoshan_ggzy:
    def __init__(self):
        self.url_list = [
            'http://www.szzyjy.com.cn:8086/jyxx/003001/003001001/{}.html',
        ]
        self.url1='http://www.szzyjy.com.cn:8086/jyxx/003001/003001001/tradeInfo.html'
        self.url = self.url_list.pop(0)
        self.headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36'}
    def parse(self):
        date = tool.date
        # date = '2020-07-10'
        page = 0
        while True:
            page += 1
            if page == 1:
                text = tool.requests_get(self.url1, self.headers)
            else:
                text = tool.requests_get(self.url.format(page),self.headers)
            print('-' * 50, page)
            html = HTML(text)
            detail = html.xpath('//table[@class="ewb-trade-tb"]//tr[@class="ewb-trade-tr"]')
            for li in detail:
                title = li.xpath('./td[3]/a/@title')[0]
                date_Today = li.xpath('./td[5]/text()')[0].replace(' ', '').replace('\n', '').replace('\r', '')
                href = li.xpath('./td[3]/a/@href')[0]
                url = 'http://www.szzyjy.com.cn:8086' + href
                if '发布' in date_Today:
                    continue
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
                    self.url = self.url_list.pop(0)
                    break
            if page == 20:
                self.url = self.url_list.pop(0)
                break

    def parse_detile(self, title, url, date):
        t = tool.requests_get(url, self.headers)
        if '抱歉，系统发生了错误！' in t:
            print('抱歉，系统发生了错误！')
            return
        url_html = etree.HTML(t)
        # try:
        detail = url_html.xpath('//div[@class="con"]/table')[0]
        detail_html = etree.tostring(detail, method='HTML')
        detail_html = html.unescape(detail_html.decode()).replace('\xa0', '').replace('\ufeff', '')
        detail_text = ''.join(url_html.xpath('//div[@class="con"]/table//text()')) \
            .replace('\xa0', '').replace('\n', '').replace('\r', '').replace('\t', '') \
            .replace(' ', '').replace('\xa5', '').replace('\ufeff', '')

        item = {}
        item['title'] = title.replace('\u2022', '')
        item['url'] = url
        item['date'] = date
        item['typeid'] = tool.get_typeid(item['title'])
        item['senddate'] = int(time.time())
        item['mid'] = 867
        item['infotype'] = tool.get_infotype(item['title'])
        item['body'] = tool.qudiao_width(detail_html)
        # print(item['body'])
        # time.sleep(666)
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
        item['nativeplace'] = tool.get_title_city(item['title'])
        if item['nativeplace'] == 0:
            item['nativeplace'] = tool.more(item['title'] + detail_text)
        item['linkman'] = tool.get_linkman(detail_text)
        item['function'] = tool.get_function(detail_text)
        item['resource'] = '苏州市公共资源交易网'
        item["shi"] = int(str(item["nativeplace"]).split('.')[0])
        if len(str(int(item["shi"]))) == 4:
            item['sheng'] = int(str(item["shi"])[:2] + '00')
        elif len(str(int(item["shi"]))) == 5:
            item['sheng'] = int(str(item["shi"])[:3] + '00')
        else:
            item['sheng'] = 0
        item['removal'] = title
        process_item(item)
        # print(item['body'])

if __name__ == '__main__':
    import traceback, os
    try:
        jl = baoshan_ggzy()
        jl.parse()
    except Exception as e:
        traceback.print_exc()
        tool.send_error('报错文件：'+str(os.path.basename(__file__))+'报错信息：'+str(e))


