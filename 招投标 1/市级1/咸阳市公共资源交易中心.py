# -*- coding: utf-8 -*-
import json
import re
import time, html
import requests
from lxml import etree
from lxml.etree import HTML
import tool
from save_database import process_item

# 咸阳市公共资源交易中心
class wenshan_ggzy:
    def __init__(self):
        self.url_list = [
            'http://xy.sxggzyjy.cn/jydt/001001/001001001/001001001001/{}.html',
            'http://xy.sxggzyjy.cn/jydt/001001/001001001/001001001002/{}.html',
            'http://xy.sxggzyjy.cn/jydt/001001/001001001/001001001005/{}.html',
            'http://xy.sxggzyjy.cn/jydt/001001/001001001/001001001003/{}.html',#结果
            'http://xy.sxggzyjy.cn/jydt/001001/001001004/001001004001/{}.html',
            'http://xy.sxggzyjy.cn/jydt/001001/001001004/001001004002/{}.html',
            'http://xy.sxggzyjy.cn/jydt/001001/001001004/001001004003/{}.html',#结果
            'http://xy.sxggzyjy.cn/jydt/001001/001001004/001001004004/{}.html'
    ]
        self.url = self.url_list.pop(0)
        self.headers = {
            'Cookie': 'homeid=1a444a31-e460-47ff-9931-1c075c0f3cd8',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36',
        }

    def parse(self):
        date = tool.date
        # date = '2020-09-22'
        page = 0
        while True:
            page += 1
            if page == 1:
                text = tool.requests_get(self.url.format('subPage'), self.headers)
            else:
                text = tool.requests_get(self.url.format(page), self.headers)
            print('*' * 20, page, '*' * 20)
            html = HTML(text)
            # print(11, text)
            # time.sleep(6666)
            detail = html.xpath('//*[@id="categorypagingcontent"]/ul/li')
            for li in detail:
                title = li.xpath('./a/@title')[0].replace('\n', '').\
                    replace('\r', '').replace('\t', '').replace(' ', '')
                url = 'http://xy.sxggzyjy.cn' + li.xpath('./a/@href')[0]
                date_Today = date[:5] + li.xpath('./span/text()')[0].replace('\xa0', '').replace('\n', '').\
                    replace('\r', '').replace('\t', '').replace(' ', '').replace('\xa5', '')
                if 'http' not in url:
                    url = 'http://xy.sxggzyjy.cn' + url
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
                print('日期不符, 正在切换类型')
                self.url = self.url_list.pop(0)
                break

    def parse_detile(self, title, url, date):
        print(url)
        t = tool.requests_get(url, self.headers)
        # print(t)
        # time.sleep(2222)
        url_html = etree.HTML(t)
        try:
            detail = url_html.xpath('//*[@id="mainContent"]')[0]
            detail_html = etree.tostring(detail, method='HTML')
            detail_html = html.unescape(detail_html.decode()).replace("display: none", '')
            detail_text = url_html.xpath('string(//*[@id="mainContent"])').replace('\xa0', '').replace('\n', '').\
                replace('\r', '').replace('\t', '').replace(' ', '').replace('\xa5', '')
            if len(detail_html) < 200:
                int('a')
        except:
            return
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
        # item['body'] = item['body'].replace('''<a href="http://www.hfztb.cn" target="_blank"><img src="../Template/Default/images/wybm.png"></a>''', '')
        # print(item['body'].replace('\xa0', '').replace('\xa5', '').replace('\xb3', ''))
        # time.sleep(6666)
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
        item['resource'] = '咸阳市公共资源交易中心'
        item['shi'] = 14004
        item['sheng'] = 14000
        # print(item)
        item['removal']= title
        process_item(item)

    def get_nativeplace(self, addr):
        city = ''
        city_list = [['14004.001', '秦都区'], ['14004.01', '长武县'], ['14004.011', '旬邑县'], ['14004.012', '淳化县'], ['14004.013', '武功县'], ['14004.014', '兴平'], ['14004.002', '杨凌区'], ['14004.003', '渭城区'], ['14004.004', '三原县'], ['14004.005', '泾阳县'], ['14004.006', '乾县'], ['14004.007', '礼泉县'], ['14004.008', '永寿县'], ['14004.009', '彬县']]

        for i in city_list:
            if i[1] in addr:
                city = float(i[0])
                break
        if city == '':
            city = 14004
        return city

if __name__ == '__main__':
    import traceback, os
    try:
        jl = wenshan_ggzy()
        jl.parse()
    except Exception as e:
        traceback.print_exc()
        tool.send_error('报错文件：'+str(os.path.basename(__file__))+'报错信息：'+str(e))


