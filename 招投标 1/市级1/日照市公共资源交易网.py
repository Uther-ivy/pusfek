# -*- coding: utf-8 -*-
import json
import re
import time, html
import requests
from lxml import etree
from lxml.etree import HTML
import tool
from save_database import process_item

# 日照市公共资源交易网
class baoshan_ggzy:
    def __init__(self):
        self.url_list = [
            'http://ggzyjy.rizhao.gov.cn/rzwz/ShowInfo/MoreJyxxList.aspx?categoryNum=071001001&Paging={}',
            'http://ggzyjy.rizhao.gov.cn/rzwz/ShowInfo/MoreJyxxList.aspx?categoryNum=071001002&Paging={}',
            'http://ggzyjy.rizhao.gov.cn/rzwz/ShowInfo/MoreJyxxList.aspx?categoryNum=071001003&Paging={}',
            'http://ggzyjy.rizhao.gov.cn/rzwz/ShowInfo/MoreJyxxList.aspx?categoryNum=071001004&Paging={}',
            'http://ggzyjy.rizhao.gov.cn/rzwz/ShowInfo/MoreJyxxList.aspx?categoryNum=071002002&Paging={}',
            'http://ggzyjy.rizhao.gov.cn/rzwz/ShowInfo/MoreJyxxList.aspx?categoryNum=071002003&Paging={}',
            'http://ggzyjy.rizhao.gov.cn/rzwz/ShowInfo/MoreJyxxList.aspx?categoryNum=071002004&Paging={}'
                         ]
        self.url = self.url_list.pop(0)
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.75 Safari/537.36',
        }

    def parse(self):
        date = tool.date
        # date = '2020-11-03'
        page = 0
        data = {}
        while True:
            page += 1
            text = tool.requests_post(self.url.format(page), data, self.headers)
            print('*' * 20, page, '*' * 20)
            html = HTML(text)
            # print(11, text)
            # time.sleep(6666)
            detail = html.xpath('//*[@id="DataList1"]/tr')
            for li in detail:
                title = li.xpath('./td/li/a/div[1]/text()')[0].replace('\n', '').replace('\r', '')\
                    .replace('\t', '').replace(' ', '').replace('<spanstyle="color:red">', '').replace('</span>', '')
                url = li.xpath('./td/li/a/@href')[0]
                if 'http' not in url:
                    url = 'http://ggzyjy.rizhao.gov.cn/rzwz' + url[2:]
                date_Today = li.xpath('./td/li/a/div[2]/text()')[0].replace('\n', '').replace('\r', '') \
                    .replace('\t', '').replace(' ', '').replace('(', '').replace(')', '').replace('.', '-')
                if '测试' in title:
                    continue
                # print(title, url, date_Today)
                # time.sleep(666)
                if tool.Transformation(date_Today) >= tool.Transformation(date):
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
        detail = url_html.xpath('//*[@id="mainContent"]')[0]
        detail_html = etree.tostring(detail, method='HTML')
        detail_html = html.unescape(detail_html.decode())
        detail_text = url_html.xpath('string(//*[@id="mainContent"])').replace('\xa0', '').replace('\n',
                                                                                                     ''). \
            replace('\r', '').replace('\t', '').replace(' ', '').replace('\xa5', '')
        if len(detail_html) < 300:
            return
        # print(111, detail_text.replace('\xa0','').replace('\xa5',''))
        # time.sleep(6666)
        item = {}
        item['title'] = title.replace('\u2022', '')
        item['url'] = url
        item['date'] = date
        item['typeid'] = tool.get_typeid(item['title'])
        item['senddate'] = int(time.time())
        item['mid'] = 867
        item['nativeplace'] = self.get_nativeplace(item['title'])
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
        item['linkman'] = tool.get_linkman(detail_text)
        item['function'] = tool.get_function(detail_text)
        item['resource'] = '日照市公共资源交易网'
        item['shi'] = 8010
        item['sheng'] = 8000
        item['removal']= title
        process_item(item)

    def get_nativeplace(self, addr):
        city = ''
        city_list = [['8010.001', '东港区'], ['8010.002', '岚山区'], ['8010.003', '五莲县'], ['8010.004', '莒县']]

        for i in city_list:
            if i[1] in addr:
                city = float(i[0])
                break
        if city == '':
            city = 8010
        return city

if __name__ == '__main__':
    import traceback, os
    try:
        jl = baoshan_ggzy()
        jl.parse()
    except Exception as e:
        traceback.print_exc()
        tool.send_error('报错文件：'+str(os.path.basename(__file__))+'报错信息：'+str(e))


