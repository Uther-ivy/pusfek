# -*- coding: utf-8 -*-
import json
import re
import time, html
import requests
from lxml import etree
from lxml.etree import HTML
import tool
from save_database import process_item

# 国家能源e购
class baoshan_ggzy:
    def __init__(self):
        self.url_list = [
            'https://www.neep.shop/rest/service/routing/nouser/inquiry/quote/searchCmsArticleList?callback=jQuery&order=asc&inquireName=&publishArea=&noticeType=6&pageNo=1',
            'https://www.neep.shop/rest/service/routing/nouser/inquiry/quote/searchCmsArticleList?callback=jQuery&order=asc&quotDeadline=&inquireName=&publishArea=&inquireCode=&noticeType=2&pageNo=1',
            'https://www.neep.shop/rest/service/routing/nouser/inquiry/quote/searchCmsArticleList?callback=jQuery&order=asc&quotDeadline=&inquireName=&publishArea=&noticeType=3&pageNo=1',
            'https://www.neep.shop/rest/service/routing/nouser/inquiry/quote/searchCmsArticleList?callback=jQuery&order=asc&inquireName=&publishArea=&noticeType=4&pageNo=1&publishTime=',
            'https://www.neep.shop/rest/service/routing/nouser/inquiry/quote/searchCmsArticleList?callback=jQuery&order=asc&inquireName=&publishArea=&noticeType=6&pageNo=1'
        ]
        self.url = self.url_list.pop(0)
        self.headers = {
            # 'Cookie': 'homeid=1a444a31-e460-47ff-9931-1c075c0f3cd8',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36',
        }

    def parse(self):
        while True:
            date = tool.date
            # date='2021-03-31'
            text = tool.requests_get(url=self.url, headers=self.headers).replace('jQuery(','')[:-1].strip()
            detail = json.loads(text)['data']['rows']
            for li in detail:
                # print(li)
                url=li['articleUrl']
                title = li["inquireName"]
                date_Today=str(li['publishTimeString']).split(' ')[0]
                # try:
                #     date_Today = li["CREATED_TIME"]
                # except:
                #     date_Today = li["CREAT_TIME"]
                if '测试' in title:
                    continue
                # url_domain = 'http://zfcgzx.huaian.gov.cn'
                # if 'http' not in url:
                #     if '../../' in url:
                #         url = url_domain + url[5:]
                #     elif '../' in url:
                #         url = url_domain + url[2:]
                #     elif './' in url:
                #         url = url_domain + url[1:]
                #     else:
                #         url = url_domain + url
                # print(title, url, date_Today)
                # # time.sleep(666)
                # print(tool.Transformation(date))
                if tool.Transformation(date) <= tool.Transformation(date_Today):
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
            self.url = self.url_list.pop(0)

    def parse_detile(self, title, url, date):
        print(url)
        t = tool.requests_get(url, self.headers)
        url_html = etree.HTML(t)
        try:
            detail = url_html.xpath('//div[@class="right-main-content"]')[0]
        except:
            return
        # print(detail)
        detail_html = etree.tostring(detail, method='HTML')
        detail_html = html.unescape(detail_html.decode())
        detail_text = url_html.xpath('string(//div[@class="right-main-content"])').replace('\xa0', '').replace('\n', ''). \
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
        item['nativeplace'] = tool.get_title_city(item['title'])
        if item['nativeplace'] == 0:
            item['nativeplace'] = tool.more(item['title']+detail_text)
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
        item['resource'] = '国家能源e购'
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


