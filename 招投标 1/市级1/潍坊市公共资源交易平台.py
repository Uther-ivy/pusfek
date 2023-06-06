# -*- coding: utf-8 -*-
import json
import re
import time, html
import requests
from lxml import etree
from lxml.etree import HTML
import tool
from save_database import process_item

# 潍坊市公共资源交易平台
class baoshan_ggzy:
    def __init__(self):
        self.url_list = [
            'http://ggzy.weifang.gov.cn/wfggzy/showinfo/moreinfo_gg.aspx?address=&type=&categorynum=004012001&Paging={}',
            'http://ggzy.weifang.gov.cn/wfggzy/showinfo/moreinfo_gg.aspx?address=&type=&categorynum=004012002&Paging={}',
            'http://ggzy.weifang.gov.cn/wfggzy/showinfo/moreinfo_gg.aspx?address=&type=&categorynum=004012006&Paging={}',
            'http://ggzy.weifang.gov.cn/wfggzy/showinfo/moreinfo_gg.aspx?address=&type=&categorynum=004012007&Paging={}',
            'http://ggzy.weifang.gov.cn/wfggzy/showinfo/moreinfo_gg_zfcgtwo.aspx?address=&type=&categorynum=004002001&Paging={}',
            'http://ggzy.weifang.gov.cn/wfggzy/showinfo/moreinfo_gg_zfcg.aspx?address=&type=&categorynum=004002011&Paging={}',
            'http://ggzy.weifang.gov.cn/wfggzy/showinfo/moreinfo_gg_zfcg.aspx?address=&type=&categorynum=004002012&Paging={}',
            'http://ggzy.weifang.gov.cn/wfggzy/showinfo/moreinfo_gg_zfcg.aspx?address=&type=&categorynum=004002016&Paging={}',
            'http://ggzy.weifang.gov.cn/6in1ggzy/showinfo/moreinfo_gg_zfcgtwo.aspx?address=&type=&categorynum=004002001',
            'http://ggzy.weifang.gov.cn/6in1ggzy/showinfo/moreinfo_gg_zfcg_cgxq.aspx?address=&categorynum=004002017',
            'http://ggzy.weifang.gov.cn/6in1ggzy/showinfo/moreinfo_gg_zfcg.aspx?address=&type=&categorynum=004002011',
            'http://ggzy.weifang.gov.cn/6in1ggzy/showinfo/moreinfo_gg_zfcg.aspx?address=&type=&categorynum=004002012',
            'http://ggzy.weifang.gov.cn/6in1ggzy/showinfo/moreinfo_gg_zfcg.aspx?address=&type=&categorynum=004002016',
            'http://ggzy.weifang.gov.cn/6in1ggzy/showinfo/moreinfo_gg_zfcg.aspx?address=&type=&categorynum=004002013',
            'http://ggzy.weifang.gov.cn/6in1ggzy/showinfo/moreinfo_gg_zfcg.aspx?address=&type=&categorynum=004002014',
                         ]
        self.url = self.url_list.pop(0)
        self.headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
            'Host': 'ggzy.weifang.gov.cn',
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
            detail = html_.xpath('//*[@class="info-form"]/table/tbody/tr')
            for li in detail:
                try:
                    title = li.xpath('./td[3]/span/a/text()')[0].replace('\n', '').replace('\r', '')\
                        .replace('\t', '').replace(' ', '')
                    url = li.xpath('./td[3]/span/a/@href')[0]
                    if 'http' not in url:
                        url = 'http://ggzy.weifang.gov.cn' + url
                    date_Today = li.xpath('./td[4]/span/text()')[0].replace('\n', '').replace('\r', '') \
                        .replace('\t', '').replace(' ', '').replace('(', '').replace(')', '').replace('.', '-')\
                        .replace('[', '').replace(']', '')
                except:
                    try:
                        title = li.xpath('./td[2]/span/a/text()')[0].replace('\n', '').replace('\r', '') \
                            .replace('\t', '').replace(' ', '')
                    except:
                        continue
                    url = li.xpath('./td[2]/span/a/@href')[0]
                    if 'http' not in url:
                        url = 'http://ggzy.weifang.gov.cn' + url
                    date_Today = li.xpath('./td[3]/span/text()')[0].replace('\n', '').replace('\r', '') \
                        .replace('\t', '').replace(' ', '').replace('(', '').replace(')', '').replace('.', '-') \
                        .replace('[', '').replace(']', '')
                if '测试' in title:
                    continue
                # print(title, url, date_Today)
                # time.sleep(666)
                if tool.Transformation(date_Today) >= tool.Transformation(date):
                    if tool.removal(url, date):
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
        item['winner'] = tool.get_winner(detail_text)
        item['address'] = tool.get_address(detail_text)
        item['linkman'] = tool.get_linkman(detail_text)
        item['function'] = tool.get_function(detail_text)
        item['resource'] = '潍坊市公共资源交易平台'
        item['shi'] = 8006
        item['sheng'] = 8000
        item['removal']= url
        process_item(item)

    def get_nativeplace(self, addr):
        city = ''
        city_list = [['8006.001', '潍城区'], ['8006.01', '安丘市'], ['8006.011', '高密市'], ['8006.012', '昌邑市'], ['8006.002', '寒亭区'], ['8006.003', '坊子区'], ['8006.004', '奎文区'], ['8006.005', '临朐县'], ['8006.006', '昌乐县'], ['8006.007', '青州市'], ['8006.008', '诸城市'], ['8006.009', '寿光市']]

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
        # tool.send_error('报错文件：'+str(os.path.basename(__file__))+'报错信息：'+str(e))


