# -*- coding: utf-8 -*-
import json
import re
import time, html
import requests
from lxml import etree
from lxml.etree import HTML
import tool
from save_database import process_item

# 中央政府采购网电子卖场
class baoshan_ggzy:
    def __init__(self):
        self.url_list = [
            'https://mkt.zycg.gov.cn/proxy/platform/platform/notice/queryMallNoticePageList?pageSize=10&pageNum={}&noticeStatus=10',
            'https://mkt.zycg.gov.cn/proxy/platform/platform/notice/queryMallNoticePageList?pageSize=10&pageNum={}&noticeTypes=1&effectType=2&noticeStatus=10',
            'https://mkt.zycg.gov.cn/proxy/platform/platform/notice/queryMallNoticePageList?pageSize=10&pageNum={}&noticeTypes=3&effectType=8&noticeStatus=10',
        ]
        self.url = self.url_list.pop(0)
        self.headers = {
            # 'Cookie': 'homeid=1a444a31-e460-47ff-9931-1c075c0f3cd8',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36',
        }

    def parse(self):
        page = 0
        while True:
            page += 1
            date = tool.date
            # date = '2021-07-12'
            print('-'*50, page)
            text = json.loads(tool.requests_get(self.url.format(page),self.headers))
            detail = text['data']['result']
            for li in detail:
                url= 'http://mkt.zycg.gov.cn/mall-view/information/detail?noticeId='+str(li['id'])
                title = li['noticeTitle']
                date_Today = li['shortPublistTime']
                if '发布' in date_Today:
                    continue
                if '测试' in title:
                    continue
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
        code = url.replace('http://mkt.zycg.gov.cn/mall-view/information/detail?noticeId=', '')
        u = 'https://mkt.zycg.gov.cn/proxy/platform/platform/notice/queryMallNoticeById?platformId=20&id='+code
        t = tool.requests_get(u, self.headers)
        detail_html = json.loads(t)['data']['contentStr']
        detail_text = ''.join(re.findall('>(.*?)<', detail_html, re.S)).replace('\xa0', '').replace('\n', ''). \
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
        item['resource'] = '中央政府采购网电子卖场'
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
