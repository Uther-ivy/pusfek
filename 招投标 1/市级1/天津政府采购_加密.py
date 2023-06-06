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

# 天津政府采购
class xinyang_ggzy:
    def __init__(self):
        self.url_list = [1665, 1664, 1663, 1666, 2014, 2013,2033,2034]
        # self.url_list = [2033,2034]
        self.url = self.url_list.pop(0)
        self.headers = {
            # 'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
            # "Accept-Encoding": "gzip, deflate",
            'Accept': '*/*',
            "Cookie": "HttpOnly; JSESSIONID=N-872i6Lk6J0n4Ab80AIMV5x9DyNUGIVNgofcJ9e022QI57aYy-R!-1298288453; insert_cookie=24822820; HttpOnly",
            "Host": "www.ccgp-tianjin.gov.cn",
            "Origin": "http://www.ccgp-tianjin.gov.cn",
            # "Referer": "http://www.ccgp-tianjin.gov.cn/portal/topicView.do?method=view&view=Infor&id=1665&ver=2&st=1&stmp=1563612630952",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.131 Safari/537.36"
        }

    def time_date(self, date):
        date_ls = date.split(' ')
        month = ''
        month_ls = ['Jan', 'Feb','Mar', 'Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec']
        for i in month_ls:
            if date_ls[1] == i:
                month = str(month_ls.index(i)+1)
                if len(month) == 1:
                    month = '0' + month
                break
        return date_ls[-1] + '-' + month + '-' + date_ls[2]

    def parse(self):
        date = tool.date
        # date = '2020-07-10'
        page = 0
        url_to = 'http://www.ccgp-tianjin.gov.cn/portal/topicView.do'
        while True:
            page += 1
            data = {"method": "view",
                    "page": "{}".format(page),
                    "id": "{}".format(self.url),
                    "step": "1",
                    "view": "Infor",
                    "st": "1",
                    'ldateQGE': '',
                    'ldateQLE': ''}
            text = tool.requests_post(url_to, data, self.headers)
            if '您的访问过于频繁，请稍后再试' in text:
                print('您的访问过于频繁，请稍后再试')
                page -= 1
                time.sleep(10)
                continue
            detail = HTML(text).xpath("//div[@id='reflshPage']/ul/li")
            # print(text)
            # time.sleep(666)
            print('*' * 20, page, '*' * 20)
            for li in detail:
                url = "http://www.ccgp-tianjin.gov.cn/portal/documentView.do?method=view&id={}&ver=2".format(
                    re.findall('id=(.*?)&', li.xpath("./a/@href")[0])[0])
                date_Today = self.time_date(li.xpath("./span/text()")[0])
                title = li.xpath("./a/text()")[0].replace(' ','')
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
                    print('日期不符, 正在切换类型', date_Today, self.url)
                    return



    def parse_detile(self, title, url, date):
        print(url)
        t = tool.requests_get(url, self.headers)
        url_html = etree.HTML(t)
        try:
            detail = url_html.xpath('//*[@id="pageContent"]/div/table')[0]
            detail_html = etree.tostring(detail, method='HTML')
            detail_html = html.unescape(detail_html.decode()).replace('\xa0', '').replace('\ufeff', '')
            detail_text = url_html.xpath('string(//*[@id="pageContent"]/div/table)') \
                .replace('\xa0', '').replace('\n', '').replace('\r', '').replace('\t', '') \
                .replace(' ', '').replace('\xa5', '').replace('\ufeff', '')
        except:
            try:
                detail = url_html.xpath('//*[@id="pageContent"]/div/table/tbody/tr/td')[0]
                detail_html = etree.tostring(detail, method='HTML')
                detail_html = html.unescape(detail_html.decode()).replace('\xa0', '').replace('\ufeff', '')
                detail_text = url_html.xpath('string(//*[@id="pageContent"]/div/table/tbody/tr/td)') \
                    .replace('\xa0', '').replace('\n', '').replace('\r', '').replace('\t', '') \
                    .replace(' ', '').replace('\xa5', '').replace('\ufeff', '')
            except:
                return
        item = {}
        item['title'] = title.replace('\u2022', '')
        item['url'] = url
        item['date'] = date
        item['typeid'] = tool.get_typeid(item['title'])
        item['senddate'] = int(time.time())
        item['mid'] = 867
        item['infotype'] = tool.get_infotype(item['title'])
        item['body'] = tool.qudiao_width(detail_html)
        # b = re.findall('''<p class="news-article-info">.*?</p>''', item['body'])[0]
        # item['body'] = item['body'].replace(b, '')
        # print(item['body'])
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
        item['winner'] = tool.get_winner(detail_text)
        item['address'] = tool.get_address(detail_text)
        item['nativeplace'] = self.get_nativeplace(item['title'])
        item['linkman'] = tool.get_linkman(detail_text)
        item['function'] = tool.get_function(detail_text)
        item['resource'] = '天津政府采购'
        item["shi"] = int(str(item["nativeplace"]).split('.')[0])
        item['sheng'] = 1500
        item['removal']= title
        process_item(item)
        # print(item['body'])

    def get_nativeplace(self, addr):
        city = ''
        city_list = [['1501', '和平'], ['1502', '河东'], ['1503', '河西'], ['1504', '南开'], ['1505', '河北'], ['1506', '红桥'], ['1507', '塘沽'], ['1508', '汉沽'], ['1509', '大港'], ['1510', '东丽'], ['1511', '西青'], ['1512', '津南'], ['1513', '北辰'], ['1514', '武清'], ['1515', '宝坻'], ['1516', '宁河'], ['1517', '静海']]

        for i in city_list:
            if i[1] in addr:
                city = float(i[0])
                break
        if city == '':
            city = 1500
        return city

if __name__ == '__main__':
    import traceback,os
    try:
        jl = xinyang_ggzy()
        jl.parse()
    except Exception as e:
        traceback.print_exc()
        tool.send_error('报错文件：'+str(os.path.basename(__file__))+'报错信息：'+str(e))



