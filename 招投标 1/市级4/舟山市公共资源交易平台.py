# -*- coding: utf-8 -*-
import json
import re
import time, html
import requests
from lxml import etree
from lxml.etree import HTML
import tool
from save_database import process_item

# 舟山市公共资源交易平台
class zhoushan_ggzy:
    def __init__(self):
        self.url_list = [
            'http://zsztb.zhoushan.gov.cn/col/col1229679799/index.html'
        ]
        self.url = self.url_list.pop(0)
        self.headers = {
            'Accept': 'application/json, text/javascript, */*; q=0.01',
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'Authorization': 'Bearer e394f9c7abd6a526d90ded06618d5b03',
            'Cookie': 'ASP.NET_SessionId=lbabxmeebhyl5q20qmv4rkm3',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36',
        }

    def parse(self):
        date = tool.date
        # date = '2022-05-21'
        page = 0
        while True:
            page += 1
            text = tool.requests_get(self.url, self.headers)
            print('*' * 20, page, '*' * 20)
            # html = HTML(text)
            # print(11, text)
            # time.sleep(6666)
            # detail = html.xpath('//*[@id="infolist"]/tr')
            # detail = json.loads(text)['custom']['infodata']
            # for li in detail:
            #     title = li['title']
            #     url = 'http://zsztb.zhoushan.gov.cn' + li['infourl']
            #     date_Today = li['infodate'].replace('[', '').replace(']', '').replace('/', '-')
            title_rule = re.compile(r'headers\[i\]=\"(?P<title>.*?)\"\;')
            urls_rule = re.compile(r'urls\[i\]=\'(?P<url2>.*?)\'\;')
            year_rule = re.compile(r'year\[i\]=\'(?P<year>.*?)\'\;')
            month_rule = re.compile(r'month\[i\]=\'(?P<month>.*?)\'\;')
            day_rule = re.compile(r'day\[i\]=\'(?P<day>.*?)\'\;')
            title_result = title_rule.finditer(text)
            urls_result = urls_rule.finditer(text)
            year_result = year_rule.finditer(text)
            month_result = month_rule.finditer(text)
            day_result = day_rule.finditer(text)
            for i in title_result:
                for u in urls_result:
                    for y in year_result:
                        for m in month_result:
                            for d in day_result:
                                title = i.group('title')
                                urls = u.group('url2')
                                url = 'http://zsztb.zhoushan.gov.cn' + urls
                                year = y.group('year')
                                month = m.group('month')
                                day = d.group('day')
                                date_Today = year + '-' + month + '-' + day
                                print(date)
                                # print(title, url, date_Today)
                                # time.sleep(666)
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
        url_html = etree.HTML(tool.requests_get(url, self.headers))
        try:
            detail = url_html.xpath('//*[@class="project-main"]/div')[0]
            detail_html = etree.tostring(detail, method='HTML')
            detail_html = html.unescape(detail_html.decode())
            detail_text = url_html.xpath('string(//*[@class="project-main"]/div)').replace('\xa0', '').replace('\n', '').\
                replace('\r', '').replace('\t', '').replace(' ', '').replace('\xa5', '')
        except:
            detail = url_html.xpath('//*[@class="project-main"]')[0]
            detail_html = etree.tostring(detail, method='HTML')
            detail_html = html.unescape(detail_html.decode())
            detail_text = url_html.xpath('string(//*[@class="project-main"])').replace('\xa0', '').replace('\n',
                                                                                                                ''). \
                replace('\r', '').replace('\t', '').replace(' ', '').replace('\xa5', '')
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
        item['body'] = detail_html
        item['body'] = tool.qudiao_width(item['body'])
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
        item['resource'] = '舟山市公共资源交易平台'
        item['shi'] = 6009
        item['sheng'] = 6000
        item['removal']= title
        # print(item)
        process_item(item)

    def get_nativeplace(self, addr):
        city = ''
        city_list = [['6009.001', '定海区'], ['6009.002', '普陀区'], ['6009.003', '岱山县'], ['6009.004', '嵊泗县']]
        for i in city_list:
            if i[1] in addr:
                city = float(i[0])
                break
        if city == '':
            city = 6009
        return city
if __name__ == '__main__':
    jl = zhoushan_ggzy()
    jl.parse()





