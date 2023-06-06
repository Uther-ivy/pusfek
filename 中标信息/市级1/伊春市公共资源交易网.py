# -*- coding: utf-8 -*-
import json
import re
import time, html
import requests
from lxml import etree
from lxml.etree import HTML
import tool
from save_database import process_item

# 伊春市公共资源交易网
class wenshan_ggzy:
    def __init__(self):
        self.url_list = [
            # 'http://ggzy.yc.gov.cn/docweb/docList.action?channelId=2117&parentChannelId=-1&pageNo={}',
            'http://ggzy.yc.gov.cn/docweb/docList.action?channelId=2120&parentChannelId=-1&pageNo={}',
            # 'http://ggzy.yc.gov.cn/docweb/docList.action?channelId=2121&parentChannelId=2107',
            # 'http://ggzy.yc.gov.cn/docweb/docList.action?channelId=2123&parentChannelId=2107'
            ]
        self.url = self.url_list.pop(0)
        self.headers = {
            'Cookie': 'homeid=1a444a31-e460-47ff-9931-1c075c0f3cd8',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36',
        }

    def parse(self):
        date = tool.date
        # date = '2020-09-16'
        page = 40
        while True:
            page += 1
            if 'pageNo' in self.url:
                text = tool.requests_get(self.url.format(page), self.headers)
            else:
                text = tool.requests_get(self.url, self.headers)
            print('*' * 20, page, '*' * 20)
            html = HTML(text)
            detail = html.xpath('/html/body/div/div[3]/div/div[2]/div[2]/div[1]/ul')
            for tr in detail:
                for li in tr.xpath('./li'):

                    try:
                        title = li.xpath('./a/@title')[0]
                        url = 'http://ggzy.yc.gov.cn' + li.xpath('./a/@href')[0]
                        date_Today = li.xpath('./span/text()')[0]
                        # print(title, url, date_Today)
                        if tool.Transformation(date) <= tool.Transformation(date_Today):
                            # if tool.removal(title, date):
                                self.parse_detile(title, url, date_Today)
                            # else:
                            #     print('【existence】', url)
                            #     continue
                        else:
                            print('日期不符, 正在切换类型', date_Today)
                            return
                    except Exception as e:
                        traceback.print_exc()

    def parse_detile(self, title, url, date):
        print(url)
        url_html = etree.HTML(tool.requests_get(url, self.headers))
        detail = url_html.xpath('/html/body/div/div[3]/div/div[3]')[0]
        detail_html = etree.tostring(detail, method='HTML')
        detail_html = html.unescape(detail_html.decode())
        detail_text = url_html.xpath('string(/html/body/div/div[3]/div/div[3])').replace('\xa0', '').replace('\n', '').\
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
        item['winner'] = tool.get_winner(detail_text)
        item['address'] = tool.get_address(detail_text)
        item['linkman'] = tool.get_linkman(detail_text)
        item['function'] = tool.get_function(detail_text)
        item['resource'] = '伊春市公共资源交易网'
        item['shi'] = 4507
        item['sheng'] = 4500
        item['removal']= title
        process_item(item)
    def get_nativeplace(self, addr):
        city = ''
        city_list = [['4507.001', '伊春区'], ['4507.01', '乌马河区'], ['4507.011', '汤旺河区'], ['4507.012', '带岭区'], ['4507.013', '乌伊岭区'], ['4507.014', '红星区'], ['4507.015', '上甘岭区'], ['4507.016', '嘉荫县'], ['4507.017', '铁力'], ['4507.002', '南岔区'], ['4507.003', '友好区'], ['4507.004', '西林区'], ['4507.005', '翠峦区'], ['4507.006', '新青区'], ['4507.007', '美溪区'], ['4507.008', '金山屯区'], ['4507.009', '五营区']]

        for i in city_list:
            if i[1] in addr:
                city = float(i[0])
                break
        if city == '':
            city = 4507
        return city

if __name__ == '__main__':
    import os,traceback
    try:
        jl = wenshan_ggzy()
        jl.parse()
    except Exception as e:
        traceback.print_exc()
        tool.send_error('报错文件：'+str(os.path.basename(__file__))+'报错信息：'+str(e))



