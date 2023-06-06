# -*- coding: utf-8 -*-
import json
import re
import time, html
import requests
from lxml import etree
from lxml.etree import HTML
import tool
from save_database import process_item

# 亚新电子交易平台
class baoshan_ggzy:
    def __init__(self):
        self.url_list = [
          'http://jypt.ahhyzb.com.cn:8080/jyxx/tradeInfo.html?categoryNum=002&pageIndex={}',
        ]
        self.url = self.url_list.pop(0)
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36',
        }

    def parse(self):
        date = tool.date
        # date = '2020-12-17'
        page = 0
        while True:
            page += 1

            text = tool.requests_get(self.url.format(page), self.headers)
            print('*' * 20, page, '*' * 20)
            html = HTML(text)
            # print(11, text)
            # time.sleep(6666)
            detail = html.xpath('//div[@class="infos-bd"]/ul/li')
            for li in detail:
                title = li.xpath('./a/@title')[0].replace('\n', '').replace('\t', '').replace(' ', '').replace('\r', '')
                data=li.xpath('./span/text()')[0].replace('\n', '').replace('\t', '').replace(' ', '').replace(
                    '\r', '').replace('发布日期:','').replace('-','')
                infoid=li.xpath('./a/@href')[0].split('&')[0].replace('/projectDetail.html?infoid=','')
                print(li.xpath('./a/@href'))
                i_id=li.xpath('./a/@href')[0].split('&')[1].replace('categorynum=','')
                url = f"http://jypt.ahhyzb.com.cn:8080/jyxx/{i_id}/{data}/{infoid}.html"

                date_Today = li.xpath('./span/text()')[0].replace('\n', '').replace('\t', '').replace(' ', '').replace(
                    '\r', '').replace('发布日期:','')
                if '测试' in title:
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
            if page == 20:
                self.url = self.url_list.pop(0)
                page = 0

    def parse_detile(self, title, url, date):
        print(url)
        t = tool.requests_get(url, self.headers)
        url_html = etree.HTML(t)
        detail = url_html.xpath('//div[@class="ewb-make-bd"]')[0]
        detail_html = etree.tostring(detail, method='HTML')
        detail_html = html.unescape(detail_html.decode()).replace('浏览次数：', '').replace('原文链接', '')
        detail_text = detail_html.replace('\xa0', '').replace('\n', ''). \
            replace('\r', '').replace('\t', '').replace(' ', '').replace('\xa5', '')
        if len(detail_text) < 300:
            return
        item = {}
        item['title'] = title.replace('\u2022', '')
        item['url'] = url
        item['date'] = date
        item['typeid'] = tool.get_typeid(item['title'])
        item['senddate'] = int(time.time())
        item['mid'] = 867
        item['nativeplace'] = tool.get_city(item['title'])
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
        item['address'] = tool.get_address(detail_text).replace('<em>','').replace('</em>','').replace('<p>','').replace('</p>','')
        item['linkman'] = tool.get_linkman(detail_text)
        item['function'] = tool.get_function(detail_text)
        item['resource'] = '寰亚新点电子交易平台'
        item['shi'] = tool.get_city(item['title'])
        item['sheng'] = tool.get_sheng(item['title'])
        item['removal']= title
        process_item(item)

    def get_nativeplace(self, addr):
        city = ''
        city_list = [['7004.001','梅列区'],['7004.01','泰宁县'],['7004.011','建宁县'],['7004.012','永安市'],['7004.002','三元区'],
    ['7004.003','明溪县'],['7004.004','清流县'],['7004.005','宁化县'],['7004.006','大田县'],['7004.007','尤溪县'],
    ['7004.008','沙　县'],['7004.009','将乐县']]
        for i in city_list:
            if i[1] in addr:
                city = float(i[0])
                break
        if city == '':
            city = 7004
        return city

if __name__ == '__main__':
    import traceback,os
    try:
        jl = baoshan_ggzy()
        jl.parse()
    except Exception as e:
        traceback.print_exc()
        tool.send_error('报错文件：'+str(os.path.basename(__file__))+'报错信息：'+str(e))



