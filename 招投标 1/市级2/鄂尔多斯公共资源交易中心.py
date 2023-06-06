# -*- coding: utf-8 -*-
import json
import re
import time, html
import requests
from lxml import etree
from lxml.etree import HTML
import tool
from save_database import process_item

# 鄂尔多斯公共资源交易中心
class wenshan_ggzy:
    def __init__(self):
        self.url_list = [
            'http://www.ordosggzyjy.org.cn/TPFront/showinfo/MoreListSqhb.aspx?CategoryNum=009001',
                     'http://www.ordosggzyjy.org.cn/TPFront/showinfo/MoreListSqhb.aspx?CategoryNum=009002',
                     'http://www.ordosggzyjy.org.cn/TPFront/showinfo/MoreListSqhb.aspx?CategoryNum=009003',
                     'http://www.ordosggzyjy.org.cn/TPFront/showinfo/MoreListSqhb.aspx?CategoryNum=009004',
                     'http://www.ordosggzyjy.org.cn/TPFront/showinfo/MoreListSqhb.aspx?CategoryNum=009005',
                     'http://www.ordosggzyjy.org.cn/TPFront/showinfo/MoreListSqhb.aspx?CategoryNum=009006',
                     'http://www.ordosggzyjy.org.cn/TPFront/showinfo/MoreListSqhb.aspx?CategoryNum=009007',
                     'http://www.ordosggzyjy.org.cn/TPFront/showinfo/MoreListSqhb.aspx?CategoryNum=009008',
                     'http://www.ordosggzyjy.org.cn/TPFront/zfcg/010001/?Paging=1',
                     'http://www.ordosggzyjy.org.cn/TPFront/zfcg/010003/?categorynum=010003',
                     'http://www.ordosggzyjy.org.cn/TPFront/zfcg/010005/?categorynum=010005',
                     'http://www.ordosggzyjy.org.cn/TPFront/zfcg/010006/?categorynum=010006',
                     'http://www.ordosggzyjy.org.cn/TPFront/zfcg/010010/?categorynum=010010',
                     'http://www.ordosggzyjy.org.cn/TPFront/zfcg/010008/010008001/?categorynum=010008001',
                     'http://www.ordosggzyjy.org.cn/TPFront/zfcg/010008/010008002/?categorynum=010008002',
                     'http://www.ordosggzyjy.org.cn/TPFront/zfcg/010008/010008004/?categorynum=010008004',
                    ]
        self.url = self.url_list.pop(0)
        self.headers = {
            'Cookie': 'homeid=1a444a31-e460-47ff-9931-1c075c0f3cd8',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36',
        }

    def parse(self):
        date = tool.date
        # date = '2020-04-02'
        page = 1
        while True:
            text = tool.requests_get(self.url, self.headers)
            print('*' * 20, page, '*' * 20)
            # print(11, text)
            # time.sleep(6666)
            if 'zfcg' in self.url:
                detail = HTML(text).xpath('//*[@id="main"]/div[2]/table/tr/td[3]/table/tr[3]/td/div/table/tr/td/table/tr')
            else:
                detail = HTML(text).xpath('//*[@id="DataGrid1"]/tr')
            for li in detail:
                if 'zfcg' not in self.url:
                    title = li.xpath('./td[3]/a/@title')[0]
                    url = 'http://www.ordosggzyjy.org.cn' + li.xpath('./td[3]/a/@href')[0]
                    date_Today = li.xpath('./td[4]/text()')[0].replace('[', '').replace(']', '').replace('\r', '').replace('\n', '').replace('\t', '').replace(' ', '')
                else:
                    try:
                        title = li.xpath('./td[2]/a/@title')[0]
                        url = 'http://www.ordosggzyjy.org.cn' + li.xpath('./td[2]/a/@href')[0]
                        date_Today = li.xpath('./td[3]/text()')[0].replace('[', '').replace(']', '').replace('\r',
                                                                                                             '').replace(
                            '\n', '').replace('\t', '').replace(' ', '')
                    except:
                        continue

                # print(title, url, date_Today)
                # time.sleep(666)
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
            page = 0
    def parse_detile(self, title, url, date):
        print(url)
        url_html = etree.HTML(tool.requests_get(url, self.headers))
        try:
            detail = url_html.xpath('//*[@id="TDContent"]/div/table')[0]
            detail_html = etree.tostring(detail, method='HTML')
            detail_html = html.unescape(detail_html.decode())
            detail_text = url_html.xpath('string(//*[@id="TDContent"]/div/table)').replace('\xa0', '').replace('\n', '').\
                replace('\r', '').replace('\t', '').replace(' ', '').replace('\xa5', '')
            if len(detail_html) < 200:
                int('a')
        except:
            try:
                detail = url_html.xpath('//*[@id="noticeArea"]')[0]
                detail_html = etree.tostring(detail, method='HTML')
                detail_html = html.unescape(detail_html.decode())
                detail_text = url_html.xpath('string(//*[@id="noticeArea"])').replace('\xa0', '').replace('\n',
                                                                                                                   ''). \
                    replace('\r', '').replace('\t', '').replace(' ', '').replace('\xa5', '')
                if len(detail_html) < 200:
                    int('a')
            except:
                detail = url_html.xpath('//*[@class="noticeArea"]')[0]
                detail_html = etree.tostring(detail, method='HTML')
                detail_html = html.unescape(detail_html.decode())
                detail_text = url_html.xpath('string(//*[@class="noticeArea"])').replace('\xa0', '').replace('\n',
                                                                                                          ''). \
                    replace('\r', '').replace('\t', '').replace(' ', '').replace('\xa5', '')
                if len(detail_html) < 200:
                    int('a')
        # print(detail_text.replace('\xa0','').replace('\xa5',''))
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
        item['resource'] = '鄂尔多斯公共资源交易中心'
        item['shi'] = 3006
        item['sheng'] = 3000
        item['removal']= title
        process_item(item)
    def get_nativeplace(self, addr):
        city = ''
        city_list = [['3006.001', '东胜区'], ['3006.002', '达拉特旗'], ['3006.003', '准格尔旗'], ['3006.004', '鄂托克前旗'], ['3006.005', '鄂托克旗'], ['3006.006', '杭锦旗'], ['3006.007', '乌审旗'], ['3006.008', '伊金霍洛旗']]

        for i in city_list:
            if i[1] in addr:
                city = float(i[0])
                break
        if city == '':
            city = 3006
        return city

if __name__ == '__main__':
    import traceback,os
    try:
        jl = wenshan_ggzy()
        jl.parse()
    except Exception as e:
        traceback.print_exc()
