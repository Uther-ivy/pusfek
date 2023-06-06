# -*- coding: utf-8 -*-
import json
import re
import time, html
import traceback

import requests
from lxml import etree
from lxml.etree import HTML
import tool
from save_database import process_item

# 青海公共资源交易网
class xinyang_ggzy:
    def __init__(self):
        self.url_list = ['001001', '001002', '001003', '001004', '001005']
        self.url = self.url_list.pop(0)
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36',
            # 'Cookie': 'JSESSIONID=Jhs7fR6dYN1sfp2nr6qwFFyJzQGyyxJY4DbWnkT0FvTx1DR6hH3y!-1581166878'
            # 'Cookie': 'JSESSIONID=6cf5cad7-9e11-4d3d-9efd-70e2f5bc0d11'
        }

    def parse(self):
        # print(headers)
        # time.sleep(6666)
        date = tool.date
        # date = '2020-07-10'
        page = 0
        url_to = 'http://www.qhggzyjy.gov.cn/inteligentsearch/rest/inteligentSearch/getFullTextData'
        while True:
            page += 1
            data = {"token": "", "pn": page*10-10, "rn": 10, "sdt": "", "edt": "", "wd": "", "inc_wd": "", "exc_wd": "",
                    "fields": "title", "cnum": "001;002;003;004;005;006;007;008;009;010",
                    "sort": "{\"showdate\":\"0\"}",
                    "ssort": "title", "cl": 200, "terminal": "",
                    "condition": [{"fieldName": "categorynum", "isLike": True, "likeType": 2, "equal": self.url}],
                    "time": None, "highlights": "title", "statistics": None, "unionCondition": None, "accuracy": "100",
                    "noParticiple": "0", "searchRange": None, "isBusiness": 1}
            text = tool.requests_post_to(url_to, data, self.headers)
            detail = json.loads(text)['result']['records']
            # print(text)
            # time.sleep(6666)
            print('*' * 20, page, '*' * 20)
            for tr in detail:
                title = tr['title']
                date_Today = tr['infodate'][:10]
                url = 'http://www.qhggzyjy.gov.cn' + tr['linkurl']
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
            if page == 30:
                self.url = self.url_list.pop(0)
                break


    def parse_detile(self, title, url, date):
        print(url)
        t = tool.requests_get(url, self.headers)
        # print(t)
        # time.sleep(6666)
        url_html = etree.HTML(t)
        try:
            detail = url_html.xpath('//*[@id="page"]/div[3]/div/div[2]')[0]
        except:
            return
        detail_html = etree.tostring(detail, method='HTML')
        detail_html = html.unescape(detail_html.decode()).replace('\xa0', '').replace('\ufeff', '')
        detail_text = url_html.xpath('string(//*[@id="page"]/div[3]/div/div[2])') \
            .replace('\xa0', '').replace('\n', '').replace('\r', '').replace('\t', '') \
            .replace(' ', '').replace('\xa5', '').replace('\ufeff', '')
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
        item['address'] = tool.get_address(detail_text)
        item['nativeplace'] = self.get_nativeplace(item['title'])
        item['linkman'] = tool.get_linkman(detail_text)
        item['function'] = tool.get_function(detail_text)
        item['resource'] = '青海公共资源交易网'
        item["shi"] = int(str(item["nativeplace"]).split('.')[0])
        item['sheng'] = 15000
        item['removal']= title
        process_item(item)
        # print(item['body'])

    def get_nativeplace(self, addr):
        city = ''
        city_list = [['15001', '西宁'], ['15001.001', '城东'], ['15001.002', '城中'], ['15001.003', '城西'], ['15001.004', '城北'], ['15001.005', '大通回族土族自治'], ['15001.006', '湟中'], ['15001.007', '湟源'], ['15002', '海东地'], ['15002.001', '平安'], ['15002.002', '民和回族土族自治'], ['15002.003', '乐都'], ['15002.004', '互助土族自治'], ['15002.005', '化隆回族自治'], ['15002.006', '循化撒拉族自治'], ['15003', '海北藏族自治州'], ['15003.001', '门源回族自治'], ['15003.002', '祁连'], ['15003.003', '海晏'], ['15003.004', '刚察'], ['15004', '黄南藏族自治州'], ['15004.001', '同仁'], ['15004.002', '尖扎'], ['15004.003', '泽库'], ['15004.004', '河南蒙古族自治'], ['15005', '海南藏族自治州'], ['15005.001', '共和'], ['15005.002', '同德'], ['15005.003', '贵德'], ['15005.004', '兴海'], ['15005.005', '贵南'], ['15006', '果洛藏族自治州'], ['15006.001', '玛沁'], ['15006.002', '班玛'], ['15006.003', '甘德'], ['15006.004', '达日'], ['15006.005', '久治'], ['15006.006', '玛多'], ['15007', '玉树藏族自治州'], ['15007.001', '玉树'], ['15007.002', '杂多'], ['15007.003', '称多'], ['15007.004', '治多'], ['15007.005', '囊谦'], ['15007.006', '曲麻莱'], ['15008', '海西蒙古族藏族自治州'], ['15008.001', '格尔木'], ['15008.002', '德令哈'], ['15008.003', '乌兰'], ['15008.004', '都兰']]

        for i in city_list:
            if i[1] in addr:
                city = float(i[0])
                break
        if city == '':
            city = 15000
        return city

if __name__ == '__main__':
    jl = xinyang_ggzy()
    jl.parse()


