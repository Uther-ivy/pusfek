# -*- coding: utf-8 -*-
import json
import re
import time, html
import requests
from lxml import etree
from lxml.etree import HTML
import tool
from save_database import process_item

# 梧州市公共资源交易中心
class wenshan_ggzy:
    def __init__(self):
        self.domain_name = 'http://ggzy.jgswj.gxzf.gov.cn'
        self.url_list = [
            'http://ggzy.jgswj.gxzf.gov.cn/inteligentsearchgxes/rest/esinteligentsearch/getFullTextDataNew'
        ]
        self.url = self.url_list.pop(0)
        self.headers = {
            'Accept': 'application/json, text/javascript, */*; q=0.01',
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'Cookie': 'ASP.NET_SessionId=35z2fvq5lvv2beeme22crjin; __CSRFCOOKIE=b36f48c6-fa2d-4882-bd90-6012bef4acb3',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36',

        }
    def parse(self):
        date = tool.date
        # date = '2022-05-31'
        page = 0
        while True:
            page += 1
            data = {"token": "", "pn": (page-1)*15, "rn": 15, "sdt": "", "edt": "", "wd": "", "inc_wd": "", "exc_wd": "",
                    "fields": "title", "cnum": "005", "sort": "{\"infodatepx\":\"0\"}", "ssort": "title", "cl": 200,
                    "terminal": "", "condition": [
                    {"fieldName": "categorynum", "equal": "001001001001", "notEqual": None, "equalList": None,
                     "notEqualList": None, "isLike": True, "likeType": 2}], "time": None, "highlights": "",
                    "statistics": None, "unionCondition": None, "accuracy": "", "noParticiple": "0",
                    "searchRange": None, "isBusiness": "1"}
            text = tool.requests_post_to(self.url, data, self.headers)
            print('*' * 20, page, '*' * 20)
            page = json.loads(text)
            detail=page["result"]["records"]
            for li in detail:
                title = li['title'].replace('\xa0', '').replace('\n', ''). \
                    replace('\r', '').replace('\t', '').replace(' ', '').replace('\xa5', '')
                url = 'http://ggzy.jgswj.gxzf.gov.cn/wzggzy' + li['linkurl']
                date_Today = li['infodate'][:10]
                if 'http' not in url:
                    url = self.domain_name + url
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
                    return


    def parse_detile(self, title, url, date):
        print(url)
        t = tool.requests_get(url, self.headers).replace('\xa9', '').replace('<br>&nbsp;&nbsp;', '')
        # print(t)
        # time.sleep(2222)
        url_html = etree.HTML(t)
        detail = url_html.xpath('//*[@class="ewb-details-info"]')[0]
        detail_html = etree.tostring(detail, method='HTML')
        detail_html = html.unescape(detail_html.decode()).replace("display: none", '')
        detail_text = url_html.xpath('string(//*[@class="ewb-details-info"])').replace('\xa0', '').replace('\n',

                                                                                                     ''). \
            replace('\r', '').replace('\t', '').replace(' ', '').replace('\xa5', '')
        if len(detail_html) < 200:
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
        # item['body'] = tool.update_img(self.domain_name, item['body'])
        # d = re.findall('<div class="news-article-info">.*?</div>', item['body'], re.S)
        # if len(d) != 0:
        #     item['body'] = item['body'].replace(d[0], '').replace('\xa0', '')
        # print(item['body'])
        # time.sleep(2222)
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
        item['resource'] = '梧州市公共资源交易中心'
        item['shi'] = 10504
        item['sheng'] = 10500
        item['removal']= title
        # print(item["body"])
        process_item(item)

    def get_nativeplace(self, addr):
        city = ''
        city_list = [['10504.001', '万秀区'], ['10504.002', '蝶山区'], ['10504.003', '长洲区'], ['10504.004', '苍梧县'], ['10504.005', '藤县'], ['10504.006', '蒙山县'], ['10504.007', '岑溪']]

        for i in city_list:
            if i[1] in addr:
                city = float(i[0])
                break
        if city == '':
            city = 10504
        return city

if __name__ == '__main__':
    import os,traceback
    try:
        jl = wenshan_ggzy()
        jl.parse()
    except Exception as e:
        traceback.print_exc()
