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

# 中国化学工程集团
class baoshan_ggzy:
    def __init__(self):
        self.url_list = [
            # 'http://bid.cncecyc.com/cms/channel/ywgg1hw/index.htm',
            # 'http://bid.cncecyc.com/cms/channel/ywgg2hw/index.htm',
            'http://bid.cncecyc.com/cms/channel/ywgg4hw/index.htm',
            # 'http://bid.cncecyc.com/cms/channel/ywgg3xj/index.htm',

        ]
        self.url = self.url_list.pop(0)
        self.headers = {
            # 'Cookie': 'homeid=1a444a31-e460-47ff-9931-1c075c0f3cd8',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36',
        }

    def parse(self):
        date = tool.date
        page=103

        while True:
            try:
                page+=1
                print('*' * 20, page, '*' * 20)
                if page == 1:
                    text = tool.requests_get(self.url,self.headers)
                else:
                    url=self.url+f"?pageNo={page}"
                    text = tool.requests_get(url, self.headers)
                # print(text)

                html = HTML(text)
                detail = html.xpath('//ul[@id="list1"]//li')

                # print(de)
                for li in range(len(detail)):
                    url= 'http://bid.cncecyc.com'+html.xpath(f'(//ul[@id="list1"]//li//a//@href)[{li+1}]')[0]
                    title = ''.join(html.xpath(f'(//ul[@id="list1"]//li//a//@title)[{li+1}]')).replace(' ','').strip()
                    date_Today = html.xpath(f'(//ul[@id="list1"]//li//span[@class="bidDate"]//text())[{li+1}]')[0]
                    if '发布' in date_Today:
                        continue
                    if '测试' in title:
                        continue
                    # print(title, url, date_Today)
                    # # time.sleep(666)
                    if tool.Transformation(date) <= tool.Transformation(date_Today):
                        # if tool.removal(title, date):
                        time.sleep(1 + random.random() * 10)
                        self.parse_detile(title, url, date_Today)
                    # else:
                    #     print('【existence】', url)
                    #     break
                    else:
                        print('日期不符, 正在切换类型', date_Today, self.url)
                        return
            except Exception:
                traceback.print_exc()


    def parse_detile(self, title, url, date):
        t = tool.requests_get(url, self.headers)
        url_html = etree.HTML(t)
        detail = url_html.xpath('//div[@class="ninfo-con"]')[0]
        if  detail:
        # print(detail)
            detail_html = etree.tostring(detail, method='HTML')
            detail_html = html.unescape(detail_html.decode())
            detail_text = url_html.xpath('string(//div[@class="ninfo-con"])').replace('\xa0', '').replace('\n', ''). \
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
            item['nativeplace'] = tool.get_title_city(item['title'])
            if item['nativeplace'] == 0:
                item['nativeplace'] = tool.more(item['title']+ detail_text)
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
            item['resource'] = '中国化学工程集团'
            if '.' in str(item["nativeplace"]):
                item["shi"] = int(float(str(item["nativeplace"]).replace("['","").split('.')[0]))
            else:
                item["shi"] = int(float(item["nativeplace"]))
            if len(str(int(item["shi"]))) == 4:
                item['sheng'] = int(str(item["shi"])[:2] + '00')
            elif len(str(int(item["shi"]))) == 5:
                item['sheng'] = int(str(item["shi"])[:3] + '00')
            else:
                item['sheng'] = 0
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
