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

# 宁夏公共资源交易网
class xinyang_ggzy:
    def __init__(self):
        self.url_list = [
            'http://www.nxggzyjy.org/inteligentsearch_es/rest/esinteligentsearch/getFullTextDataNew'
        ]
        self.url = self.url_list.pop(0)
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36',
        }

    def parse(self):
        date = tool.date
        page = 0
        while True:
            data = {"token":"","pn":page*20,"rn":20,"sdt":"","edt":"","wd":"","inc_wd":"","exc_wd":"","fields":"","cnum":"","sort":"{\"istop\":\"0\",\"ordernum\":\"0\",\"webdate\":\"0\",\"infoid\":\"0\"}","ssort":"","cl":10000,"terminal":"","condition":[{"fieldName":"categorynum","equal":"002","notEqual":None,"equalList":None,"notEqualList":None,"isLike":True,"likeType":2}],"time":None,"highlights":"","statistics":None,"unionCondition":None,"accuracy":"","noParticiple":"1","searchRange":None,"noWd":True}
            page += 1
            print('*'*50, page)
            text = tool.requests_post_to(self.url, data, self.headers)
            # html = HTML(text)
            detail = json.loads(text)['result']['records']
            for li in detail:
                title = li['title']
                date_Today = li['infodate'][:10]
                url = 'http://www.nxggzyjy.org/ningxiaweb/{}/{}/{}/{}/{}.html'\
                    .format(li['categorynum'][:3],li['categorynum'][:6],li['categorynum'],date_Today.replace('-', ''), li['infoid'])
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
                    print('日期不符, 正在切换类型', date_Today)
                    page = 0

                    break



    def parse_detile(self, title, url, date):
        print(url)
        t = tool.requests_get(url, self.headers)
        # print(t)
        # time.sleep(6666)
        url_html = etree.HTML(t)
        try:
            quanrang = url_html.xpath('//*[@id="mainContent"]/text()')[0]
            if quanrang is not None:
                print('权让公告')
                return
        except:
            pass
        try:
            detail = url_html.xpath('//*[@id="tablecontent3"]')[0]
            detail_html = etree.tostring(detail, method='HTML')
            detail_html = html.unescape(detail_html.decode()).replace('\xa0', '').replace('\ufeff', '')
            detail_text = url_html.xpath('string(//*[@id="tablecontent3"])') \
                .replace('\xa0', '').replace('\n', '').replace('\r', '').replace('\t', '') \
                .replace(' ', '').replace('\xa5', '').replace('\ufeff', '')
            if len(detail_html) < 200:
                int('a')
        except:
            try:
                detail = url_html.xpath('//*[@id="createForm"]')[0]
                detail_html = etree.tostring(detail, method='HTML')
                detail_html = html.unescape(detail_html.decode()).replace('\xa0', '').replace('\ufeff', '')
                detail_text = url_html.xpath('string(//*[@id="createForm"])') \
                    .replace('\xa0', '').replace('\n', '').replace('\r', '').replace('\t', '') \
                    .replace(' ', '').replace('\xa5', '').replace('\ufeff', '')
                if len(detail_html) < 200:
                    int('a')
            except:
                try:
                    detail = url_html.xpath('//*[@class="epoint-article-content"]')[0]
                    detail_html = etree.tostring(detail, method='HTML')
                    detail_html = html.unescape(detail_html.decode()).replace('\xa0', '').replace('\ufeff', '')
                    detail_text = url_html.xpath('string(//*[@class="epoint-article-content"])') \
                        .replace('\xa0', '').replace('\n', '').replace('\r', '').replace('\t', '') \
                        .replace(' ', '').replace('\xa5', '').replace('\ufeff', '')
                    if len(detail_html) < 200:
                        int('a')
                except:
                    try:
                        detail = url_html.xpath('//*[@id="tablecontent1"]')[0]
                        detail_html = etree.tostring(detail, method='HTML')
                        detail_html = html.unescape(detail_html.decode()).replace('\xa0', '').replace('\ufeff', '')
                        detail_text = url_html.xpath('string(//*[@id="tablecontent1"])') \
                            .replace('\xa0', '').replace('\n', '').replace('\r', '').replace('\t', '') \
                            .replace(' ', '').replace('\xa5', '').replace('\ufeff', '')
                        if len(detail_html) < 200:
                            int('a')
                    except:
                        return
        item = {}
        item['title'] = title.replace('\u2022', '').replace('[None]', '')
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
        item['resource'] = '宁夏公共资源交易网'
        item["shi"] = int(item['nativeplace'])
        item['sheng'] = 15500
        item['removal']= title
        process_item(item)
        # print(item['body'])

    def get_nativeplace(self, addr):
        city = ''
        city_list = [['15501', '银川'], ['15501.001', '兴庆'], ['15501.002', '西夏'], ['15501.003', '金凤'], ['15501.004', '永宁'], ['15501.005', '贺兰'], ['15501.006', '灵武'], ['15502', '石嘴山'], ['15502.001', '大武口'], ['15502.002', '惠农'], ['15502.003', '平罗'], ['15503', '吴忠'], ['15503.001', '利通'], ['15503.002', '盐池'], ['15503.003', '同心'], ['15503.004', '青铜峡'], ['15503.005', '红寺堡'], ['15504', '固原'], ['15504.001', '原州'], ['15504.002', '西吉'], ['15504.003', '隆德'], ['15504.004', '泾源'], ['15504.005', '彭阳'], ['15505', '中卫'], ['15505.001', '沙坡头'], ['15505.002', '中宁']]

        for i in city_list:
            if i[1] in addr:
                city = float(i[0])
                break
        if city == '':
            city = 15500
        return city

if __name__ == '__main__':
    try:
        jl = xinyang_ggzy()
        jl.parse()
    except Exception as e:
        traceback.print_exc()


