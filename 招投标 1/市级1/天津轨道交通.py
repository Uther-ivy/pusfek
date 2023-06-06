# -*- coding: utf-8 -*-
import json
import re
import time, html
import requests
from lxml import etree
from lxml.etree import HTML
import tool
from save_database import process_item

# 天津轨道交通
class xinyang_ggzy:
    def __init__(self):
        self.url_list = [
            'http://www.tjgdjt.com/xinwen/{}.htm'
        ]
        self.url = self.url_list.pop(0)
        self.headers = {
            # 'Content-Type': 'text/plain',
            # 'Referer': 'http://ggzy.ah.gov.cn/bulletininfo.do?method=showList&bulletinType=01&fileType=2&hySort=&bulletinclass=jy&num=1',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36',
        }

    def parse(self):
        date = tool.date
        # date = '2020-07-10'
        page = 0
        while True:
            page += 1
            if page == 1:
                text = tool.requests_get(self.url.format('node_163'), self.headers)
            else:
                text = tool.requests_get(self.url.format('node_163_'+str(page)), self.headers)
            detail = HTML(text).xpath('/html/body/div/div[3]/div[2]/div[2]/ul/li')
            print('*' * 20, page, '*' * 20)
            for li in detail:
                title = li.xpath('./a/text()')[0]
                url = 'http://www.tjgdjt.com/xinwen/'+ li.xpath('./a/@href')[0]
                date_Today = li.xpath('./span/text()')[0]
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
            if page == 20:
                self.url = self.url_list.pop(0)
                break

    def parse_detile(self, title, url, date):
        print(url)
        t = tool.requests_get(url, self.headers)
        url_html = etree.HTML(t)
        detail = url_html.xpath('/html/body/div[1]/div[3]/div[2]/div[1]')[0]
        detail_html = etree.tostring(detail, method='HTML')
        detail_html = html.unescape(detail_html.decode()).replace('\xa0', '').replace('\ufeff', '')
        detail_text = url_html.xpath('string(/html/body/div[1]/div[3]/div[2]/div[1])') \
            .replace('\xa0', '').replace('\n', '').replace('\r', '').replace('\t', '') \
            .replace(' ', '').replace('\xa5', '').replace('\ufeff', '')
        # print(detail_text)
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
        item['winner'] = tool.get_winner(detail_text)
        item['address'] = tool.get_address(detail_text)
        item['nativeplace'] = self.get_nativeplace_to(item['title'])
        item['linkman'] = tool.get_linkman(detail_text)
        item['function'] = tool.get_function(detail_text)
        item['resource'] = '天津轨道交通'
        item["shi"] = int(str(item["nativeplace"]).split('.')[0])
        item['sheng'] = 1500
        item['removal']= title
        process_item(item)
        # print(item['body'])

    def get_nativeplace_to(self, city):
        a = ''
        ls = [['1501', '和平区'], ['1502', '河东区'], ['1503', '河西区'], ['1504', '南开区'], ['1505', '河北区'], ['1506', '红桥区'], ['1507', '塘沽区'], ['1508', '汉沽区'], ['1509', '大港区'], ['1510', '东丽区'], ['1511', '西青区'], ['1512', '津南区'], ['1513', '北辰区'], ['1514', '武清区'], ['1515', '宝坻区'], ['1516', '宁河县'], ['1517', '静海县'], ['1518', '蓟县']]
        for i in ls:
            if i[1] in city:
                a = i[0]
                break
        if a == '':
            return 1500
        else:
            return a

if __name__ == '__main__':
    jl = xinyang_ggzy()
    jl.parse()
    try:
        jl = anshun_ggzy()
        jl.parse()
    except Exception as e:
        traceback.print_exc()
        tool.send_error('报错文件：'+str(os.path.basename(__file__))+'报错信息：'+str(e))


