# -*- coding: utf-8 -*-
import json
import re, asyncio
import time, html
import requests
from lxml import etree
from lxml.etree import HTML
import tool
from save_database import process_item

# 白银市公共资源交易平台
class baoshan_ggzy:
    def __init__(self):  #  url中的App_Web_fry0c105  会定期变换
        self.url_list = [
            'http://ggzyjy.baiyin.gov.cn{}?_method=getTradeDataList&_session=no'
                         ]
        self.url = self.url_list.pop(0)
        self.session = requests.session()
        self.headers = {
            'Accept': '*/*',
            'Cookie': 'userName=; number=4942191; Hm_lvt_06dc77eaa473c9272f6495913fda20e3=1627978616,1627980364; Hm_lpvt_06dc77eaa473c9272f6495913fda20e3=1627980364; SERVERID=02204eefebef9d539ec310f9d13d1c6e|1627980790|1627980361',
            'Host': 'ggzyjy.baiyin.gov.cn',
            'Origin': 'http://ggzyjy.baiyin.gov.cn',
            'Referer': 'http://ggzyjy.baiyin.gov.cn/InfoPage/TradeInfomation.aspx?state=1,2,3',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36',
        }


    def parse(self):
        date = tool.date
        # date = '2021-03-03'
        page = 0
        while True:
            page += 1
            u = 'http://ggzyjy.baiyin.gov.cn/InfoPage/TradeInfomation.aspx?state=1,2,3'
            code = HTML(tool.requests_get(u, self.headers)).xpath('//*[@id="form1"]/script[2]/@src')[0]
            data = 'infoType=0\ncurr='+str(page)+'\nkeywords=\nqueryStr=and\ta.PrjPropertyNew\tin\t(1,2,3,21,22,23,24,5,6,12,13,14,15,16,17,18,19,20,4,7,8,9,11,41,31,44,43,45,551,552,553,0,441,442,443,0,331,332,333,0,2000)\tand\ta.Field1\tin(3259,2955,2956,2957,2958,2959,2960)'
            text = tool.requests_post(self.url.format(code), data, self.headers)
            if text is False or '未将对象引用设置到对象的实例' in text:
                print('未将对象引用设置到对象的实例')
                time.sleep(5)
                page -= 1
                continue
            print('*' * 20, page, '*' * 20)
            html_ = HTML(text)
            detail = html_.xpath('//li')
            for li in detail:
                title = li.xpath('./a/@title')[0].replace('\n', '').replace('\r', '')\
                    .replace('\t', '').replace(' ', '')
                url = li.xpath('./a/@href')[0]
                if 'http' not in url:
                    url = 'http://ggzyjy.baiyin.gov.cn' + url[2:]
                date_Today = li.xpath('./span/text()')[0].replace('\n', '').replace('\r', '') \
                    .replace('\t', '').replace(' ', '').replace('(', '').replace(')', '').replace('.', '-')\
                    .replace('[', '').replace(']', '').replace('.', '-')
                if '测试' in title:
                    continue
                # print(title, url, date_Today)
                # time.sleep(666)
                if tool.Transformation(date_Today) == tool.Transformation(date):
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
                break

    def parse_detile(self, title, url, date):
        print(url)
        code_ = HTML(tool.requests_get(url, self.headers)).xpath('//*[@id="form1"]/script[2]/@src')[0]
        code = url.split('?')[1].replace('TenderProject=', '')
        data = 'tenderId=' + code
        url_to = 'http://ggzyjy.baiyin.gov.cn{}?_method=getTenderId&_session=no'
        t = tool.requests_post(url_to.format(code_), data, self.headers)
        if t is False:
            return
        data = 'tenderId=' + t.replace("'", '')
        url_to = 'http://ggzyjy.baiyin.gov.cn{}?_method=GetTenderProjetAndAnn&_session=no'
        detail_html = tool.requests_post(url_to.format(code_), data, self.headers)
        detail_text = ''.join(re.findall('>(.*?)<', detail_html, re.S)).replace('\xa0', '').replace('\n',
                                                                                                       ''). \
            replace('\r', '').replace('\t', '').replace(' ', '').replace('\xa5', '')
        if '没有相关公告' in detail_text or '未将对象引用设置到对象的实例' in detail_text:
            int('a')
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
        item['resource'] = '白银市公共资源交易平台'
        item['shi'] = 14504
        item['sheng'] = 14500
        item['removal']= title
        process_item(item)

    def get_nativeplace(self, addr):
        city = ''
        city_list = [['14504.001', '白银区'], ['14504.002', '平川区'], ['14504.003', '靖远县'], ['14504.004', '会宁县'], ['14504.005', '景泰县']]

        for i in city_list:
            if i[1] in addr:
                city = float(i[0])
                break
        if city == '':
            city = 14504
        return city

if __name__ == '__main__':
    import traceback, os
    try:
        jl = baoshan_ggzy()
        jl.parse()
    except Exception as e:
        traceback.print_exc()
