# -*- coding: utf-8 -*-
import json
import re
import time, html, base64
import requests
from lxml import etree
from lxml.etree import HTML
import tool
from save_database import process_item

# 池州市公共资源交易中心
class chizhou_ggzy:
    def __init__(self):
        self.domain_name = 'http://ggj.chizhou.gov.cn'
        self.url_list = [
            'http://ggj.chizhou.gov.cn/front/bidcontent/9005001002',
            'http://ggj.chizhou.gov.cn/front/bidcontent/9005001005',
            'http://ggj.chizhou.gov.cn/front/bidcontent/9005001003',
            'http://ggj.chizhou.gov.cn/front/bidcontent/9005001004',
            'http://ggj.chizhou.gov.cn/front/bidcontent/9005001007',
            'http://ggj.chizhou.gov.cn/front/bidcontent/9005002002',
            'http://ggj.chizhou.gov.cn/front/bidcontent/9005002004',
            'http://ggj.chizhou.gov.cn/front/bidcontent/9005002003',
            'http://ggj.chizhou.gov.cn/front/bidcontent/9005002006',
        ]
        self.url = self.url_list.pop(0)
        self.headers = {
            # 'Accept': 'application/json, text/javascript, */*; q=0.01',
            # 'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'Cookie': 'ASP.NET_SessionId=35z2fvq5lvv2beeme22crjin; __CSRFCOOKIE=b36f48c6-fa2d-4882-bd90-6012bef4acb3',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36',

        }

    def parse(self):
        date = tool.date
        page = 0
        while True:
            page += 1
            data = {"filter":{"date":"","regionCode":"","tenderProjectType":"","tenderMode":""},"page":page,"rows":15,"searchKey":""}
            text = tool.requests_post_to(self.url, data, self.headers)
            # print('*' * 20, page, '*' * 20)
            detail = json.loads(text)['rows']
            for li in detail:
                title = li['title'].replace('\xa0', '').replace('\n', ''). \
                    replace('\r', '').replace('\t', '').replace(' ', '').replace('\xa5', '')
                url = 'http://ggj.chizhou.gov.cn/front/bidcontent/detailByTenderProjectCode?categoryCode={}&tenderProjectCode={}'.format(self.url.split('/')[-1], base64.b64encode(li['tenderProjectCode'].encode('utf-8')).decode('ascii')[:-1])
                date_Today = li['publishTime'][:10].replace('\xa0', '').replace('\n', ''). \
                    replace('\r', '').replace('\t', '').replace(' ', '').replace('\xa5', '') \
                    .replace('[', '').replace(']', '').replace('/', '-')
                if 'http' not in url:
                    url = self.domain_name + url
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
                break

    def parse_detile(self, title, url, date):
        print(url)
        t = tool.requests_get(url, self.headers).replace('\xa9', '').replace('<br>&nbsp;&nbsp;', '')
        detail_html = json.loads(t)['data'][0]['content']
        detail_text = ''.join(re.findall('>(.*?)<', detail_html, re.S)).replace('\xa0', '').replace('\n',

                                                                                                     ''). \
            replace('\r', '').replace('\t', '').replace(' ', '').replace('\xa5', '')
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
        # d = re.findall('''<td align='center' style='border:0;'>.*?</td>''', item['body'], re.S)
        # if len(d) != 0:
        item['body'] = item['body'].replace('''<a href="http://223.247.35.138/chiztpbidder/login.aspx?ReturnUrl=%2fchiztpbidder" class="abm"><font><strong>我要投标</strong></font></a>''', '').replace('\xa0', '')
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
        item['resource'] = '池州市公共资源交易中心'
        item['shi'] = 6516
        item['sheng'] = 6500
        item['removal']= title
        process_item(item)

    def get_nativeplace(self, addr):
        city = ''
        city_list = [['6516.001', '贵池区'], ['6516.002', '东至县'], ['6516.003', '石台县'], ['6516.004', '青阳县']]

        for i in city_list:
            if i[1] in addr:
                city = float(i[0])
                break
        if city == '':
            city = 6516
        return city

if __name__ == '__main__':
    jl = chizhou_ggzy()
    jl.parse()


