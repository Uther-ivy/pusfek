# -*- coding: utf-8 -*-
import json
import re
import time, html
import requests
from lxml import etree
from lxml.etree import HTML
import tool
from save_database import process_item

# 岳阳市公共资源交易平台
class yueyang_ggzy:
    def __init__(self):
        self.url_list = [
            # 市本级
            #   工程建设
            'http://ggzy.yueyang.gov.cn/56114/56125/{}',
            #   政府采购
            'http://ggzy.yueyang.gov.cn/56114/56131/{}',
            # 医疗采购
            'http://ggzy.yueyang.gov.cn/56114/56143/{}'
        ]
        self.url = self.url_list.pop(0)
        self.headers = {
            'Cookie': 'HttpOnly; VISIT_UV=202004081515232746039586; HttpOnly; HttpOnly; HttpOnly; VISIT_UV=202004081515232746039586',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36',
        }

    def requests_get(self, url, headers):
        num = 0
        while True:
            try:
                p = tool.process_request()
                proxies = {
                    'http': p,
                    'https': p
                }
                rst = requests.get(url, headers=headers, timeout=30, verify=False, proxies=proxies)
                rst.encoding = rst.apparent_encoding
                return rst.text
            except Exception as e:
                print('请求错误', e.args)
                num += 1
                if num == 10:
                    int('a')
                time.sleep(5)
                continue

    def parse(self):
        date = tool.date
        # date = '2020-04-08'
        page = 0
        while True:
            page += 1
            if page == 1:
                text = self.requests_get(self.url.format('index.htm'), self.headers)
            else:
                text = self.requests_get(self.url.format('index_'+ str(page-1)+'.htm'), self.headers)
            print('*' * 20, page, '*' * 20)
            html = HTML(text)
            # print(11, text)
            # time.sleep(6666)
            detail = html.xpath('//*[@class="list-right"]/ul/li')
            for li in detail:
                title = li.xpath('./a/@title')[0]
                url = self.url.format(li.xpath('./a/@href')[0])
                date_Today = li.xpath('./span/text()')[0]
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
                    self.url = self.url_list.pop(0)

                    break
            if page == 20:
                self.url = self.url_list.pop(0)
                break

    def parse_detile(self, title, url, date):
        print(url)
        url_html = etree.HTML(self.requests_get(url, self.headers))
        detail = url_html.xpath('//*[@id="content"]')[0]
        detail_html = etree.tostring(detail, method='HTML')
        detail_html = html.unescape(detail_html.decode())
        detail_text = url_html.xpath('string(//*[@id="content"])').replace('\xa0', '').replace('\n', '').\
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
        item['resource'] = '岳阳市公共资源交易网'
        item['shi'] = 9506
        item['sheng'] = 9500
        item['removal']= title
        process_item(item)

    def get_nativeplace(self, addr):
        city = ''
        city_list = [['9506.001', '岳阳楼区'], ['9506.002', '云溪区'], ['9506.003', '君山区'], ['9506.004', '岳阳县'], ['9506.005', '华容县'], ['9506.006', '湘阴县'], ['9506.007', '平江县'], ['9506.008', '汨罗市'], ['9506.009', '临湘市']]
        for i in city_list:
            if i[1] in addr:
                city = float(i[0])
                break
        if city == '':
            city = 9506
        return city

if __name__ == '__main__':
    import traceback, os
    try:
        jl = yueyang_ggzy()
        jl.parse()
    except Exception as e:
        traceback.print_exc()
        tool.send_error('报错文件：'+str(os.path.basename(__file__))+'报错信息：'+str(e))


