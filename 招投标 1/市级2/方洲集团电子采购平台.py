# -*- coding: utf-8 -*-
import json
import re
import time, html
import requests
from lxml import etree
from lxml.etree import HTML
import tool
from save_database import process_item

# 方洲集团电子采购平台
class xinyang_ggzy:
    def __init__(self):
        self.url_list = [
            'http://218.92.104.98:18080/jyxx/001001/{}.html',
            'http://218.92.104.98:18080/jyxx/001002/{}.html'
        ]
        self.url = self.url_list.pop(0)
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36',
        }

    def parse(self):
        date = tool.date
        # date = '2022-05-22'
        page = 0
        while True:
            page += 1
            if page == 1:
                if '001002' in self.url:
                    text = tool.requests_get(self.url.format('list'), self.headers)
                else:
                    text = tool.requests_get(self.url.format('listcggg'), self.headers)
            else:
                text = tool.requests_get(self.url.format(page), self.headers)
            # print(text)
            # time.sleep(666)
            html = HTML(text)
            print('*' * 20, page, '*' * 20)
            detail = html.xpath('//*[@id="list"]/li')
            for li in detail:
                title = li.xpath('./a/@title')[0].replace('\xa0', '').replace(' ', '')
                url = li.xpath('./a/@href')[0]
                date_Today = li.xpath('./span/text()')[0].replace('\r', '').replace(' ', '').replace('\n', '').replace('\t', '').replace('发布时间：', '')
                if 'http' not in url:
                    if '../../' in url:
                        url = '/'.join(self.url.split('/')[:3]) + '/' + url.replace('../', '')
                    elif '../' in url:
                        url = '/'.join(self.url.split('/')[:5]) + '/' + url.replace('../', '')
                    elif url[0] == '/':
                        url = '/'.join(self.url.split('/')[:3]) + url.replace('./', '')
                    else:
                        url = '/'.join(self.url.split('/')[:-1]) + '/' + url.replace('./', '')
                # print(title, url, date_Today)
                # time.sleep(666)
                if '测试' in title or '/'.join(self.url.split('/')[:3]) not in url:
                    continue
                if tool.Transformation(date) <= tool.Transformation(date_Today):
                    if tool.removal(title, date):
                        self.parse_detile(title, url, date_Today)
                    else:
                        print('【existence】', url)
                        continue
                else:
                    print('日期不符, 正在切换类型', date_Today)
                    self.url = self.url_list.pop(0)
                    page = 0
                    break
            if page == 20:
                self.url = self.url_list.pop(0)
                break

    def parse_detile(self, title, url, date):
        print(url)
        t = tool.requests_get(url, self.headers)
        url_html = etree.HTML(t)
        try:
            detail = url_html.xpath('/html/body/div[2]/div/div[2]/div/div[2]')[0]
            detail_html = etree.tostring(detail, method='HTML')
            detail_html = html.unescape(detail_html.decode()).replace('\xa0', '').replace('\ufeff', '')
            detail_text = url_html.xpath('string(/html/body/div[2]/div/div[2]/div/div[2])') \
                .replace('\xa0', '').replace('\n', '').replace('\r', '').replace('\t', '') \
                .replace(' ', '').replace('\xa5', '').replace('\ufeff', '')
        except:
            detail = url_html.xpath('//*[@class="table table-sm table-bordered table-th-bg-light"]')[0]
            detail_html = etree.tostring(detail, method='HTML')
            detail_html = html.unescape(detail_html.decode()).replace('\xa0', '').replace('\ufeff', '')
            detail_text = url_html.xpath('string(//*[@class="table table-sm table-bordered table-th-bg-light"])') \
                .replace('\xa0', '').replace('\n', '').replace('\r', '').replace('\t', '') \
                .replace(' ', '').replace('\xa5', '').replace('\ufeff', '')
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
            item['nativeplace'] = tool.more(item['title']+detail_text)
        item['linkman'] = tool.get_linkman(detail_text)
        item['function'] = tool.get_function(detail_text)
        item['resource'] = '方洲集团电子采购平台'
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
    jl = xinyang_ggzy()
    jl.parse()


