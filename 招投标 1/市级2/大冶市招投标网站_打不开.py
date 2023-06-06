# -*- coding: utf-8 -*-
import json
import re
import time, html
import requests
from lxml import etree
from lxml.etree import HTML
import tool
from save_database import process_item

# 大冶市招投标网站
class baoshan_ggzy:
    def __init__(self):
        self.url_list = [
            'http://111.4.115.225:8010/ztb/jyxx/001001/001001001/threeLevel.html',
            'http://111.4.115.225:8010/ztb/jyxx/001001/001001002/threeLevel.html',
            'http://111.4.115.225:8010/ztb/jyxx/001001/001001003/threeLevel.html',
            'http://111.4.115.225:8010/ztb/jyxx/001001/001001004/threeLevel.html',
            'http://111.4.115.225:8010/ztb/jyxx/001001/001001005/threeLevel.html',
        ]
        self.url = self.url_list.pop(0)
        self.headers = {
            # 'Cookie': 'homeid=1a444a31-e460-47ff-9931-1c075c0f3cd8',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36',
        }

    def parse(self):
        while True:
            date = tool.date
            # date='2021-04-12'
            text = tool.requests_get(self.url,self.headers)
            # print(text)
            html = HTML(text)
            detail = html.xpath('//ul[@class="wb-data-item"]//li')
            for li in range(len(detail)):
                url = html.xpath(f'(//ul[@class="wb-data-item"]//li//a//@href)[{li+1}]')[0]
                title = html.xpath(f'(//ul[@class="wb-data-item"]//li//a//text())[{li+1}]')[0].strip()

                date_Today = html.xpath(f'(//ul[@class="wb-data-item"]//li//span//text())[{li+1}]')[0]
                print(date_Today)

                # print(li+1,url,title,date_Today)
                if '发布' in date_Today:
                    continue
                # month=re.findall('(\d*)-\d*-\d*',date_Today)
                # day=re.findall('\d*-(\d*)-\d*',date_Today)
                # print(month,day)
                if '测试' in title:
                    continue
                # urls=re.findall("(.*?)\(\'(.*?)\'\)",url)[0]
                url="http://111.4.115.225:8010"+url
                print(title, url, date_Today)
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
                    break


    def parse_detile(self, title, url, date):
        t = tool.requests_get(url, self.headers)
        url_html = etree.HTML(t)
        detail = url_html.xpath('//div[@class="ewb-detail-text"]')[0]
        # print(detail)
        detail_html = etree.tostring(detail, method='HTML')
        detail_html = html.unescape(detail_html.decode())
        detail_text = url_html.xpath('string(//div[@class="ewb-detail-text"])').replace('\xa0', '').replace('\n', ''). \
            replace('\r', '').replace('\t', '').replace(' ', '').replace('\xa5', '')
        # if len(detail_text) < 100:
        #     return
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
        item['nativeplace'] = 9002.006
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
        item['resource'] = '大冶市招投标网站'
        item["shi"] = 9002
        item['sheng'] = 9000
        # print(item)
        item['removal']= title
        process_item(item)

    def get_nativeplace(self, addr):
        city = ''
        city_list = [['2502.001', '南郊区'], ['2502.01', '城区'], ['2502.011', '矿区'], ['2502.012', '南郊区'], ['2502.002', '新荣区'], ['2502.003', '阳高县'], ['2502.004', '天镇县'], ['2502.005', '广灵县'], ['2502.006', '灵丘县'], ['2502.007', '浑源县'], ['2502.008', '左云县'], ['2502.009', '大同县']]

        for i in city_list:
            if i[1] in addr:
                city = float(i[0])
                break
        if city == '':
            city = 2502
        return city

if __name__ == '__main__':

    import traceback, os
    try:
        jl = baoshan_ggzy()
        jl.parse()
    except Exception as e:
        traceback.print_exc()
