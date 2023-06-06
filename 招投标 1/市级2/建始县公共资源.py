# -*- coding: utf-8 -*-
import json
import re
import time, html
import requests
from lxml import etree
from lxml.etree import HTML
import tool
from save_database import process_item

# 建始县公共资源
class baoshan_ggzy:
    def __init__(self):
        self.url_list = [
            'http://js.eszggzy.cn/jsweb/jyxx/070001/070001001/',
            'http://js.eszggzy.cn/jsweb/jyxx/070001/070001002/',
            'http://js.eszggzy.cn/jsweb/jyxx/070001/070001003/',
            'http://js.eszggzy.cn/jsweb/jyxx/070002/070002001/',
            'http://js.eszggzy.cn/jsweb/jyxx/070002/070002002/',
            'http://js.eszggzy.cn/jsweb/jyxx/070002/070002003/',
            'http://js.eszggzy.cn/jsweb/jyxx/070003/070003001/',
            'http://js.eszggzy.cn/jsweb/jyxx/070003/070003003/',
            'http://js.eszggzy.cn/jsweb/jyxx/070004/070004001/',
            'http://js.eszggzy.cn/jsweb/jyxx/070004/070004002/',
            'http://js.eszggzy.cn/jsweb/jyxx/070004/070004003/',

        ]
        self.url = self.url_list.pop(0)
        self.headers = {
            # 'Cookie': 'homeid=1a444a31-e460-47ff-9931-1c075c0f3cd8',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36',
        }
    def Transformation(self,date):
        """日期转时间戳"""
        timeArray = time.strptime(date, "%b %d %Y")
        timeStamp = int(time.mktime(timeArray))
        return timeStamp

    def parse(self):
        while True:
            date = tool.date
            # date='2021-07-27'
            text = tool.requests_get(self.url,self.headers)
            # print(text)
            html = HTML(text)
            detail = html.xpath('//tr[@class="trfont"]')

            # print(de)
            for li in range(len(detail)):
                # print(html.xpath('(//table[@id="dataTable"]//tr//@id)[1]'))
                url= html.xpath(f'(//tr[@class="trfont"]//a//@href)[{li+1}]')[0]
                # urls_=re.findall("view\('(.*?)','(.*?)'\);",urls)
                # print(urls_)
                title = ''.join(html.xpath(f'(//tr[@class="trfont"]//a//text())[{li+1}]')).strip()
                #
                date_Today = html.xpath(f'(//tr[@class="trfont"]//span//text())[{li+1}]')[0].strip()
                # print(li+1,url,title,date_Today)
                if '发布' in date_Today:
                    continue
                # month=re.findall('(\d*)-\d*-\d*',date_Today)
                # day=re.findall('\d*-(\d*)-\d*',date_Today)
                # print(month,day)
                if '测试' in title:
                    continue
                # urls=re.findall("(.*?)\(\'(.*?)\'\)",url)[0]
                url='http://js.eszggzy.cn'+url
                # print(title, url, date_Today)
                # # time.sleep(666)
                if tool.Transformation(date) <= tool.Transformation(date_Today):
                    if tool.removal(title, date):
                        self.parse_detile(title, url, date_Today)
                    else:
                        print('【existence】', url)
                        continue
                else:
                    # print(tool.Transformation(date),self.Transformation(date_Today))
                    print('日期不符, 正在切换类型', date_Today, self.url)
                    self.url = self.url_list.pop(0)
                    page = 0
                    continue
            self.url = self.url_list.pop(0)

    def parse_detile(self, title, url, date):
        print(url)
        t = tool.requests_get(url, self.headers)
        url_html = etree.HTML(t)
        detail = url_html.xpath('//td[@class="infodetail"]')[0]
        # print(detail)
        detail_html = etree.tostring(detail, method='HTML')
        detail_html = html.unescape(detail_html.decode())
        detail_text = url_html.xpath('string(//td[@class="infodetail"])').replace('\xa0', '').replace('\n', ''). \
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
        item['nativeplace'] = 9013.003
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
        item['resource'] = '建始县公共资源'
        item["shi"] = 9013
        item['sheng'] = 9000
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
