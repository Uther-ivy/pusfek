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

# 雄安新区公共资源网
class xinyang_ggzy:
    def __init__(self):
        self.url_list = [
            'http://www.xaprtc.com/jyxxzc/index_{}.jhtml?token=d89e753d90084c08a6b7ea95bd5c61c0',
            'http://www.xaprtc.com/jyxxgc/index_{}.jhtml?token=34311e73bf7a464c8b350e0ff4e01301'
        ]
        self.url = self.url_list.pop(0)
        self.headers = {
                # "Accept": "*/*",
                # "Accept-Encoding": "gzip, deflate",
                # "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
                # "Connection": "keep-alive",
                # "Content-Type": "application/json",
                # "Cookie": "acw_tc=76b20ffc15687134890437834e2184fbe853526d3525595fc50cea2c76ef1b",
                # "Host": "www.ccgp-xinjiang.gov.cn",
                # "Origin": "http://www.ccgp-xinjiang.gov.cn",
                # "Referer": "http://www.ccgp-xinjiang.gov.cn/ZcyAnnouncement/ZcyAnnouncement9/index.html",
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.131 Safari/537.36",
                # "X-Requested-With": "XMLHttpRequest"
            }

    def parse(self):
        date = tool.date
        # date = '2020-07-10'
        page = 0
        while True:
            page += 1
            text = tool.requests_get(self.url.format(page), self.headers)
            detail = HTML(text).xpath("//div[@class='er-container']/ul/li")
            print('*' * 20, page, '*' * 20)
            for li in detail:
                url = li.xpath("./div/a/@href")[0]
                title = li.xpath("./div/a/@title")[0]
                date_Today = li.xpath("./div/p/text()")[0]
                # print(title, url, date_Today)
                # time.sleep(666)
                if '测试' in title:
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
            if page == 30:
                self.url = self.url_list.pop(0)
                break


    def parse_detile(self, title, url, date):
        print(url)
        t = tool.requests_get(url, self.headers)
        url_html = etree.HTML(t)
        try:
            detail = 'https://www.xaprtc.com/' + url_html.xpath('//*[@id="previewPdf"]/@src')[0].replace('../', '').replace('./', '')
            detail_html = '<embed src="{}">'.format(detail)
            detail_text = url_html.xpath('string(//div[@class="article"])') \
                .replace('\xa0', '').replace('\n', '').replace('\r', '').replace('\t', '') \
                .replace(' ', '').replace('\xa5', '').replace('\ufeff', '')
        except:
            detail = url_html.xpath('//div[@class="article"]')[0]
            detail_html = etree.tostring(detail, method='HTML')
            detail_html = html.unescape(detail_html.decode())
            detail_text = url_html.xpath('string(//div[@class="article"])') \
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
        item['nativeplace'] = self.get_nativeplace(item['title'])
        item['linkman'] = tool.get_linkman(detail_text)
        item['function'] = tool.get_function(detail_text)
        item['resource'] = '雄安新区公共资源网'
        item["shi"] = 2006
        item['sheng'] = 2000
        item['removal']= title
        process_item(item)
        # print(item['body'])

    def get_nativeplace(self, addr):
        city = ''
        city_list = [['2006.001', '新市区'], ['2006.01', '唐县'], ['2006.011', '高阳县'], ['2006.012', '容城县'], ['2006.013', '涞源县'], ['2006.014', '望都县'], ['2006.015', '安新县'], ['2006.016', '易县'], ['2006.017', '曲阳县'], ['2006.018', '蠡县'], ['2006.019', '顺平县'], ['2006.002', '北市区'], ['2006.02', '博野县'], ['2006.021', '雄县'], ['2006.022', '涿州市'], ['2006.023', '定州市'], ['2006.024', '安国市'], ['2006.025', '高碑店市'], ['2006.026', '竞秀区'], ['2006.027', '莲池区'], ['2006.003', '南市区'], ['2006.004', '满城县'], ['2006.005', '清苑县'], ['2006.006', '涞水县'], ['2006.007', '阜平县'], ['2006.008', '徐水县']]

        for i in city_list:
            if i[1] in addr:
                city = float(i[0])
                break
        if city == '':
            city = 2006
        return city

if __name__ == '__main__':
    import traceback, os
    try:
        jl = xinyang_ggzy()
        jl.parse()
    except Exception as e:
        traceback.print_exc()
        tool.send_error('报错文件：'+str(os.path.basename(__file__))+'报错信息：'+str(e))


