# -*- coding: utf-8 -*-
import json
import re
import time, html
import requests
from lxml import etree
from lxml.etree import HTML
import tool
from save_database import process_item

# 阜新市公共资源交易网
class fuxin_ggzy:
    def __init__(self):
        self.url_code = [
            # 建设工程
            'http://ggzy.fuxin.gov.cn/jsgc/{}.html',
            # 政府采购
            'http://ggzy.fuxin.gov.cn/zfcg/{}.html'
        ]
        self.url = self.url_code.pop(0)
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36'
        }

    def parse(self):
        date = tool.date
        # date = '2020-01-10'
        page = 0
        for i in range(1,20):
            page += 1
            if page == 1:
                text = tool.requests_get(self.url.format('secondPage'), self.headers)
            else:
                text = tool.requests_get(self.url.format(page), self.headers)
            # print(text)
            if '503 Service Unavailable' in text:
                break
            html = HTML(text)
            print('*' * 20, page, '*' * 20)
            detail = html.xpath('/html/body/div[2]/div[2]/div[2]/ul/li')
            for li in detail:
                title = li.xpath('./a/@title')[0]
                url = 'http://ggzy.fuxin.gov.cn' + li.xpath('./a/@href')[0]
                date_Today = li.xpath('./span/text()')[0]
                # print(11, title, url, date_Today)
                # time.sleep(666)
                if tool.Transformation(date) <= tool.Transformation(date_Today):
                    if tool.removal(title, date):
                        self.parse_detile(title, url, date_Today)
                    else:
                        print('【existence】', url)
                        continue
                else:
                    print('日期不符, 正在切换类型...', date_Today)
                    self.url = self.url_code.pop(0)
                    page = 0
                    break
            if page == 20:
                self.url = self.url_code.pop(0)
                page = 0
    def parse_detile(self, title, url, date):
        print(url)
        url_html = etree.HTML(tool.requests_get(url, self.headers))
        detail = url_html.xpath('/html/body/div[2]/div[2]/div/div[2]')[0]
        detail_html = etree.tostring(detail, method='HTML')
        detail_html = html.unescape(detail_html.decode())
        detail_text = url_html.xpath('string(/html/body/div[2]/div[2]/div/div[2])').replace('\xa0', '').replace('\n', '').\
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
        width_list = re.findall('width="(.*?)"', item["body"])
        for i in width_list:
            item["body"] = item["body"].replace('width="{}"'.format(i), '')
        width_list = re.findall('WIDTH: (.*?)pt;', item["body"])
        for i in width_list:
            item["body"] = item["body"].replace('WIDTH: {}pt;'.format(i), '')
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
        item['resource'] = '阜新市公共资源交易网'
        item['shi'] = 3509
        item['sheng'] = 3500
        item['removal']= title
        process_item(item)

    def get_nativeplace(self, addr):
        city = ''
        city_list = [['3509.001', '海州区'], ['3509.002', '新邱区'], ['3509.003', '太平区'], ['3509.004', '清河门区'], ['3509.005', '细河区'], ['3509.006', '阜新蒙古族自治县'], ['3509.007', '彰武县']]
        for i in city_list:
            if i[1] in addr:
                city = float(i[0])
                break
        if city == '':
            city = 3509
        return city

if __name__ == '__main__':

    import traceback, os
    try:
        jl = fuxin_ggzy()
        jl.parse()
    except Exception as e:
        traceback.print_exc()
        tool.send_error('报错文件：'+str(os.path.basename(__file__))+'报错信息：'+str(e))


