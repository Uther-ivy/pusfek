# -*- coding: utf-8 -*-
import json
import re
import time, html
import traceback
import scrapy
import base64
import requests
from lxml import etree
from lxml.etree import HTML
import tool
from save_database import process_item
from tool import get_city,more
# 中国政府采购网
class xinyang_ggzy:
    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36',
            'Cookie': 'Hm_lvt_9f8bda7a6bb3d1d7a9c7196bfed609b5=1630995346; JSESSIONID=s1i-5xuUUYpn30u7YNw3JBb7rVvFOtUKJAdzsa_FgAnaZL1fPadh!2105014073; Hm_lpvt_9f8bda7a6bb3d1d7a9c7196bfed609b5=1630995422'
        }

    def parse(self):
        date = tool.date
        page = 20
        while True:
            page += 1
            print('*' * 20, page, '*' * 20)
            url=f'http://search.ccgp.gov.cn/bxsearch?searchtype=1&page_index={page}&bidSort=0&buyerName=&projectId=&pinMu=0&bidType=7&dbselect=bidx&kw=%E4%B8%AD%E6%A0%87&start_time=2019%3A01%3A01&end_time=2023%3A04%3A12&timeType=6&displayZone=&zoneId=&pppStatus=0&agentName='
            text = tool.requests_get(url, self.headers)

            html = HTML(text)
            detail = html.xpath("//ul[@class='vT-srch-result-list-bid']/li")
            for li in detail:
                try:
                    title = li.xpath('./a//text()')[0].split('发布日期')[0].replace(' ','')
                    dates=li.xpath('./span/text()')[0].split('|')[0]
                    date_Today = re.findall(r'(\d{4}\.\d{2}\.\d{2})',dates)[0].replace('.','-')
                    url =  li.xpath('./a/@href')[0]

                    print(title,date_Today,url)
                    if '测试' in title:
                        continue
                    if tool.Transformation(date) <= tool.Transformation(date_Today):
                            self.parse_detile(title, url, date_Today)
                    else:
                        print('日期不符, 正在切换类型', date_Today)
                        return
                except Exception:
                    traceback.print_exc()


    def parse_detile(self, title, url, date):
        print(url)
        t = tool.requests_get(url, self.headers)
        # print(t)
        url_html = etree.HTML(t)
        try:
            detail = url_html.xpath('//*[@class="vF_detail_content"]')[0]
            detail_html = etree.tostring(detail, method='HTML')
            detail_html = html.unescape(detail_html.decode()).replace('\xa0', '').replace('\ufeff', '')
            detail_text = url_html.xpath('string(//*[@class="vF_detail_content"])') \
                .replace('\xa0', '').replace('\n', '').replace('\r', '').replace('\t', '') \
                .replace(' ', '').replace('\xa5', '').replace('\ufeff', '')
        except:
            try:
                detail = url_html.xpath('//*[@class="vF_detail_content_container"]')[0]
                detail_html = etree.tostring(detail, method='HTML')
                detail_html = html.unescape(detail_html.decode()).replace('\xa0', '').replace('\ufeff', '')
                detail_text = url_html.xpath('string(//*[@class="vF_detail_content_container"])') \
                    .replace('\xa0', '').replace('\n', '').replace('\r', '').replace('\t', '') \
                    .replace(' ', '').replace('\xa5', '').replace('\ufeff', '')
            except:
                return
        item = {}
        item['title'] = title.replace('\u2022', '').replace('\n', '').replace('\r', '')
        item['url'] = url
        item['date'] = date
        item['typeid'] = tool.get_typeid(item['title'])
        item['senddate'] = int(time.time())
        item['mid'] = 867
        item['infotype'] = tool.get_infotype(item['title'])
        item['body'] = tool.qudiao_width(detail_html)
        item['body'] = tool.qudiao_width(item["body"])
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
        # print(item['title'])
        item['winner'] = tool.get_winner(detail_text)
        item['address'] = tool.get_address(detail_text)
        item['nativeplace'] = tool.get_title_city(item['title'])
        if item['nativeplace'] == 0:
            item['nativeplace'] = tool.more(item['title']+detail_text)
        item['linkman'] = tool.get_linkman(detail_text)
        item['function'] = tool.get_function(detail_text)
        item['resource'] = '中国政府采购网'
        # print(';;;;;',item["nativeplace"])
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
        item['removal']= title
        process_item(item)
        # print(item['title'],item['url'],item['nativeplace'],item['address'])
        # time.sleep(6666)

if __name__ == '__main__':
    import traceback, os
    try:
        jl = xinyang_ggzy()
        jl.parse()
    except Exception as e:
        traceback.print_exc()
