# -*- coding: utf-8 -*-
import json
import re
import time, html
import requests
from lxml import etree
from lxml.etree import HTML
import tool
from save_database import process_item

# 烟台市公共资源交易平台
class baoshan_ggzy:
    def __init__(self):
        self.url_list = [
            'http://ggzyjy.yantai.gov.cn/jyxxgc/index_{}.jhtml',
            'http://ggzyjy.yantai.gov.cn/jyxxzc/index_{}.jhtml',
                         ]
        self.url = self.url_list.pop(0)
        self.headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.75 Safari/537.36',
        }

    def parse(self):
        date = tool.date
        # date = '2020-12-11'
        page = 0
        while True:
            page += 1
            text = tool.requests_get(self.url.format(page), self.headers)
            print('*' * 20, page, '*' * 20)
            html_ = HTML(text)
            # print(11, text)
            # time.sleep(6666)
            detail = html_.xpath('//*[@class="article-list2"]/li')
            for li in detail:
                title = li.xpath('./div[1]/a/@title')[0].replace('\n', '').replace('\r', '')\
                    .replace('\t', '').replace(' ', '')
                url = li.xpath('./div[1]/a/@href')[0]
                if 'http' not in url:
                    url = 'http://ggzyjy.yantai.gov.cn' + url
                try:
                    date_Today = li.xpath('./div[1]/div/text()')[0].replace('\n', '').replace('\r', '') \
                        .replace('\t', '').replace(' ', '').replace('(', '').replace(')', '').replace('.', '-')\
                        .replace('[', '').replace(']', '').replace('.', '-')
                except:
                    date_Today = li.xpath('./div[1]/span/text()')[0][:10].replace('\n', '').replace('\r', '') \
                        .replace('\t', '').replace(' ', '').replace('(', '').replace(')', '').replace('.', '-') \
                        .replace('[', '').replace(']', '').replace('.', '-')
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
        try:
            detail = url_html.xpath('//*[@id="content"]')[0]
            detail_html = etree.tostring(detail, method='HTML')
            detail_html = html.unescape(detail_html.decode())
            detail_text = url_html.xpath('string(//*[@id="content"])').replace('\xa0', '').replace('\n',
                                                                                                  ''). \
                replace('\r', '').replace('\t', '').replace(' ', '').replace('\xa5', '')
            if len(detail_html) < 300:
                int('a')
        except:
            try:
                url_ = url_html.xpath('/html/body/div/div[2]/div[2]/iframe/@src')[0]
                t = tool.requests_get(url_, self.headers)
                url_html = etree.HTML(t)
                detail = url_html.xpath('//*[@id="form1"]/table')[0]
                detail_html = etree.tostring(detail, method='HTML')
                detail_html = html.unescape(detail_html.decode())
                detail_text = url_html.xpath('string(//*[@id="form1"]/table)').replace('\xa0', '').replace('\n',
                                                                                                             ''). \
                    replace('\r', '').replace('\t', '').replace(' ', '').replace('\xa5', '')
                if len(detail_html) < 300:
                    int('a')
            except:
                try:
                    detail = url_html.xpath('//*[@class="detail"]')[0]
                    detail_html = etree.tostring(detail, method='HTML')
                    detail_html = html.unescape(detail_html.decode())
                    detail_text = url_html.xpath('string(//*[@class="detail"])').replace('\xa0', '').replace('\n',
                                                                                                              ''). \
                        replace('\r', '').replace('\t', '').replace(' ', '').replace('\xa5', '')
                    if len(detail_html) < 300:
                        int('a')
                except:
                    try:
                        detail = url_html.xpath('//*[@class="content"]')[0]
                        detail_html = etree.tostring(detail, method='HTML')
                        detail_html = html.unescape(detail_html.decode())
                        detail_text = url_html.xpath('string(//*[@class="content"])').replace('\xa0', '').replace('\n',
                                                                                                                 ''). \
                            replace('\r', '').replace('\t', '').replace(' ', '').replace('\xa5', '')
                        if len(detail_html) < 300:
                            return
                    except:
                        detail = url_html.xpath('//*[@class="project_info"]')[0]
                        detail_html = etree.tostring(detail, method='HTML')
                        detail_html = html.unescape(detail_html.decode())
                        detail_text = url_html.xpath('string(//*[@class="project_info"])').replace('\xa0', '').replace('\n',
                                                                                                                  ''). \
                            replace('\r', '').replace('\t', '').replace(' ', '').replace('\xa5', '')
                        if len(detail_html) < 300:
                            return
        if '没有相关公告' in detail_text:
            int('a')
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
        item['resource'] = '烟台市公共资源交易平台'
        item['shi'] = 8005
        item['sheng'] = 8000
        item['removal']= title
        process_item(item)

    def get_nativeplace(self, addr):
        city = ''
        city_list = [['8005.001', '芝罘区'], ['8005.01', '招远市'], ['8005.011', '栖霞市'], ['8005.012', '海阳市'], ['8005.002', '福山区'], ['8005.003', '牟平区'], ['8005.004', '莱山区'], ['8005.005', '长岛县'], ['8005.006', '龙口市'], ['8005.007', '莱阳市'], ['8005.008', '莱州市'], ['8005.009', '蓬莱市']]

        for i in city_list:
            if i[1] in addr:
                city = float(i[0])
                break
        if city == '':
            city = 8006
        return city

if __name__ == '__main__':
    import traceback, os
    try:
        jl = baoshan_ggzy()
        jl.parse()
    except Exception as e:
        traceback.print_exc()
        tool.send_error('报错文件：'+str(os.path.basename(__file__))+'报错信息：'+str(e))


