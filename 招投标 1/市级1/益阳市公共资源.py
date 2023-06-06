# -*- coding: utf-8 -*-
import json
import re
import time, html
import requests
from lxml import etree
from lxml.etree import HTML
import tool
from save_database import process_item

# 益阳市公共资源
class baoshan_ggzy:
    def __init__(self):
        self.url_list = [
            'https://yiyang.hnsggzy.com/queryContent-jygk.jspx?title=&origin=&inDates=7&channelId=552&ext=&beginTime=&endTime=',
            'https://yiyang.hnsggzy.com/queryContent-jygk.jspx?title=&origin=&inDates=7&channelId=557&ext=&beginTime=&endTime=',
        ]
        self.url = self.url_list.pop(0)
        self.headers = {
            # 'Cookie': 'homeid=1a444a31-e460-47ff-9931-1c075c0f3cd8',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36',
        }

    def parse(self):
        while True:
            date = tool.date
            # date='2021-07-23'
            print(self.url)
            text = tool.requests_get(self.url,self.headers)
            html = HTML(text)
            detail = html.xpath('//ul[@class="article-list2"]//li')
            for li in range(len(detail)):
                url = html.xpath(f'(//ul[@class="article-list2"]//li//a//@href)[{li+1}]')[0].strip()
                title = ''.join(html.xpath(f'(//ul[@class="article-list2"]//li//div[@class="article-list3-t"])[{li+1}]//text()')).strip().split(" ")[0].replace('\r','').replace('\n','')
                date_Today = html.xpath(f'(//ul[@class="article-list2"]//li//div[@class="list-times"]//text())[{li+1}]')[0].strip()
                # print(li+1,url,title,date_Today)
                if '发布' in date_Today:
                    continue
                if '测试' in title:
                    continue
                # print(title, url, date_Today)
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


    def parse_detile(self, title, url, date):
        print(url)
        t = tool.requests_get(url, self.headers)
        url_html = etree.HTML(t)
        try:
            detail = url_html.xpath('//table[@class="gycq-table"]')[0]
        except:
            return
        # print(detail)
        detail_html = etree.tostring(detail, method='HTML')
        detail_html = html.unescape(detail_html.decode())
        detail_text = url_html.xpath('string(//table[@class="gycq-table"])').replace('\xa0', '').replace('\n', ''). \
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
        item['nativeplace'] = self.get_nativeplace(title)
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
        item['resource'] = '益阳市公共资源'
        item["shi"] = 9509
        item['sheng'] = 9500
        # print(item)
        item['removal']= title
        process_item(item)

    def get_nativeplace(self, addr):
        city = ''
        city_list = [['9509.001', '资阳区'], ['9509.002', '赫山区'], ['9509.003', '南县'], ['9509.004', '桃江县'],
                     ['9509.005', '安化县'], ['9509.006', '沅江市']]
        for i in city_list:
            if i[1] in addr:
                city = float(i[0])
                break
        if city == '':
            city = 9509
        return city

if __name__ == '__main__':

    import traceback, os
    try:
        jl = baoshan_ggzy()
        jl.parse()
    except Exception as e:
        traceback.print_exc()
