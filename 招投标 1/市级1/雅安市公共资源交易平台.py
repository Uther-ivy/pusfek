# -*- coding: utf-8 -*-
import json
import re
import time, html
import requests
from lxml import etree
from lxml.etree import HTML
import tool
from save_database import process_item

# 雅安市公共资源交易平台
class baoshan_ggzy:
    def __init__(self):
        self.url_list = [
            'http://www.yaggzy.org.cn/jyxx/jsgcBgtz',
            'http://www.yaggzy.org.cn/jyxx/jsgcpbjggs',
            'http://www.yaggzy.org.cn/jyxx/jsgcZbjggs',
            'http://www.yaggzy.org.cn/jyxx/zfcg/zbjggs'
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
            text = tool.requests_get(self.url, self.headers)
            print('*' * 20, page, '*' * 20)
            html_ = HTML(text)
            # print(11, text)
            # time.sleep(6666)
            detail = html_.xpath('//*[@id="p2"]/tr')
            if len(detail) == 0:
                detail = html_.xpath('/html/body/div[6]/div[2]/ul/li[3]/table/tr')
            if len(detail) == 0:
                detail = html_.xpath('/html/body/div[6]/div[2]/ul/li[2]/table/tr')
            for li in detail:
                try:
                    title = li.xpath('./td[3]/a/@title')[0].replace('\n', '').replace('\r', '')\
                        .replace('\t', '').replace(' ', '')
                    url = li.xpath('./td[3]/a/@href')[0]
                except:
                    continue
                if 'http' not in url:
                    url = 'http://www.yaggzy.org.cn' + url
                date_Today = li.xpath('./td[4]/text()')[0].replace('\n', '').replace('\r', '') \
                    .replace('\t', '').replace(' ', '').replace('(', '').replace(')', '').replace('.', '-')\
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
            detail = url_html.xpath('/html/body/div[5]/div/div/div/div[2]/table')[0]
            detail_html = etree.tostring(detail, method='HTML')
            detail_html = html.unescape(detail_html.decode())
            detail_text = url_html.xpath('string(/html/body/div[5]/div/div/div/div[2]/table)').replace('\xa0', '').replace('\n',
                                                                                                      ''). \
                replace('\r', '').replace('\t', '').replace(' ', '').replace('\xa5', '')
            if len(detail_html) < 300:
                return
        except:
            try:
                detail = url_html.xpath('//*[@id="myShow"]/div[3]')[0]
                detail_html = etree.tostring(detail, method='HTML')
                detail_html = html.unescape(detail_html.decode())
                detail_text = url_html.xpath('string(//*[@id="myShow"]/div[3])').replace('\xa0',
                                                                                                           '').replace('\n',
                                                                                                                       ''). \
                    replace('\r', '').replace('\t', '').replace(' ', '').replace('\xa5', '')
                if len(detail_html) < 300:
                    return
            except:
                detail = url_html.xpath('//*[@class="nr"]')[0]
                detail_html = etree.tostring(detail, method='HTML')
                detail_html = html.unescape(detail_html.decode())
                detail_text = url_html.xpath('string(//*[@class="nr"])').replace('\xa0',
                                                                                         '').replace('\n',
                                                                                                     ''). \
                    replace('\r', '').replace('\t', '').replace(' ', '').replace('\xa5', '')
                if len(detail_html) < 300:
                    return
        if '没有相关公告' in detail_text:
            int('a')
        # print(111, detail_html.replace('\xa0','').replace('\xa5',''))
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
        item['resource'] = '雅安市公共资源交易平台'
        item['shi'] = 12016
        item['sheng'] = 12000
        item['removal']= title
        process_item(item)

    def get_nativeplace(self, addr):
        city = ''
        city_list = [['12016.001', '雨城区'], ['12016.002', '名山县'], ['12016.003', '荥经县'], ['12016.004', '汉源县'], ['12016.005', '石棉县'], ['12016.006', '天全县'], ['12016.007', '芦山县'], ['12016.008', '宝兴县']]

        for i in city_list:
            if i[1] in addr:
                city = float(i[0])
                break
        if city == '':
            city = 12016
        return city

if __name__ == '__main__':
    import traceback, os
    try:
        jl = baoshan_ggzy()
        jl.parse()
    except Exception as e:
        traceback.print_exc()
        # traceback.print_exc()
        tool.send_error('报错文件：'+str(os.path.basename(__file__))+'报错信息：'+str(e))


